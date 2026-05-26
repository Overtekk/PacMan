# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  base_menu.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:35:18 by roandrie        #+#    #+#               #
#  Updated: 2026/05/26 13:12:56 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from abc import ABC, abstractmethod

from .base_button import BaseButton


class BaseMenu(arcade.View, ABC):
    def __init__(self) -> None:
        super().__init__()
        self.highscore_filename = str
        self.button_list: arcade.SpriteList = arcade.SpriteList()
        self.text_lst: list[arcade.Text] = []

    def on_draw(self) -> None:
        self.clear()
        self.button_list.draw()
        for txt in self.text_lst:
            txt.draw()

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

    def on_show_view(self) -> None:
        self.text_lst.clear()
        self.button_list.clear()
        self.build_ui()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        pass

    @abstractmethod
    def build_ui(self) -> None:
        pass
