# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  main_menu.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:37:31 by roandrie        #+#    #+#               #
#  Updated: 2026/05/14 19:40:34 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from pathlib import Path

from .base_menu import BaseMenu
from .base_button import BaseButton


class PlayButton(BaseButton):
    def __init__(
        self, center_x: float, center_y: float, sprite_path: Path
    ) -> None:

        BaseButton.__init__(
            self, center_x=center_x, center_y=center_y, sprite_path=sprite_path
        )

    def on_click(self) -> None:
        pass


class MainMenu(BaseMenu):
    def __init__(self) -> None:
        super().__init__()

        arcade.set_background_color(arcade.color.BLACK)

        play_button = PlayButton(center_x=400, center_y=300)

        self.button_list.append(play_button)
