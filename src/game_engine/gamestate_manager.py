# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  gamestate_manager.py                              :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 20:03:38 by roandrie        #+#    #+#               #
#  Updated: 2026/05/20 11:08:52 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade
from src.renderer.ui.pause_menu import PauseMenu


class GameStateManager():
    def __init__(self, game_window: arcade.Window, parent_view: arcade.View) -> None:
        self.window = game_window
        self.config = game_window.game_config
        self.parent_view = parent_view
        # self.asset_manager = game_window.sprites_list

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            from src.renderer.ui.main_menu import MainMenu
            if self.window:
                self.window.show_view(MainMenu())
        if symbol == arcade.key.SPACE:
            if self.window:
                self.window.show_view(PauseMenu(previous_view=self.parent_view))

    # stock data : score, lives, current_level, timer
