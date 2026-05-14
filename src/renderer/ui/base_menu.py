# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  base_menu.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:35:18 by roandrie        #+#    #+#               #
#  Updated: 2026/05/14 19:40:32 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from .base_button import BaseButton


class BaseMenu(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        self.button_list: arcade.SpriteList = arcade.SpriteList()

    def on_draw(self) -> None:
        self.clear()
        self.button_list.draw()

    def on_mouse_motion(
        self, x: float, y: float, _dx: float, _dy: float
    ) -> None:

        for button in self.button_list:
            if isinstance(button, BaseButton):
                button.check_hover(x, y)

    def on_mouse_press(
        self, x: float, y: float, button: int, _modifiers: int
    ) -> None:

        if button == arcade.MOUSE_BUTTON_LEFT:
            for ui_button in self.button_list:
                if (isinstance(ui_button, BaseButton) and
                        ui_button.collides_with_point((x, y))):

                    ui_button.on_click()
