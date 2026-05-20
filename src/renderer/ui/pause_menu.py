# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  pause_menu.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:41:43 by roandrie        #+#    #+#               #
#  Updated: 2026/05/20 11:10:44 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from pathlib import Path

from .base_menu import BaseMenu
from .base_button import BaseButton
from src.renderer.ui.instructions_screen import InstructionsScreen


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
        arcade.exit()
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


class Resume(BaseButton):
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
        if self.parent_view.window:
            self.parent_view.window.show_view(self.parent_view.previous_view)


class Pause(BaseButton):
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


class PauseMenu(BaseMenu):
    def __init__(self, previous_view: arcade.View) -> None:
        super().__init__()
        self.previous_view = previous_view
        arcade.set_background_color(arcade.color.BLACK)

    def build_ui(self) -> None:
        pause = Pause(
            center_x=640,
            center_y=575,
            sprite_path=(
                self.window.asset_manager.textures["pause_button"]
            ),
            parent_view=self
        )
        resume = Resume(
            center_x=640,
            center_y=475,
            sprite_path=(
                self.window.asset_manager.textures["resume_button"]
            ),
            parent_view=self
        )
        instructions_button = InstructionsButton(
            center_x=640,
            center_y=375,
            sprite_path=(
                self.window.asset_manager.textures["instructions_button"]
            ),
            parent_view=self
        )
        go_back = GoBack(
            center_x=640,
            center_y=275,
            sprite_path=(
                self.window.asset_manager.textures["return_button"]
            ),
            parent_view=self
        )
        exit = Exit(
            center_x=640,
            center_y=175,
            sprite_path=(
                self.window.asset_manager.textures["exit_button"]
            ),
            parent_view=self
        )
        self.button_list.append(pause)
        self.button_list.append(resume)
        self.button_list.append(instructions_button)
        self.button_list.append(go_back)
        self.button_list.append(exit)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            from src.renderer.ui.main_menu import MainMenu
            if self.window:
                self.window.show_view(MainMenu())
        if symbol == arcade.key.SPACE:
            if self.window:
                self.window.show_view(self.previous_view)
