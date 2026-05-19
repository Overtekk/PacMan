# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_over_screen.py                               :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:42:18 by roandrie        #+#    #+#               #
#  Updated: 2026/05/19 10:53:40 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from pathlib import Path

from .base_menu import BaseMenu
from .base_button import BaseButton


class Exit(BaseButton):
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


class GoBack(BaseButton):
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


class GameOver(BaseButton):
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


class GameOverScreen(BaseMenu):
    def __init__(self) -> None:
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)

    def build_ui(self) -> None:
        game_over = GameOver(
            center_x=640,
            center_y=600,
            sprite_path=(
                self.window.asset_manager.textures["game_over_screen"]
            ),
            parent_view=self
        )
        go_back = GoBack(
            center_x=640,
            center_y=500,
            sprite_path=(
                self.window.asset_manager.textures["return_button"]
            ),
            parent_view=self
        )
        exit = Exit(
            center_x=640,
            center_y=400,
            sprite_path=(
                self.window.asset_manager.textures["exit_button"]
            ),
            parent_view=self
        )
        self.button_list.append(game_over)
        self.button_list.append(go_back)
        self.button_list.append(exit)
