# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_over_screen.py                               :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:42:18 by roandrie        #+#    #+#               #
#  Updated: 2026/05/21 10:35:25 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from pathlib import Path

from .base_menu import BaseMenu


class GameOver(arcade.Sprite):
    def __init__(
        self,
        center_x: float,
        center_y: float,
        sprite_path: Path,
        parent_view: arcade.View,
        scale: float = 1.5
    ) -> None:

        super().__init__(
            path_or_texture=sprite_path,
            scale=scale
        )

        self.center_x = center_x
        self.center_y = center_y

        self.parent_view = parent_view


class GameOverScreen(BaseMenu):
    def __init__(self) -> None:
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)
        self.player_name = ""

    def build_ui(self) -> None:
        game_over = GameOver(
            center_x=640,
            center_y=560,
            sprite_path=(
                self.window.asset_manager.textures["game_over_screen"]
            ),
            parent_view=self
        )
        score = arcade.Text(text="SCORE: 100", x=410, y=360,
                                   color=arcade.color.WHITE, font_size=40)
        self.text_lst.append(score)
        enter_name = arcade.Text(text="SAVE YOUR NAME:", x=410, y=300,
                                   color=arcade.color.WHITE, font_size=40)
        self.text_lst.append(enter_name)
        self.button_list.append(game_over)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if len(self.player_name) < 10:
            if arcade.key.A <= symbol <= arcade.key.Z:
                maj = modifiers & arcade.key.MOD_CAPSLOCK
                self.player_name += chr(symbol).upper() if maj else chr(symbol)
                text = arcade.Text(text=self.player_name, x=480, y=200,
                                   color=arcade.color.YELLOW, font_size=40)
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
            # + mettre la string et le score dans le json

    def on_draw(self) -> None:
        self.clear()
        self.button_list.draw()
        for txt in self.text_lst:
            txt.draw()

# afficher le score
