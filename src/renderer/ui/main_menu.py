# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  main_menu.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:37:31 by roandrie        #+#    #+#               #
#  Updated: 2026/05/18 16:12:59 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from pathlib import Path

from .base_menu import BaseMenu
from .base_button import BaseButton
from src.game_engine import GameEngine
from src.renderer.ui.highscores_screen import HighscoresScreen
from src.renderer.ui.instructions_screen import InstructionsScreen

class LogoButton(BaseButton):
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
        pass

    def check_hover(self, x: float, y: float) -> None:
        pass

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
        instructions = InstructionsScreen()

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
            center_y=550,
            sprite_path=self.window.asset_manager.textures["logo"],
            parent_view=self
        )

        play_button = PlayButton(
            center_x=640,
            center_y=450,
            sprite_path=self.window.asset_manager.textures["start_button"],
            parent_view=self
        )

        highscores_button = HighscoresButton(
            center_x=640,
            center_y=350,
            sprite_path=(
                self.window.asset_manager.textures["highscores_button"]
            ),
            parent_view=self
        )

        instructions_button = InstructionsButton(
            center_x=640,
            center_y=250,
            sprite_path=(
                self.window.asset_manager.textures["instructions_button"]
            ),
            parent_view=self
        )

        exit_button = ExitButton(
            center_x=640,
            center_y=150,
            sprite_path=self.window.asset_manager.textures["exit_button"],
            parent_view=self
        )

        self.button_list.append(logo_button)
        self.button_list.append(play_button)
        self.button_list.append(highscores_button)
        self.button_list.append(instructions_button)
        self.button_list.append(exit_button)

