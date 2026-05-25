# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_engine.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:20:06 by roandrie        #+#    #+#               #
#  Updated: 2026/05/25 10:45:50 by roandrie        ###   ########.fr        #
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

# Number of seconds before the level start (player and enemies movement) or
# between lose
TIMER_LEVEL_START: float = 3.0


class GameEngine(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        self.config: GameConfig = self.window.game_config

        # Instanciate class instance
        self.game_renderer = GameRenderer()
        self.game_state = GameState.SETUP
        self.state_manager = GameStateManager(self.window, parent_view=self)
        self.level_manager = LevelManager(game_window=self.window)

        self._first_launch: bool = True
        self._game_paused: bool = False

    @property
    def game_paused(self) -> bool:
        return self._game_paused

    @game_paused.setter
    def game_paused(self, new_value: bool) -> None:
        self._game_paused = new_value

    def on_update(self, delta_time: float) -> None:
        if self._game_paused:
            return

        if self.game_state == GameState.SETUP:
            pass

        elif self.game_state == GameState.STARTING:
            self._timer_start(delta_time)

        elif self.game_state == GameState.PLAYING:
            # Check for collisions
            self.coll_manager.update()

            # Update all entities
            self.player.update(delta_time)

            for enemy_obj in self.level_manager.enemies_list.values():
                enemy_obj.update(delta_time)

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

        self._setup_entities()

        # Instanciate the Collision Manager
        self.coll_manager: CollisionManager = CollisionManager(
            self.player, self.level_manager.enemies_list,
            self.enemies_sprite_list,
            self.level_manager.byte_maze,
            self.level_manager.factory.offset_x,
            self.level_manager.factory.offset_y,
            self.level_manager.factory.tile_size,
            self.level_manager.maze_height,
            self.state_manager
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

        elif self.state_manager:
            self.state_manager.on_key_press(symbol, _modifiers)

    # :---------------:
    #  PRIVATE METHODS
    # :---------------:

    def _timer_start(self, delta_time: float) -> None:
        self._current_timer_start -= delta_time

        if self._current_timer_start > 0:
            return

        self._setup_start()

    def _setup_entities(self) -> None:

        # Create a reference of all movable entities
        self.player = self.level_manager.player
        self.cat_enemy = self.level_manager.enemies_list["cat_enemy"]
        self.fox_enemy = self.level_manager.enemies_list["fox_enemy"]
        self.rat_enemy = self.level_manager.enemies_list["rat_enemy"]
        self.dog_enemy = self.level_manager.enemies_list["dog_enemy"]

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
        self.rat_enemy._can_move = True
