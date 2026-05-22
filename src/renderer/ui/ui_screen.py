# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  ui_screen.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:44:37 by roandrie        #+#    #+#               #
#  Updated: 2026/05/22 15:02:23 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from pathlib import Path

from .base_menu import BaseMenu
from .base_button import BaseButton
from src.renderer.screen_settings import ScreenSettings


class DisplayLives(arcade.Sprite):
    def __init__(
        self,
        center_x: float,
        center_y: float,
        sprite_path: Path,
        parent_view: arcade.View,
        scale: float = 2.0,
        anchor_x="center"
    ) -> None:

        super().__init__(
            path_or_texture=sprite_path,
            scale=scale,
            anchor_x=anchor_x
        )

        self.center_x = center_x
        self.center_y = center_y

        self.parent_view = parent_view


class UIScreen(BaseMenu):
    def __init__(self, score: int, time: float, lives: int) -> None:
        super().__init__()
        self.score = score
        self.time = time
        image = arcade.get_image()
        self.background = arcade.Texture(image)

    def build_ui(self) -> None:
        lives = DisplayLives(
            center_x=1,
            center_y=1,
            sprite_path=(
                self.window.asset_manager.textures["life"]
            ),
            parent_view=self
        )
        display_score = arcade.Text(text=self.score,
                                    x=ScreenSettings.WIDTH -50,
                                    y=ScreenSettings.HEIGHT - 50,
                                    color=arcade.color.WHITE, font_size=40,
                                    font_name="Press Start 2P")
        self.text_lst.append(display_score)
        display_time = arcade.Text(text=self.time, x=ScreenSettings.WIDTH -100,
                                   y=1,
                                   color=arcade.color.YELLOW,
                                   font_size=40, font_name="Press Start 2P")
        self.text_lst.append(display_time)
        self.button_list.append(lives)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            from src.renderer.ui.main_menu import MainMenu
            if self.window:
                self.window.show_view(MainMenu())
        if symbol == arcade.key.SPACE:
            if self.window:
                self.window.show_view(self.previous_view)

    def on_draw(self):
        self.clear()
        self.button_list.draw()
        for txt in self.text_lst:
            txt.draw()
