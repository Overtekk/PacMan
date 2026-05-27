# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  cheat_menu.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:43:51 by roandrie        #+#    #+#               #
#  Updated: 2026/05/27 15:50:40 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from pathlib import Path

from .base_menu import BaseMenu
from .base_button import BaseButton


class MenuButton(BaseButton):
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


class SpeedUpButton(BaseButton):
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


class NextLevelButton(BaseButton):
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


class FreezeGhostButton(BaseButton):
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


class ExtraLivesButton(BaseButton):
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


class InvincibilityButton(BaseButton):
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


class CheatMenu(BaseMenu):
    def __init__(self) -> None:
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)

    def build_ui(self) -> None:
        invincibility = InvincibilityButton(
            center_x=640,
            center_y=600,
            sprite_path=(
                self.window.asset_manager.textures["invincibility"]
            ),
            parent_view=self
        )
        extra_lives = ExtraLivesButton(
            center_x=640,
            center_y=500,
            sprite_path=(
                self.window.asset_manager.textures["extra_lives"]
            ),
            parent_view=self
        )
        freeze_ghost = FreezeGhostButton(
            center_x=640,
            center_y=400,
            sprite_path=(
                self.window.asset_manager.textures["freeze_ghost"]
            ),
            parent_view=self
        )
        next_level = NextLevelButton(
            center_x=640,
            center_y=300,
            sprite_path=(
                self.window.asset_manager.textures["next_level"]
            ),
            parent_view=self
        )
        speed_up = SpeedUpButton(
            center_x=640,
            center_y=200,
            sprite_path=(
                self.window.asset_manager.textures["speed_up"]
            ),
            parent_view=self
        )
        menu = MenuButton(
            center_x=640,
            center_y=100,
            sprite_path=(
                self.window.asset_manager.textures["return_button"]
            ),
            parent_view=self
        )
        self.button_list.append(invincibility)
        self.button_list.append(extra_lives)
        self.button_list.append(freeze_ghost)
        self.button_list.append(next_level)
        self.button_list.append(speed_up)
        self.button_list.append(menu)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            from src.renderer.ui.main_menu import MainMenu
            if self.window:
                self.window.show_view(MainMenu())

    def on_update(self, delta_time):
        self.button_list.update()
        for sprite in self.button_list:
            sprite.on_update(delta_time)
