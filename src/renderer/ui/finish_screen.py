# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  finish_screen.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:43:32 by roandrie        #+#    #+#               #
#  Updated: 2026/05/22 10:51:59 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from src.renderer.screen_settings import ScreenSettings
from pathlib import Path
from src.leaderboard.update_leaderboard import save_score_to_leaderboard

from .base_menu import BaseMenu


class PacmanVictory(arcade.Sprite):
    def __init__(
        self,
        center_x: float,
        center_y: float,
        sprite_path: Path,
        parent_view: arcade.View,
        scale: float = 2.2,
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


class Victory(arcade.Sprite):
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


class FinishScreen(BaseMenu):
    def __init__(self, score: str, filename: str,
                 previous_view: arcade.View) -> None:
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)
        self.player_name = ""
        self.score = score
        self.filename = filename
        self.previous_view = previous_view
        image = arcade.get_image()
        self.background = arcade.Texture(image)

    def build_ui(self) -> None:
        victory = Victory(
            center_x=ScreenSettings.WIDTH // 2,
            center_y=580,
            sprite_path=(
                self.window.asset_manager.textures["victory_screen"]
            ),
            parent_view=self
        )
        pacman = PacmanVictory(
            center_x=300,
            center_y=400,
            sprite_path=(
                self.window.asset_manager.textures["pacman_victory"]
            ),
            parent_view=self
        )
        score = arcade.Text(text="SCORE", x=ScreenSettings.WIDTH // 2, y=410,
                                   color=arcade.color.WHITE, font_size=40,
                                   font_name="Press Start 2P",
                                   anchor_x="center")
        self.text_lst.append(score)
        nb = arcade.Text(text=self.score, x=ScreenSettings.WIDTH // 2, y=335,
                                   color=arcade.color.YELLOW, font_size=40,
                                   font_name="Press Start 2P",
                                   anchor_x="center")
        self.text_lst.append(nb)
        enter_name = arcade.Text(text="SAVE YOUR NAME",
                                 x=ScreenSettings.WIDTH // 2, y=230,
                                 color=arcade.color.WHITE, font_size=40,
                                 font_name="Press Start 2P",
                                 anchor_x="center")
        self.text_lst.append(enter_name)
        self.button_list.append(victory)
        self.button_list.append(pacman)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if len(self.player_name) < 10:
            if arcade.key.A <= symbol <= arcade.key.Z:
                maj = modifiers & arcade.key.MOD_CAPSLOCK
                self.player_name += chr(symbol).upper() if maj else chr(symbol)
                text = arcade.Text(text=self.player_name,
                                   x=ScreenSettings.WIDTH // 3, y=160,
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
        if self.background:
            arcade.draw_texture_rect(
                self.background,
                arcade.XYWH(
                    self.window.width / 2,
                    self.window.height / 2,
                    self.window.width,
                    self.window.height
                )
            )
        arcade.draw_rect_filled(
            arcade.XYWH(
                self.window.width / 2,
                self.window.height / 2,
                self.window.width,
                self.window.height
            ),
            (0, 0, 0, 120)
        )
        self.button_list.draw()
        for txt in self.text_lst:
            txt.draw()
