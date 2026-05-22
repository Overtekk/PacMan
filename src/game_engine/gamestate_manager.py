# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  gamestate_manager.py                              :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 20:03:38 by roandrie        #+#    #+#               #
#  Updated: 2026/05/22 21:11:17 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any

import arcade

from src.renderer.ui.pause_menu import PauseMenu


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
            "level": self.config.level[0],
            "lives": self.config.lives,
            "score": 0,
            "time_left": self.config.level_max_time
        }

    def on_key_press(self, symbol: int, _modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            if self.window:
                self.window.show_view(PauseMenu(
                        previous_view=self.parent_view))

    # stock data : score, lives, current_level, timer
