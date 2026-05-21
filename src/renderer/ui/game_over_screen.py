# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_over_screen.py                               :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:42:18 by roandrie        #+#    #+#               #
#  Updated: 2026/05/21 12:04:22 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from pathlib import Path
from src.renderer.screen_settings import ScreenSettings
from src.leaderboard.update_leaderboard import save_score_to_leaderboard

from .base_menu import BaseMenu
arcade.load_font("assets/fonts/PressStart2P.ttf")


class GameOver(arcade.Sprite):
    def __init__(
        self,
        center_x: float,
        center_y: float,
        sprite_path: Path,
        parent_view: arcade.View,
        scale: float = 1.5,
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


class GameOverScreen(BaseMenu):
    def __init__(self, score: str, filename: str) -> None:
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)
        self.player_name = ""
        self.score = score
        self.filename = filename

    def build_ui(self) -> None:
        game_over = GameOver(
            center_x=ScreenSettings.WIDTH // 2,
            center_y=560,
            sprite_path=(
                self.window.asset_manager.textures["game_over_screen"]
            ),
            parent_view=self
        )
        score = arcade.Text(text="SCORE", x=ScreenSettings.WIDTH // 2, y=360,
                                   color=arcade.color.WHITE, font_size=40,
                                   font_name="Press Start 2P",
                                   anchor_x="center")
        self.text_lst.append(score)
        nb = arcade.Text(text=self.score, x=ScreenSettings.WIDTH // 2, y=285,
                                   color=arcade.color.YELLOW, font_size=40,
                                   font_name="Press Start 2P",
                                   anchor_x="center")
        self.text_lst.append(nb)
        enter_name = arcade.Text(text="SAVE YOUR NAME",
                                 x=ScreenSettings.WIDTH // 2, y=180,
                                 color=arcade.color.WHITE, font_size=40,
                                 font_name="Press Start 2P",
                                 anchor_x="center")
        self.text_lst.append(enter_name)
        self.button_list.append(game_over)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if len(self.player_name) < 10:
            if arcade.key.A <= symbol <= arcade.key.Z:
                maj = modifiers & arcade.key.MOD_CAPSLOCK
                self.player_name += chr(symbol).upper() if maj else chr(symbol)
                text = arcade.Text(text=self.player_name,
                                   x=ScreenSettings.WIDTH // 3, y=110,
                                   color=arcade.color.YELLOW, font_size=40,
                                   font_name="Press Start 2P")
                self.text_lst.append(text)
        if len(self.player_name) > 0:
            if symbol == arcade.key.BACKSPACE:
                self.player_name = self.player_name[:-1]
                if self.text_lst:
                    self.text_lst.pop()
        if symbol == arcade.key.ENTER:
            from src.renderer.ui.main_menu import MainMenu
            if self.window:
                self.window.show_view(MainMenu())
            save_score_to_leaderboard(self.filename, self.player_name,
                                      float(self.score))

    def on_draw(self) -> None:
        self.clear()
        self.button_list.draw()
        for txt in self.text_lst:
            txt.draw()
