# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_engine.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:20:06 by roandrie        #+#    #+#               #
#  Updated: 2026/05/25 19:15:27 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any

import arcade

from src.renderer import GameRenderer
from src.game_engine.gamestate_manager import GameStateManager
from src.config import GameConfig
from .level_manager import LevelManager
from .collision_manager import CollisionManager
from .game_settings import GameState
from src.utils import print_log

# Number of seconds before the level start (player and enemies movement) or
# between lose
TIMER_LEVEL_START: float = 3.0


class GameEngine(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        self.config: GameConfig = self.window.game_config
        self.debug_mode: bool = self.window.debug_mode

        # Instanciate class instance
        self.game_renderer = GameRenderer()
        self.game_state = GameState.SETUP
        self.state_manager = GameStateManager(self.window, parent_view=self)
        self.level_manager = LevelManager(game_window=self.window)

        self._first_launch: bool = True

    def on_update(self, delta_time: float) -> None:
        self.game_renderer.update(delta_time)

        if self.game_state == GameState.SETUP:
            pass

        elif self.game_state == GameState.STARTING:
            self._timer_start(delta_time)

        elif self.game_state == GameState.PAUSE:
            pass

        elif self.game_state == GameState.PLAYING:
            # Check for collisions
            player_died: bool = self.coll_manager.update()

            if player_died:
                self.game_state = GameState.RESPAWN

            else:
                # Update all entities
                self.player.update(delta_time)

                for enemy_obj in self.level_manager.enemies_list.values():
                    enemy_obj.update(delta_time)

        elif self.game_state == GameState.RESPAWN:
            self._reset_entities(self.player)

            for enemy_obj in self.level_manager.enemies_list.values():
                enemy_obj.respawn()
                self._reset_entities(enemy_obj)

            self._current_timer_start = TIMER_LEVEL_START
            self.game_state = GameState.STARTING

        elif self.game_state == GameState.FINISH:
            pass

    def on_draw(self) -> None:
        self.clear()

        # Render the game
        self.game_renderer.draw()

    def on_show_view(self) -> None:
        # Clear the screen
        self.clear()

        # Call the setup method
        if self._first_launch:
            self._first_launch = False
            self.setup(first_instance=True)

        else:
            self.game_renderer.draw()

    def setup(self, first_instance: bool = False) -> None:
        if first_instance:
            self.state_manager.current_level_index = 0
            self.state_manager.score = 0

        # Reset game data
        self.state_manager.live = self.config.live
        self.state_manager.time_left = self.config.level_max_time

        # Create the level
        level_index: int = self.state_manager.current_level_index

        level: list[list[int]] = self.level_manager.create_level(
            maze_width=self.config.level[level_index].width,
            maze_height=self.config.level[level_index].height,
            first_instance=first_instance
        )

        # Render the maze
        self.game_renderer.wall_generator(level)

        # -------------TEMP

        self._setup_entities()

        # Instanciate the Collision Manager
        self.coll_manager: CollisionManager = CollisionManager(
            self.player, self.level_manager.enemies_list,
            self.enemies_sprite_list,
            self.level_manager.maze_bitmap,
            self.level_manager.calculator,
            self.state_manager,
            self.debug_mode
        )

        self._current_timer_start: float = TIMER_LEVEL_START
        self.game_state = GameState.STARTING

    def on_key_press(self, symbol: int, _modifiers: int) -> None:
        if symbol == arcade.key.UP or symbol == arcade.key.W:
            self.player._next_direction = (0, 1)

        elif symbol == arcade.key.DOWN or symbol == arcade.key.S:
            self.player._next_direction = (0, -1)

        elif symbol == arcade.key.LEFT or symbol == arcade.key.A:
            self.player._next_direction = (-1, 0)

        elif symbol == arcade.key.RIGHT or symbol == arcade.key.D:
            self.player._next_direction = (1, 0)

        elif self.debug_mode:
            if symbol == arcade.key.R and self.game_state == GameState.PLAYING:
                print_log("Debug: activate died!")
                self.coll_manager.debug_force_death = True

    # :---------------:
    #  PRIVATE METHODS
    # :---------------:

    def _timer_start(self, delta_time: float) -> None:
        # Save the current second
        previous_second: int = int(self._current_timer_start) + 1

        # Time elapsed
        self._current_timer_start -= delta_time

        # New second
        current_second: int = int(self._current_timer_start) + 1

        if current_second != previous_second and current_second > 0:
            if self.debug_mode:
                print(f"Game starting in: {current_second}")
            self.game_renderer.trigger_time_text(str(current_second))

        if self._current_timer_start <= 0.0:
            if self.debug_mode:
                print_log("Game started")
            self.game_renderer.trigger_time_text("GO!", True)

            self._setup_start()

    def _setup_entities(self) -> None:

        # Create a reference of all movable entities
        self.player = self.level_manager.player
        self.cat_enemy = self.level_manager.enemies_list["cat_enemy"]
        self.fox_enemy = self.level_manager.enemies_list["fox_enemy"]
        self.rat_enemy = self.level_manager.enemies_list["rat_enemy"]
        self.dog_enemy = self.level_manager.enemies_list["dog_enemy"]

        # -------------------------- TEMP
        t, p = self.level_manager.factory.get_pixel_coordinates(12, 5)

        from src.entity.logics.StateMachine import EnemyState

        self.dog_enemy.x = t
        self.dog_enemy.y = p

        self.dog_enemy.mode = EnemyState.RESPAWN

        # List containing all enemies sprites
        self.enemies_sprite_list: arcade.SpriteList[Any] = arcade.SpriteList()

        # Enemy rendering
        for enemy_obj in self.level_manager.enemies_list.values():
            # Store the sprite
            self.enemies_sprite_list.append(enemy_obj.sprite)
            # Render the sprites on screen
            self.game_renderer.setup_entities(enemy_obj.sprite)

        # Render the player
        self.game_renderer.setup_entities(self.player.sprite)

    def _setup_start(self) -> None:
        self.game_state = GameState.PLAYING

        # Authorize movement
        self.player._can_move = True

        for enemy_obj in self.level_manager.enemies_list.values():
            enemy_obj._can_move = True

    def _reset_entities(self, entity: Any) -> None:
        # Block movement
        entity._can_move = False

        # Reset positions
        entity._current_direction = (0.0, 0.0)
        entity._next_direction = (0.0, 0.0)

        # Reset sprites direction
        entity.reset_animation()
