# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  base_menu.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:35:18 by roandrie        #+#    #+#               #
#  Updated: 2026/06/12 12:16:55 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from abc import ABC, abstractmethod

from .base_button import BaseButton

from src.audio.AudioManager import AudioManager


class BaseMenu(arcade.View, ABC):
    """Abstract class establishing rendering pipelines and layouts for
    application menus.

    Intercepts framework mouse ticks and transfers operational bounds to
    structural UI lists.
    """
    def __init__(self) -> None:
        """Initializes display registries and links central audio players."""
        super().__init__()
        self.highscore_filename: str = ""
        self.button_list: arcade.SpriteList[arcade.Sprite]
        self.button_list = arcade.SpriteList()
        self.text_lst: list[arcade.Text] = []

        self.audio_manager: AudioManager | None = self.window.audio_player

    def on_draw(self) -> None:
        """Clears frame structures and renders localized lists and elements."""
        self.clear()
        self.button_list.draw()
        for txt in self.text_lst:
            txt.draw()

    def on_mouse_motion(
        self, x: float, y: float, _dx: float, _dy: float
    ) -> None:
        """Triggers intersection queries on menu assets when the pointer moves.

        Args:
            x (float): Core application space viewport horizontal coordinate.
            y (float): Core application space viewport vertical coordinate.
            _dx (float): Delta movement step parameter (unused).
            _dy (float): Delta movement step parameter (unused).
        """

        for button in self.button_list:
            if isinstance(button, BaseButton):
                button.check_hover(x, y)

    def on_mouse_press(
        self, x: float, y: float, button: int, _modifiers: int
    ) -> None:
        """Dispatches click commands to buttons matching structural
        intersection rules.

        Args:
            x (float): Core application space viewport horizontal coordinate.
            y (float): Core application space viewport vertical coordinate.
            button (int): Framework tracking flag specifying which input key
            was pressed.
            _modifiers (int): Bitwise map showing active modifier keys
            (unused).
        """
        self.last_click_x = x
        self.last_click_y = y

        if button == arcade.MOUSE_BUTTON_LEFT:
            for ui_button in self.button_list:
                if (isinstance(ui_button, BaseButton) and
                        ui_button.collides_with_point((x, y))):

                    if self.audio_manager:
                        self.audio_manager.play_sound('click1', 1.0)

                    ui_button.on_click()

    def on_show_view(self) -> None:
        """
        Wipes lingering elements and runs the main user interface builders.
        """
        self.text_lst.clear()
        self.button_list.clear()

        self.build_ui()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """Optional keyboard handler override hook."""
        pass

    @abstractmethod
    def build_ui(self) -> None:
        """
        Abstract method designated to instantiate menu layout lists and button
        arrays.
        """
        pass
