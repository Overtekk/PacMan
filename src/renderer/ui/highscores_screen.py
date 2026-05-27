# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  highscores_screen.py                              :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/18 12:52:32 by anacharp        #+#    #+#               #
#  Updated: 2026/05/27 15:56:36 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from pathlib import Path
from .base_menu import BaseMenu
from .base_button import BaseButton
from src.leaderboard.extract_leaderboard import extract_leaderboard
from src.renderer.screen_settings import ScreenSettings


class Highscores(BaseButton):
    def __init__(
            self,
            center_x: float,
            center_y: float,
            sprite_path: Path,
            parent_view: arcade.View,
            anchor_x="center"
    ) -> None:

        super().__init__(
            sprite_path=sprite_path,
            center_x=center_x,
            center_y=center_y,
            parent_view=parent_view,
        )
        anchor_x = anchor_x

    def on_click(self) -> None:
        from src.renderer.ui.main_menu import MainMenu
        menu = MainMenu()

        if self.parent_view.window:
            self.parent_view.window.show_view(menu)


class HighscoresScreen(BaseMenu):
    def __init__(self) -> None:
        super().__init__()
        self.background = arcade.load_texture(
            "assets/sprites/main_menu/ocean.png"
        )

    def build_ui(self) -> None:
        highscores = Highscores(
            center_x=ScreenSettings.WIDTH // 2,
            center_y=600,
            sprite_path=(
                self.window.asset_manager.textures["highscores_button"]
            ),
            parent_view=self
        )
        self.button_list.append(highscores)
        file_content = extract_leaderboard(
            self.window.game_config.highscore_filename)
        split_content = file_content.split("\n")
        y = 520
        for string in split_content:
            text = arcade.Text(text=string, x=ScreenSettings.WIDTH // 2, y=y,
                               color=arcade.color.WHITE, font_size=15,
                               font_name="press Start 2P", anchor_x="center")
            self.text_lst.append(text)
            y -= 50

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            from src.renderer.ui.main_menu import MainMenu
            if self.window:
                self.window.show_view(MainMenu())

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            texture=self.background,
            rect=arcade.LBWH(0, 0, ScreenSettings.WIDTH, ScreenSettings.HEIGHT)
        )
        self.button_list.draw()
        for txt in self.text_lst:
            txt.draw()

    def on_update(self, delta_time):
        self.button_list.update()
        for sprite in self.button_list:
            if isinstance(sprite, Highscores):
                sprite.on_update(delta_time)
