# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  highscores_screen.py                              :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/18 12:52:32 by anacharp        #+#    #+#               #
#  Updated: 2026/06/04 15:52:40 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from pathlib import Path
from .base_menu import BaseMenu
from .base_button import BaseButton
from src.leaderboard.extract_leaderboard import extract_leaderboard
from src.renderer.screen_settings import ScreenSettings


class HighscoresButton(BaseButton):
    def __init__(
            self,
            center_x: float,
            center_y: float,
            sprite_path: Path,
            parent_view: arcade.View,
            anchor_x: str = "center"
    ) -> None:

        super().__init__(
            sprite_path=sprite_path,
            center_x=center_x,
            center_y=center_y,
            parent_view=parent_view,
        )
        anchor_x = anchor_x

    def on_click(self) -> None:
        if self.parent_view.window:
            self.parent_view.window.show_view(self.parent_view.previous_view)


class HighscoresScreen(BaseMenu):
    def __init__(self, previous_view: arcade.View) -> None:
        super().__init__()
        self.previous_view = previous_view

        # Initialise the beach background
        self.background = arcade.load_texture(
            self.window.asset_manager.textures["ocean"]
        )

        self.y = 0

    def build_ui(self) -> None:
        # Create highscore button to go back on main menu
        self.highscores = HighscoresButton(
            center_x=ScreenSettings.WIDTH // 2, center_y=600,
            sprite_path=(
                self.window.asset_manager.textures["highscores_button"]),
            parent_view=self)
        self.button_list.append(self.highscores)

        # Put the leaderboard content on a text list
        file_content = extract_leaderboard(
            self.window.game_config.highscore_filename)
        split_content = file_content.split("\n")
        y = 520
        for string in split_content:
            if string.startswith("CHEATER"):
                string = string.strip("CHEATER ")
                text = arcade.Text(text=string, x=ScreenSettings.WIDTH // 2,
                                   y=y, color=arcade.color.RED, font_size=15,
                                   font_name="press Start 2P",
                                   anchor_x="center")
            else:
                text = arcade.Text(text=string, x=ScreenSettings.WIDTH // 2,
                                   y=y, color=arcade.color.WHITE, font_size=15,
                                   font_name="press Start 2P",
                                   anchor_x="center")
            self.text_lst.append(text)
            y -= 50

    def on_key_press(self, symbol: int, _modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            if self.window:
                self.window.show_view(self.previous_view)

        if symbol == arcade.key.DOWN:
            self.y += 1
        if symbol == arcade.key.UP:
            self.y += 1

        if self.y > 1:
            self.y = 0
        if self.y == 1:
            self.highscores.check_hover(self.highscores.center_x,
                                          self.highscores.center_y)
        else:
            self.highscores.color = arcade.color.WHITE
        if symbol == arcade.key.ENTER or symbol == arcade.key.SPACE:
            if self.y == 1:
                self.highscores.on_click()

    def on_draw(self) -> None:
        self.clear()
        # Draw the beach background
        arcade.draw_texture_rect(
            texture=self.background,
            rect=arcade.LBWH(0, 0, ScreenSettings.WIDTH, ScreenSettings.HEIGHT)
        )

        # Draw highscore button and text (leaderboard content)
        self.button_list.draw()
        for txt in self.text_lst:
            txt.draw()

    def on_update(self, delta_time: float) -> None:
        # Update the highscore sprite to check if user touch it or not
        self.button_list.update()
        for sprite in self.button_list:
            if isinstance(sprite, HighscoresButton):
                sprite.on_update(delta_time)
