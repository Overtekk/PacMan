# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  cheat_menu.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:43:51 by roandrie        #+#    #+#               #
#  Updated: 2026/05/30 15:07:08 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from pathlib import Path

from .base_menu import BaseMenu
from .base_button import BaseButton
from src.renderer.screen_settings import ScreenSettings


class BackButton(BaseButton):
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
            parent_view=parent_view
        )

    def on_click(self) -> None:
        if self.parent_view.window:
            self.parent_view.window.show_view(self.parent_view)


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
    def __init__(self, previous_view: arcade.View) -> None:
        super().__init__()
        self.previous_view = previous_view
        # Initialise the beach background
        path = "assets/sprites/main_menu/ocean.png"
        self.background = arcade.load_texture(path)

    def build_ui(self) -> None:
        # Create all the cheat mode buttons
        invincibility = InvincibilityButton(
            center_x=ScreenSettings.WIDTH // 2,
            center_y=600,
            sprite_path=(
                self.window.asset_manager.textures["invincibility"]
            ),
            parent_view=self
        )
        extra_lives = ExtraLivesButton(
            center_x=ScreenSettings.WIDTH // 2,
            center_y=500,
            sprite_path=(
                self.window.asset_manager.textures["extra_lives"]
            ),
            parent_view=self
        )
        freeze_ghost = FreezeGhostButton(
            center_x=ScreenSettings.WIDTH // 2,
            center_y=400,
            sprite_path=(
                self.window.asset_manager.textures["freeze_ghost"]
            ),
            parent_view=self
        )
        next_level = NextLevelButton(
            center_x=ScreenSettings.WIDTH // 2,
            center_y=300,
            sprite_path=(
                self.window.asset_manager.textures["next_level"]
            ),
            parent_view=self
        )
        speed_up = SpeedUpButton(
            center_x=ScreenSettings.WIDTH // 2,
            center_y=200,
            sprite_path=(
                self.window.asset_manager.textures["speed_up"]
            ),
            parent_view=self
        )
        back = BackButton(
            center_x=ScreenSettings.WIDTH // 2,
            center_y=100,
            sprite_path=(
                self.window.asset_manager.textures["return_button"]
            ),
            parent_view=self.previous_view,
        )
        # Add all buttons on a button list
        self.button_list.append(invincibility)
        self.button_list.append(extra_lives)
        self.button_list.append(freeze_ghost)
        self.button_list.append(next_level)
        self.button_list.append(speed_up)
        self.button_list.append(back)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            # Set the "return to the main menu"
            from src.renderer.ui.main_menu import MainMenu
            if self.window:
                self.window.show_view(MainMenu())

    def on_draw(self) -> None:
        self.clear()
        # Draw the beach background
        arcade.draw_texture_rect(
            texture=self.background,
            rect=arcade.LBWH(0, 0, ScreenSettings.WIDTH, ScreenSettings.HEIGHT)
        )
        # Draw the buttons
        self.button_list.draw()
