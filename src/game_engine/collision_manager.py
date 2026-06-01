# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  collision_manager.py                              :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 20:04:13 by roandrie        #+#    #+#               #
#  Updated: 2026/06/01 13:36:08 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any

import arcade
from src import game_config

from src.entity import Entity, Player, Movable
from .gamestate_manager import GameStateManager
from src.utils import print_log, SuperCalculator
from .level_manager import LevelManager


class CollisionManager():
    def __init__(
        self,
        player_reference: Player,
        enemies_reference: list[str, Any],
        enemies_sprite_list: arcade.SpriteList,
        pacgums_sprite_list: arcade.SpriteList,
        super_pacgums_sprite_list: arcade.SpriteList,
        maze_bitmap: dict[tuple[int, int], str],
        calculator: SuperCalculator,
        state_manager: GameStateManager
    ) -> None:

        self.player_reference = player_reference
        self.enemies_reference = enemies_reference
        self.enemies_sprite_list = enemies_sprite_list
        self.pacgums_sprite_list = pacgums_sprite_list
        self.super_pacgums_sprite_list = super_pacgums_sprite_list
        self.maze_bitmap = maze_bitmap
        self.state_manager = state_manager
        self.calculator = calculator

        self.offset_x: float = self.calculator.maze_offset_x
        self.offset_y: float = self.calculator.maze_offset_y
        self.tile_size: float = self.calculator.maze_tile_size

        # DEBUG
        self.debug_force_death: bool = False

    def update(self, delta_time: float) -> bool | str:
        # Check collisions for the player with walls
        self._entity_collisions_logic(self.player_reference)

        # Check collisions for enemies with walls
        for enemy in self.enemies_reference.values():
            self._entity_collisions_logic(enemy)

        # Check for collision between player/enemy
        enemy_colliding: list[arcade.SpriteType] = (
            self._check_collisions_with_enemy()
        )

        # Debug force died
        if self.debug_force_death:
            self.debug_force_death = False
            self.state_manager.live -= 1
            self.player_reference.die(delta_time)

            if game_config.debug_mode:
                print_log(
                    f"Player died! Life remaining: {self.state_manager.live}")
            return True

        # If player is invincible, check if enemy can be eaten
        elif (self.player_reference.invincible or
                self.state_manager.parent_view.is_cheat_invincible_active):
            for enemy in enemy_colliding:
                if enemy.parent.is_edible and not enemy.parent.died:

                    enemy.parent.die(delta_time)
                    self.state_manager.score += (
                        self.state_manager.config.ghost_points)

                    if game_config.debug_mode:
                        print_log(f"{enemy.parent} died!")

        # Check if player have encountered an enemy
        elif len(enemy_colliding) > 0:
            for enemy in enemy_colliding:
                if not enemy.parent._died:

                    self.debug_force_death = False
                    self.state_manager.live -= 1

                    if game_config.debug_mode:
                        print_log(
                            "Player died! Life remaining: "
                            f"{self.state_manager.live}"
                        )

                    self.player_reference.die(delta_time)
                    return True

        # Check for collision between player/collectibles
        list_colliding: list[arcade.SpriteType] = (
            self._check_collision_with_collectibles()
        )
        if len(list_colliding) > 0:
            for obj in list_colliding:
                print_log(f"+{obj.parent.score} points.")
                # Increase score
                self.state_manager.score += obj.parent.score

                # Activate power
                if hasattr(obj.parent, 'activate_power'):

                    if game_config.debug_mode:
                        print_log("Activate SUPERPACGUM")

                    obj.parent.activate_power(
                        self.player_reference, self.enemies_reference
                    )

                # Remove the sprite
                obj.kill()

        if len(self.pacgums_sprite_list) == 0:
            for sprite in self.super_pacgums_sprite_list:
                sprite.remove_from_sprite_lists()
            return "level_complete"

        return False

    # :---------------:
    #  PRIVATE METHODS
    # :---------------:

    def _entity_collisions_logic(self, entity: Movable) -> None:
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

    def _check_collisions_with_enemy(self) -> list[arcade.SpriteType]:
        colliding_sprite: list[arcade.SpriteType] = (
            arcade.check_for_collision_with_list(
                self.player_reference.sprite,
                sprite_list=self.enemies_sprite_list
            ))

        return colliding_sprite

    def _check_collision_with_collectibles(self) -> list[arcade.SpriteType]:
        colliding_sprite: list[arcade.SpriteType] = (
            arcade.check_for_collision_with_lists(
                sprite=self.player_reference.sprite,
                sprite_lists=[self.pacgums_sprite_list,
                              self.super_pacgums_sprite_list]
            ))

        return colliding_sprite

    def _check_for_collisions(
        self, entity: Entity, direction: tuple[float, float]
    ) -> bool:
        conv_x, conv_y = self.calculator.get_pixel_to_grid_entity(entity)

        # Inverted Y (because Arcade Y=0 is bottom right)
        wall_x: int = conv_x + direction[0]
        wall_y: int = conv_y - direction[1]

        # Check if the destination is open
        if self.maze_bitmap.get((wall_x, wall_y), 1) == 0:
            return True
        return False

    def _snap_to_grid(
        self, entity: Entity, direction: tuple[float, float]
    ) -> None:
        # Calculate the exact center of the current tile
        center_x: int = (((entity.x - self.offset_x) // self.tile_size) *
                         self.tile_size + (self.tile_size / 2) + self.offset_x)
        center_y: int = (((entity.y - self.offset_y) // self.tile_size) *
                         self.tile_size + (self.tile_size / 2) + self.offset_y)

        # Lock the perpendicular axis
        if direction == 0.0 and direction != 0.0:
            # Vertical movement: lock X to the center of the column
            entity.x = center_x
        elif direction == 0.0 and direction != 0.0:
            # Horizontal movement: lock Y to the center of the row
            entity.y = center_y

    def _get_tile_center(self, entity: Entity) -> tuple[float, float]:
        # Calculate X center
        logic_x = (entity.x - self.offset_x) // self.tile_size
        center_x = ((logic_x * self.tile_size) + (self.tile_size / 2) +
                    self.offset_x)

        # Calculate Y center
        logic_y = (entity.y - self.offset_y) // self.tile_size
        center_y = ((logic_y * self.tile_size) + (self.tile_size / 2) +
                    self.offset_y)

        return center_x, center_y
