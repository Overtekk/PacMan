# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  intro_screen.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/05 11:10:24 by roandrie        #+#    #+#               #
#  Updated: 2026/06/05 15:17:40 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from pathlib import Path

from .base_menu import BaseMenu
from src.renderer.screen_settings import ScreenSettings


class CallBackground(arcade.Sprite):
    def __init__(
        self, center_x: float, center_y: float, sprite_path: Path,
        scale: float = 1.5, anchor_x: str = 'left',
        anchor_y: str = 'top'
    ) -> None:

        super().__init__(
            path_or_texture=sprite_path, scale=scale, anchor_x=anchor_x,
            anchor_y=anchor_y
        )

        self.center_x = center_x
        self.center_y = center_y


class IntroScreen(BaseMenu):
    def __init__(self, previous_view: arcade.View) -> None:
        super().__init__()

        self.previous_view = previous_view

        # Sprites list
        self.fixed_sprites: list[arcade.Sprite] = arcade.SpriteList()
        self.sprites_lst: dict[str, arcade.Sprite] = {}

        # Dialogues
        self.dialogue_list: list[str] = [
            'Ceci est le premier test',
            'ceci est le deuxieme test'
        ]

        self.dialogue_index: int = 0

        # - Private variables -
        self._dialogue_text: str = ""
        self._index: int = 0
        self._timer: float = 0.0
        self._txt_show_speed: float = 0.00
        self._pause: bool = False

    def build_ui(self) -> None:
        # Create the background screen
        self._create_ui_elements(                                                 )

        self.text: arcade.Text = arcade.Text(
            "",
            x=ScreenSettings.WIDTH // 2, y=(ScreenSettings.HEIGHT // 2),
            color=arcade.color.WHITE_SMOKE, font_size=35,
            font_name='fibberish', align='center', anchor_x='center',
            anchor_y='center'
        )

        self._load_dialogue(0)

    def on_update(self, delta_time) -> None:
        self._timer += delta_time

        if (self._timer > self._txt_show_speed and
                self._index < len(self._dialogue_text)):
            self._index += 1
            self._timer -= self._txt_show_speed
            self.text.text = self._dialogue_text[0:self._index]

    def on_key_press(self, symbol: int, _modifiers: int) -> None:
        if symbol == arcade.key.SPACE and not self._pause:
            if self._index < len(self._dialogue_text):
                self._index = len(self._dialogue_text)
                self.text.text = self._dialogue_text
            else:
                self.dialogue_index += 1
                if len(self.dialogue_list) > self.dialogue_index:
                    self._load_dialogue(self.dialogue_index)
                else:
                    pass # leave

    def on_draw(self) -> None:
        self.clear()

        # Draw background
        self.fixed_sprites.draw()

        self.text.draw()

    # :---------------:
    #  PRIVATE METHODS
    # :---------------:

    def _load_dialogue(
        self, dialogue_index: int, text_speed: float = 0.06
    ) -> None:

        self._dialogue_text = self.dialogue_list[dialogue_index]
        self.text.text = ""
        self._index = 0
        self._timer = 0
        self._txt_show_speed = text_speed

    def _create_ui_elements(self) -> None:
        background = CallBackground(
            ScreenSettings.WIDTH // 2, (ScreenSettings.HEIGHT // 2) + 200,
            self.window.asset_manager.textures['call_background'], scale=0.3
        )

        self.fixed_sprites.append(background)
