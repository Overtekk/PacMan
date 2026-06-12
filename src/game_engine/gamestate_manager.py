# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  gamestate_manager.py                              :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 20:03:38 by roandrie        #+#    #+#               #
#  Updated: 2026/06/12 11:29:36 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any

import arcade

from src import game_config
from src.utils import print_log
from src.audio import AudioManager
from src.renderer.screen_settings import ScreenSettings


class GameStateManager():
    """Manages persistent game state and triggers screen transitions.

    Stores score, lives, time, and level index. Property setters handle
    boundary checks and automatically trigger game-over or victory screens
    when thresholds are reached.

    Attributes:
        window (arcade.Window): The main game window.
        config: The loaded game configuration.
        parent_view (arcade.View): The game engine view that owns this manager.
        audio_manager (AudioManager): Shared audio manager.
        game_data (dict[str, Any]): Internal storage for all game state values.
    """
    def __init__(
        self,
        game_window: arcade.Window,
        parent_view: arcade.View,
        audio_manager: AudioManager
    ) -> None:
        """Initialize the GameStateManager.

        Args:
            game_window (arcade.Window): The main game window.
            parent_view (arcade.View): The game engine view that owns this
            manager.
            audio_manager (AudioManager): Shared audio manager instance.
        """

        self.window = game_window
        self.config = game_window.game_config
        self.parent_view = parent_view
        self.audio_manager = audio_manager

        # Init the game data
        self.game_data: dict[str, Any] = {
            "current_level_index": 0,
            "live": self.config.live,
            "score": 0,
            "time_left": self.config.level_max_time
        }

    @property
    def live(self) -> Any:
        """
        int: Current number of lives. Triggers game over when it reaches 0.
        """
        return self.game_data["live"]

    @live.setter
    def live(self, new_value: int) -> None:
        # SECURITY CHECK
        if new_value < 0:
            new_value = 0

        self.game_data["live"] = new_value

        # DEATH TRIGGER
        if self.game_data["live"] <= 0:
            self.audio_manager.stop_all_sounds()
            self.audio_manager.play_sound('gameover', 1.0)

            if self.window:
                from src.renderer.ui.game_over_screen import GameOverScreen

                self.window.show_view(GameOverScreen(
                    score=self.score, filename=self.config.highscore_filename,
                    previous_view=self.parent_view
                ))

    @property
    def score(self) -> Any:
        """int: Current player score. Negative values are clamped to 0."""
        return self.game_data["score"]

    @score.setter
    def score(self, new_value: int) -> None:
        # SECURITY CHECK
        if new_value < 0:
            new_value = 0

        self.game_data["score"] = new_value

        if game_config.debug_mode:
            print_log(
                f"Score: {self.score}"
            )

    @property
    def time_left(self) -> Any:
        """float: Remaining time in seconds. Triggers a life loss at 0."""
        return self.game_data["time_left"]

    @time_left.setter
    def time_left(self, new_value: float, reset_timer: bool = False) -> None:
        # RESET THE TIMER TO DEFAULT VALUE
        if reset_timer:
            self.game_data["time_left"] = self.config.level_max_time

        # SECURITY CHECK
        if new_value < 0:
            new_value = 0

        self.game_data["time_left"] = new_value

        # TIMES OUT TRIGGER
        if int(self.game_data["time_left"]) <= 0:
            self.live -= 1

    @property
    def current_level_index(self) -> Any:
        """int: Index of the current level in the config level list."""
        return self.game_data["current_level_index"]

    @current_level_index.setter
    def current_level_index(self, new_index: int) -> None:
        self.game_data["current_level_index"] = new_index

    def win(self) -> None:
        """Trigger the victory sequence when all levels are completed.

        Resets the camera, stops all sounds, plays victory audio, and
        navigates to the FinishScreen. Protected against double-triggering.
        """
        # SECURITY
        if hasattr(self, "_win_triggered") and self._win_triggered:
            return
        self._win_triggered: bool = True

        # TRIGGER VICTORY SCREEN
        self.audio_manager.stop_all_sounds()
        self.audio_manager.play_sound('victory', 0.2)
        self.audio_manager.play_random_sound(
            ['gg1', 'gg2', 'gg3', 'gg4'], 1.0
        )

        if self.game_data["current_level_index"] >= len(self.config.level):
            from src.game_engine.game_engine import GameEngine
            if isinstance(self.parent_view, GameEngine):
                if hasattr(self.parent_view, 'game_renderer'):
                    self.parent_view.game_renderer.gui_camera.position = (
                        ScreenSettings.WIDTH//2,
                        ScreenSettings.HEIGHT//2)
                    self.parent_view.game_renderer.gui_camera.zoom = 1.0
                    self.parent_view.game_renderer.draw()

            from src.renderer.ui.finish_screen import FinishScreen
            self.window.show_view(FinishScreen(
                score=self.score,
                filename=self.config.highscore_filename,
                previous_view=self.parent_view))

    def pause_game(self) -> None:
        """Pause the game and show the pause menu overlay."""
        if self.window:
            from src.renderer.ui.pause_menu import PauseMenu
            self.window.show_view(PauseMenu(previous_view=self.parent_view))
