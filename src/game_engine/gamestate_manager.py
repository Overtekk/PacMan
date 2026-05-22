# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  gamestate_manager.py                              :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 20:03:38 by roandrie        #+#    #+#               #
#  Updated: 2026/05/22 22:51:19 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any

import arcade


class GameStateManager():
    def __init__(
        self,
        game_window: arcade.Window,
        parent_view: arcade.View
    ) -> None:

        self.window = game_window
        self.config = game_window.game_config
        self.parent_view = parent_view

        # Init the game data
        self.game_data: dict[str, Any] = {
            "current_level_index": 0,
            "live": self.config.live,
            "score": 0,
            "time_left": self.config.level_max_time
        }

    @property
    def live(self) -> int:
        return self.game_data["live"]

    @live.setter
    def live(self, new_value: int) -> None:
        # SECURITY CHECK
        if new_value < 0:
            new_value = 0

        self.game_data["live"] = new_value

        # DEATH TRIGGER
        if self.game_data["live"] <= 0:
            if self.window:
                from src.renderer.ui.game_over_screen import GameOverScreen

                self.window.show_view(GameOverScreen)

    @property
    def score(self) -> float:
        return self.game_data["score"]

    @score.setter
    def score(self, new_value: int) -> None:
        # SECURITY CHECK
        if new_value < 0:
            new_value = 0

        self.game_data["score"] = new_value

    @property
    def time_left(self) -> float:
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
        if self.game_data["time_left"] <= 0:
            self.lives -= 1

    @property
    def current_level_index(self) -> int:
        return self.game_data["current_level_index"]

    @current_level_index.setter
    def current_level_index(self, new_index: int) -> None:
        self.game_data["current_level_index"] += new_index

        # TRIGGER VICTORY SCREEN
        if self.game_data["current_level_index"] > len(self.config.level):
            from src.renderer.ui.finish_screen import FinishScreen

            self.window.show(FinishScreen)

    def on_key_press(self, symbol: int, _modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            if self.window:
                from src.renderer.ui.pause_menu import PauseMenu

                self.window.show_view(PauseMenu(
                        previous_view=self.parent_view))

    # stock data : score, lives, current_level, timer
