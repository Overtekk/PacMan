# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  collision_manager.py                              :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 20:04:13 by roandrie        #+#    #+#               #
#  Updated: 2026/06/12 12:00:01 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any

import arcade

from .gamestate_manager import GameStateManager
from .game_settings import LevelState
from src.entity import Entity, Player, Movable, EnemyState
from src.utils import print_log, SuperCalculator
from src.audio import AudioManager
from src import game_config


class CollisionManager():
    """Manages all 2D collision detection and resolution within the game grid

    Handles spatial intractions including actor-vs-wall obstructions,
    player-vs-enemy contact, and collectible item gathering.
    """

    def __init__(
        self,
        player_reference: Player,
        enemies_reference: dict[str, Any],
        enemies_sprite_list: arcade.SpriteList[Any],
        pacgums_sprite_list: arcade.SpriteList[Any],
        super_pacgums_sprite_list: arcade.SpriteList[Any],
        maze_bitmap: dict[tuple[int, int], int],
        calculator: SuperCalculator,
        state_manager: GameStateManager,
        audio_manager: AudioManager,
    ) -> None:
        """Initializes the collision manager with world and actor context.

        Args:
            player_reference (Player): Reference to the player object instance.
            enemies_reference (dict[str, Any]): Dictionary mapping enemy
            identifiers to instances.
            enemies_sprite_list (arcade.SpriteList): Arcade engine list holding
            enemy sprites.
            pacgums_sprite_list (arcade.SpriteList): Arcade engine list holding
            standard pacgums.
            super_pacgums_sprite_list (arcade.SpriteList): Arcade engine list
            holding power pacgums.
            maze_bitmap (dict[tuple[int, int], int]): Structural matrix map
            defining wall coordinates.
            calculator (SuperCalculator): Spatial unit dimension translation
            tool.
            state_manager (GameStateManager): System interface handling scores,
            status, and lives.
            audio_manager (AudioManager): Central sound registry controller.
        """

        self.player_reference = player_reference
        self.enemies_reference = enemies_reference
        self.enemies_sprite_list = enemies_sprite_list
        self.pacgums_sprite_list = pacgums_sprite_list
        self.super_pacgums_sprite_list = super_pacgums_sprite_list
        self.maze_bitmap = maze_bitmap
        self.state_manager = state_manager
        self.audio_manager = audio_manager
        self.calculator = calculator

        self.offset_x: float = self.calculator.maze_offset_x
        self.offset_y: float = self.calculator.maze_offset_y
        self.tile_size: float = self.calculator.maze_tile_size

        self.pacgums_sprite_list_total: int = len(self.pacgums_sprite_list)

        # DEBUG
        self.debug_force_death: bool = False

    def update(self, delta_time: float) -> LevelState:
        """Evaluates ongoing collision criteria for all active scene objects.

        Processes environment bounding restrictions, validates interaction
        results
        such as player casualties or ghost consumption, and computes overall
        progression.

        Args:
            delta_time (float): Seconds elapsed since the last system tick.

        Returns:
            LevelState: Enum signal defining the resulting lifecycle state
            modification.
        """
        # Check collisions for the player with walls
        self._entity_collisions_logic(self.player_reference)

        # Check collisions for enemies with walls
        for enemy in self.enemies_reference.values():
            self._entity_collisions_logic(enemy)

        # Check for collision between player/enemy
        enemy_colliding: list[arcade.Sprite] = (
            self._check_collisions_with_enemy()
        )

        # Check for collision between player/collectibles
        list_colliding: list[arcade.Sprite] = (
            self._check_collision_with_collectibles()
        )

        # Check state of enemies
        for enemy in enemy_colliding:
            if hasattr(enemy, 'parent'):
                if enemy.parent.is_edible and not enemy.parent.died:
                    self._kill_enemy(enemy.parent, delta_time)
                    return LevelState.ENEMY_DIED

        # Debug force player to died
        if self.debug_force_death:
            self._kill_player()
            return LevelState.PLAYER_DIED

        # Kill player if an enemy is colliding with him
        if not self.player_reference.cheat_invincible:
            if len(enemy_colliding) > 0:
                for enemy in enemy_colliding:
                    if hasattr(enemy, 'parent'):
                        if not enemy.parent.died:
                            if (not self.player_reference.invincible
                               or enemy.parent.have_respawned):
                                self._kill_player()
                                return LevelState.PLAYER_DIED

        # Get the collectible if it collides with the player
        if len(list_colliding) > 0:
            for obj in list_colliding:
                if hasattr(obj, 'parent'):
                    self._collect_collectible(obj.parent)

        # Check if all pacgums are eaten
        if len(self.pacgums_sprite_list) == 0:
            for sprite in self.super_pacgums_sprite_list:
                sprite.remove_from_sprite_lists()
            return LevelState.LEVEL_COMPLETED

        return LevelState.CONTINUE

    # :---------------:
    #  PRIVATE METHODS
    # :---------------:

    def _kill_player(self) -> None:
        """
        Processes player mortality events, updates audio assets, and subtracts
        lives.
        """
        if self.debug_force_death:
            self.debug_force_death = False

        self.audio_manager.play_sound('dead1', 1.0)
        self.state_manager.live -= 1

        if game_config.debug_mode:
            print_log(
                f"Player died! Life remaining: {self.state_manager.live}"
            )

    def _kill_enemy(self, enemy: Any, delta_time: float) -> None:
        """Dispatches an enemy lifecycle state change to defeated and awards
        points.

        Args:
            enemy (Any): The enemy class instance being consumed.
            delta_time (float): Delta timing tracker from the execution window.
        """
        self.audio_manager.play_random_sound(
            ['slurp1', 'slurp2', 'slurp3', 'slurp4', 'slurp5'], 2.0
        )
        enemy.die(delta_time)
        self.state_manager.score += self.state_manager.config.ghost_points

        if game_config.debug_mode:
            print_log(f"{enemy} died!")

    def _collect_collectible(self, collectible: Any) -> None:
        """Handles player acquisition of item pickups and increments the active
          score index.

        Args:
            collectible (Any): The item object picked up by the player.
        """
        # self.audio_manager.play_random_sound(
        #     ['eat1', 'eat2', 'eat3'], 2.0
        # )
        self.audio_manager.play_sound('eat1')

        self.state_manager.score += collectible.score

        if game_config.debug_mode:
            print_log(
                f'{len(self.pacgums_sprite_list)}/'
                f'{self.pacgums_sprite_list_total}'
            )
            print_log(f"+{collectible.score} points.")

        # Activate power if it's a superpacgum
        if hasattr(collectible, 'is_activate'):
            self._activate_superpacgum()

        # Remove the sprite
        collectible.sprite.kill()

    def _activate_superpacgum(self) -> None:
        """
        Triggers the invincibility power-up loop and shifts enemy AI to runaway
          mode.
        """
        if game_config.debug_mode:
            print_log("Activate SUPERPACGUM")

        self.audio_manager.stop_sound('music_invincible')
        if hasattr(self.state_manager.parent_view, 'level_sound'):
            self.audio_manager.pause_sound(
                self.state_manager.parent_view.level_sound
            )
        self.audio_manager.play_sound('music_invincible', 0.3)

        self.player_reference.invincible = True

        if hasattr(self.state_manager.parent_view, '_pacgum_timer'):
            self.state_manager.parent_view._pacgum_timer = (
                game_config.time_power_up
            )

        for enemy in self.enemies_reference.values():
            if enemy.mode in [EnemyState.RESPAWN, EnemyState.WAIT]:
                continue

            if enemy.mode != EnemyState.RUNAWAY:
                enemy.mode = EnemyState.RUNAWAY
                enemy.have_respawned = False

            enemy.is_edible = True
            enemy.sprite.color = (64, 99, 193)
            enemy.speed = ((enemy.base_speed - (enemy.base_speed//10)))

            # Turn the enemy
            x: float = enemy.current_direction[0] * -1.0
            y: float = enemy.current_direction[1] * -1.0
            enemy.current_direction = (x, y)

    def _entity_collisions_logic(self, entity: Movable) -> None:
        """Resolves structural navigation boundaries, grid snapping, and
        direction buffers.

        Locks perpendicular movement components to prevent tracking slippage
        outside valid corridors.

        Args:
            entity (Movable): The entity instance requiring position
            validation.
        """
        # Get the exact center of the current tile
        center_x, center_y = self._get_tile_center(entity)

        # Verify if player near the center
        at_center: bool = (
            abs(entity.x - center_x) < 3 and abs(entity.y - center_y) < 3
        )

        # BUFFER logic
        if at_center and entity._next_direction != (0.0, 0.0):
            if self._check_for_collisions(entity, entity._next_direction):
                entity.current_direction = entity._next_direction
                entity._next_direction = (0.0, 0.0)

        direction: tuple[float, float] = entity.current_direction

        # If the player is not moving, do nothing
        if direction == (0.0, 0.0):
            return

        # Check if there is a wall in front
        path_is_clear = self._check_for_collisions(entity, direction)

        if not path_is_clear:
            dx, dy = direction

            # Check if the player has reached or passed the center on their
            # movement axis
            if dx > 0 and entity.x >= center_x:
                entity.x = center_x
                entity.current_direction = (0.0, 0.0)

            elif dx < 0 and entity.x <= center_x:
                entity.x = center_x
                entity.current_direction = (0.0, 0.0)

            elif dy > 0 and entity.y >= center_y:
                entity.y = center_y
                entity.current_direction = (0.0, 0.0)

            elif dy < 0 and entity.y <= center_y:
                entity.y = center_y
                entity.current_direction = (0.0, 0.0)

        else:
            # Snap the player
            # Path is clear, lock the perpendicular axis
            dx, dy = direction

            # Vertical movement: lock X to the center
            if dy != 0 and dx == 0:
                entity.x = center_x

            # Horizontal movement: lock Y to the center
            elif dx != 0 and dy == 0:
                entity.y = center_y

    def _check_collisions_with_enemy(self) -> list[arcade.Sprite]:
        """Scans overlapping bounds between the player and the enemy layer.

        Returns:
            list[arcade.Sprite]: Overlapping target object sprites discovered.
        """
        colliding_sprite: list[arcade.Sprite] = (
            arcade.check_for_collision_with_list(
                self.player_reference.sprite,
                sprite_list=self.enemies_sprite_list
            ))

        return colliding_sprite

    def _check_collision_with_collectibles(self) -> list[arcade.Sprite]:
        """Scans overlapping bounds between the player and all consumable
        structures.

        Returns:
            list[arcade.Sprite]: Overlapping collection sprites discovered.
        """
        colliding_sprite: list[arcade.Sprite] = (
            arcade.check_for_collision_with_lists(
                sprite=self.player_reference.sprite,
                sprite_lists=[self.pacgums_sprite_list,
                              self.super_pacgums_sprite_list]
            ))

        return colliding_sprite

    def _check_for_collisions(
        self, entity: Entity, direction: tuple[float, float]
    ) -> bool:
        """Determines if a prospective step intersects with a layout wall
        coordinate.

        Args:
            entity (Entity): Testing entity instance.
            direction (tuple[float, float]): Proposed directional movement
            offset.

        Returns:
            bool: True if destination grid is open and unblocked.
        """
        conv_x, conv_y = self.calculator.get_pixel_to_grid_entity(entity)

        # Inverted Y (because Arcade Y=0 is bottom right)
        wall_x: int = int(conv_x + direction[0])
        wall_y: int = int(conv_y - direction[1])

        # Check if the destination is open
        if self.maze_bitmap.get((wall_x, wall_y), 1) == 0:
            return True
        return False

    def _snap_to_grid(
        self, entity: Entity, direction: tuple[float, float]
    ) -> None:
        """Forces an entity's coordinates onto the center axis of its path.

        Args:
            entity (Entity): Target actor object structure.
            direction (tuple[float, float]): Dimensional vector tracking
            heading.
        """
        # Calculate the exact center of the current tile
        center_x: int = int((
            ((entity.x - self.offset_x) // self.tile_size)
            * self.tile_size + (self.tile_size / 2) + self.offset_x))
        center_y: int = int((
            ((entity.y - self.offset_y) // self.tile_size)
            * self.tile_size + (self.tile_size / 2) + self.offset_y))

        # Lock the perpendicular axis
        if direction[0] == 0.0 and direction[1] != 0.0:
            # Vertical movement: lock X to the center of the column
            entity.x = center_x
        elif direction[0] == 0.0 and direction[1] != 0.0:
            # Horizontal movement: lock Y to the center of the row
            entity.y = center_y

    def _get_tile_center(self, entity: Entity) -> tuple[float, float]:
        """Calculates precise target grid center pixel coordinates for an
        actor.

        Args:
            entity (Entity): Inspected target engine instance.

        Returns:
            tuple[float, float]: True geometric midpoints (X, Y).
        """
        # Calculate X center
        logic_x = (entity.x - self.offset_x) // self.tile_size
        center_x = ((logic_x * self.tile_size) + (self.tile_size / 2) +
                    self.offset_x)

        # Calculate Y center
        logic_y = (entity.y - self.offset_y) // self.tile_size
        center_y = ((logic_y * self.tile_size) + (self.tile_size / 2) +
                    self.offset_y)

        return center_x, center_y
