# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_over_screen.py                               :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:42:18 by roandrie        #+#    #+#               #
#  Updated: 2026/06/05 13:51:59 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from pathlib import Path
from src.renderer.screen_settings import ScreenSettings
from src.leaderboard.update_leaderboard import save_score_to_leaderboard

from .base_menu import BaseMenu


class GhostsWin(arcade.Sprite):
    def __init__(
        self,
        center_x: float,
        center_y: float,
        sprite_path: Path,
        parent_view: arcade.View,
        scale: float = 1.8,
        anchor_x: str = "center"
    ) -> None:

        super().__init__(
            path_or_texture=sprite_path,
            scale=scale,
            anchor_x=anchor_x
        )

        self.center_x = center_x
        self.center_y = center_y

        self.parent_view = parent_view


class DeadPacman(arcade.Sprite):
    def __init__(
        self,
        center_x: float,
        center_y: float,
        sprite_path: Path,
        parent_view: arcade.View,
        scale: float = 2.0,
        anchor_x: str = "center"
    ) -> None:

        super().__init__(
            path_or_texture=sprite_path,
            scale=scale,
            anchor_x=anchor_x
        )

        self.center_x = center_x
        self.center_y = center_y

        self.parent_view = parent_view


class GameOver(arcade.Sprite):
    def __init__(
        self,
        center_x: float,
        center_y: float,
        sprite_path: Path,
        parent_view: arcade.View,
        scale: float = 1.5,
        anchor_x: str = "center"
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
    def __init__(self, score: int, filename: str,
                 previous_view: arcade.View) -> None:
        super().__init__()
        self.player_name = ""
        self.score = score
        self.filename = filename
        self.previous_view = previous_view
        image = arcade.get_image()
        self.background = arcade.Texture(image)

    def build_ui(self) -> None:
        # Set the 'game over' sprite
        game_over = GameOver(
            center_x=ScreenSettings.WIDTH // 2,
            center_y=560,
            sprite_path=self.window.asset_manager.textures["game_over_screen"],
            parent_view=self)

        # Set funny sprites
        dead_pacman = DeadPacman(
            center_x=ScreenSettings.WIDTH // 2 - 290,
            center_y=330,
            sprite_path=self.window.asset_manager.textures["dead_pacman"],
            parent_view=self)
        ghosts_win = GhostsWin(
            center_x=ScreenSettings.WIDTH // 2 + 285,
            center_y=345,
            sprite_path=self.window.asset_manager.textures["ghosts_win"],
            parent_view=self)

        # Write some text
        score = arcade.Text(text="SCORE", x=ScreenSettings.WIDTH // 2, y=360,
                            color=arcade.color.WHITE, font_size=40,
                            font_name="Press Start 2P",
                            anchor_x="center")
        nb = arcade.Text(text=str(int(self.score)),
                         x=ScreenSettings.WIDTH // 2, y=285,
                         color=arcade.color.YELLOW, font_size=40,
                         font_name="Press Start 2P",
                         anchor_x="center")
        enter_name = arcade.Text(text="SAVE YOUR NAME",
                                 x=ScreenSettings.WIDTH // 2, y=180,
                                 color=arcade.color.WHITE, font_size=40,
                                 font_name="Press Start 2P",
                                 anchor_x="center")

        # Add all texts on a text list and all buttons on a button list
        self.text_lst.append(score)
        self.text_lst.append(nb)
        self.text_lst.append(enter_name)
        self.button_list.append(game_over)
        self.button_list.append(dead_pacman)
        self.button_list.append(ghosts_win)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        # Enter name to save the score in the highscores list

        if len(self.player_name) < 10:
            # User can only use alpha characters
            if arcade.key.A <= symbol <= arcade.key.Z:
                maj = modifiers & arcade.key.MOD_CAPSLOCK
                self.player_name += chr(symbol).upper() if maj else chr(symbol)
                text = arcade.Text(text=self.player_name,
                                   x=ScreenSettings.WIDTH // 3, y=110,
                                   color=arcade.color.YELLOW, font_size=40,
                                   font_name="Press Start 2P")
                self.text_lst.append(text)

        if len(self.player_name) > 0:
            # Delete a character
            if symbol == arcade.key.BACKSPACE:
                self.player_name = self.player_name[:-1]
                if self.text_lst:
                    self.text_lst.pop()

            if symbol == arcade.key.ENTER:
                # Press enter to return on main menu, it saves the name and
                # highscore on the highscores list
                from src.renderer.ui.main_menu import MainMenu
                if self.window:
                    self.window.show_view(MainMenu())

                if hasattr(self.previous_view, 'parent_view'):
                    save_score_to_leaderboard(
                        self.filename, self.player_name, float(self.score),
                        self.previous_view.parent_view.code_found)

    def on_draw(self) -> None:
        self.clear()

        # Draw the game background image
        if self.background:
            arcade.draw_texture_rect(self.background,
                                     arcade.XYWH(self.window.width / 2,
                                                 self.window.height / 2,
                                                 self.window.width,
                                                 self.window.height))

        # Draw a black rectangle with an opacity
        arcade.draw_rect_filled(arcade.XYWH(self.window.width / 2,
                                            self.window.height / 2,
                                            self.window.width,
                                            self.window.height),
                                (0, 0, 0, 180))

        self.button_list.draw()
        for txt in self.text_lst:
            txt.draw()
