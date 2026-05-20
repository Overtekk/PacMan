# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  highscores_screen.py                              :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/18 12:52:32 by anacharp        #+#    #+#               #
#  Updated: 2026/05/20 09:19:51 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from pathlib import Path
from .base_menu import BaseMenu
from .base_button import BaseButton
from src.leaderboard.extract_leaderboard import extract_leaderboard


class Highscores(BaseButton):
    def __init__(
            self,
            center_x: float,
            center_y: float,
            sprite_path: Path,
            parent_view: arcade.View
    ) -> None:

        super().__init__(
            center_x=center_x,
            center_y=center_y,
            sprite_path=sprite_path,
            parent_view=parent_view
        )

    def on_click(self) -> None:
        from src.renderer.ui.main_menu import MainMenu
        menu = MainMenu()

        if self.parent_view.window:
            self.parent_view.window.show_view(menu)


class HighscoresScreen(BaseMenu):
    def __init__(self) -> None:
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)

    def build_ui(self) -> None:
        highscores = Highscores(
            center_x=640,
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
            text = arcade.Text(text=string, x=540, y=y,
                               color=arcade.color.WHITE, font_size=15)
            self.text_lst.append(text)
            y -= 50
