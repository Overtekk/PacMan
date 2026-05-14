# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  main_menu.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:37:31 by roandrie        #+#    #+#               #
#  Updated: 2026/05/14 21:40:41 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from pathlib import Path

from .base_menu import BaseMenu
from .base_button import BaseButton
from src.game_engine import GameEngine


class PlayButton(BaseButton):
    def __init__(
        self, center_x: float,
        center_y: float,
        sprite_path: Path,
        parent_view: arcade.View
    ) -> None:

        BaseButton.__init__(
            self,
            center_x=center_x,
            center_y=center_y,
            sprite_path=sprite_path,
            parent_view=parent_view
        )

    def on_click(self) -> None:
        game_session = GameEngine()
        game_session.setup()

        if self.parent_view.window:
            self.parent_view.window.show_view(game_session)


class MainMenu(BaseMenu):
    def __init__(self) -> None:
        super().__init__()

        arcade.set_background_color(arcade.color.BLACK)

        play_button = PlayButton(
            center_x=400,
            center_y=300,
            sprite_path="",
            parent_view=self
        )

        self.button_list.append(play_button)
