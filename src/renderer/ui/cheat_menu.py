# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  cheat_menu.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:43:51 by roandrie        #+#    #+#               #
#  Updated: 2026/05/19 15:12:45 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from pathlib import Path

from .base_menu import BaseMenu
from .base_button import BaseButton


class CheatMenu(BaseMenu):
    def __init__(self) -> None:
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)

    # def build_ui(self) -> None:
    #     x = x(
    #         center_x=640,
    #         center_y=600,
    #         sprite_path=(
    #             self.window.asset_manager.textures["x"]
    #         ),
    #         parent_view=self
    #     )
    #     self.button_list.append(x)


# Invincibility
# Ghost freeze
# Extra lives
# Increase speed
# next level
