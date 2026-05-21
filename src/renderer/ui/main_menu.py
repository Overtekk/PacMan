# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  main_menu.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:37:31 by roandrie        #+#    #+#               #
#  Updated: 2026/05/21 11:03:55 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from pathlib import Path

from .base_menu import BaseMenu
from .base_button import BaseButton
from src.game_engine import GameEngine
from src.renderer.ui.highscores_screen import HighscoresScreen
from src.renderer.ui.instructions_screen import InstructionsScreen
from src.renderer.ui.cheat_menu import CheatMenu


class LogoButton(arcade.Sprite):
    def __init__(
        self,
        center_x: float,
        center_y: float,
        sprite_path: Path,
        parent_view: arcade.View,
        scale: float = 1.3
    ) -> None:

        super().__init__(
            path_or_texture=sprite_path,
            scale=scale
        )

        self.center_x = center_x
        self.center_y = center_y

        self.parent_view = parent_view


class CheatButton(BaseButton):
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
        cheat_menu = CheatMenu()

        if self.parent_view.window:
            self.parent_view.window.show_view(cheat_menu)


class ExitButton(BaseButton):
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
        arcade.exit()
        exit()


class InstructionsButton(BaseButton):
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
        instructions = InstructionsScreen(previous_view=self.parent_view)
        if self.parent_view.window:
            self.parent_view.window.show_view(instructions)


class HighscoresButton(BaseButton):
    def __init__(
            self,
            center_x: float,
            center_y: float,
            sprite_path: Path,
            parent_view: arcade.View,
    ) -> None:

        super().__init__(
            center_x=center_x,
            center_y=center_y,
            sprite_path=sprite_path,
            parent_view=parent_view,
        )

    def on_click(self) -> None:
        highscores = HighscoresScreen()

        if self.parent_view.window:
            self.parent_view.window.show_view(highscores)


class PlayButton(BaseButton):
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
        game_session = GameEngine()

        if self.parent_view.window:
            self.parent_view.window.show_view(game_session)


class MainMenu(BaseMenu):
    def __init__(self) -> None:
        super().__init__()

        arcade.set_background_color(arcade.color.BLACK)

    def build_ui(self) -> None:

        logo_button = LogoButton(
            center_x=640,
            center_y=600,
            sprite_path=self.window.asset_manager.textures["logo"],
            parent_view=self,
        )

        play_button = PlayButton(
            center_x=640,
            center_y=475,
            sprite_path=self.window.asset_manager.textures["start_button"],
            parent_view=self
        )

        highscores_button = HighscoresButton(
            center_x=640,
            center_y=375,
            sprite_path=(
                self.window.asset_manager.textures["highscores_button"]
            ),
            parent_view=self
        )

        instructions_button = InstructionsButton(
            center_x=640,
            center_y=275,
            sprite_path=(
                self.window.asset_manager.textures["instructions_button"]
            ),
            parent_view=self
        )

        cheat_button = CheatButton(
            center_x=640,
            center_y=175,
            sprite_path=self.window.asset_manager.textures["cheat_button"],
            parent_view=self
        )

        exit_button = ExitButton(
            center_x=640,
            center_y=75,
            sprite_path=self.window.asset_manager.textures["exit_button"],
            parent_view=self
        )

        self.button_list.append(logo_button)
        self.button_list.append(play_button)
        self.button_list.append(highscores_button)
        self.button_list.append(instructions_button)
        self.button_list.append(cheat_button)
        self.button_list.append(exit_button)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            arcade.exit()
            exit()
