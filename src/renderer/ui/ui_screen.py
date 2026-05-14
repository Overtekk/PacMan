# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  ui_screen.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:44:37 by roandrie        #+#    #+#               #
#  Updated: 2026/05/14 19:44:40 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from pathlib import Path

from .base_menu import BaseMenu
from .base_button import BaseButton


class UIScreen(BaseMenu):
    def __init__(self) -> None:
        super().__init__()

        arcade.set_background_color(arcade.color.BLACK)
