# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  pause_menu.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:41:43 by roandrie        #+#    #+#               #
#  Updated: 2026/05/30 15:05:05 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from pathlib import Path

from .base_menu import BaseMenu
from .base_button import BaseButton
from src.renderer.ui.instructions_screen import InstructionsScreen
from src.renderer.screen_settings import ScreenSettings
from src.renderer.ui.cheat_menu import CheatMenu


class Exit(BaseButton):
    def __init__(self,
                 center_x: float,
                 center_y: float,
                 sprite_path: Path,
                 parent_view: arcade.View) -> None:

        super().__init__(center_x=center_x, center_y=center_y,
                         sprite_path=sprite_path, parent_view=parent_view)

    def on_click(self) -> None:
        # Close arcade
        arcade.exit()
        exit()


class GoBack(BaseButton):
    def __init__(self,
                 center_x: float,
                 center_y: float,
                 sprite_path: Path,
                 parent_view: arcade.View) -> None:

        super().__init__(center_x=center_x, center_y=center_y,
                         sprite_path=sprite_path, parent_view=parent_view)

    def on_click(self) -> None:
        # Go back on menu
        from src.renderer.ui.main_menu import MainMenu
        if self.parent_view.window:
            self.parent_view.window.show_view(MainMenu())


class InstructionsButton(BaseButton):
    def __init__(self,
                 center_x: float,
                 center_y: float,
                 sprite_path: Path,
                 parent_view: arcade.View) -> None:

        super().__init__(center_x=center_x, center_y=center_y,
                         sprite_path=sprite_path, parent_view=parent_view)

    def on_click(self) -> None:
        # Go on instructions menu
        instructions = InstructionsScreen(previous_view=self.parent_view)
        if self.parent_view.window:
            self.parent_view.window.show_view(instructions)


class Resume(BaseButton):
    def __init__(self,
                 center_x: float,
                 center_y: float,
                 sprite_path: Path,
                 parent_view: arcade.View) -> None:

        super().__init__(center_x=center_x, center_y=center_y,
                         sprite_path=sprite_path, parent_view=parent_view)

    def on_click(self) -> None:
        # Go back on the game
        if self.parent_view.window:
            self.parent_view.window.show_view(self.parent_view)


class Cheat(BaseButton):
    def __init__(self,
                 center_x: float,
                 center_y: float,
                 sprite_path: Path,
                 parent_view: arcade.View) -> None:

        super().__init__(center_x=center_x,
                         center_y=center_y,
                         sprite_path=sprite_path,
                         parent_view=parent_view)

    def on_click(self) -> None:
        # Go on cheat menu
        cheat = CheatMenu(previous_view=self.parent_view)
        if self.parent_view.window:
            self.parent_view.window.show_view(cheat)


class Pause(BaseButton):
    def __init__(self,
                 center_x: float,
                 center_y: float,
                 sprite_path: Path,
                 parent_view: arcade.View) -> None:

        super().__init__(center_x=center_x, center_y=center_y,
                         sprite_path=sprite_path, parent_view=parent_view)

    def on_click(self) -> None:
        pass


class PauseMenu(BaseMenu):
    def __init__(self, previous_view: arcade.View) -> None:
        super().__init__()
        self.previous_view = previous_view
        image = arcade.get_image()
        self.background = arcade.Texture(image)

    def build_ui(self) -> None:
        # Create buttons
        pause = Pause(center_x=ScreenSettings.WIDTH // 2, center_y=575,
                      sprite_path=(
                          self.window.asset_manager.textures["pause_button"]),
                      parent_view=self)
        resume = Resume(
            center_x=ScreenSettings.WIDTH // 2, center_y=475,
            sprite_path=(
                self.window.asset_manager.textures["resume_button"]),
            parent_view=self.previous_view)
        instructions_button = InstructionsButton(
            center_x=ScreenSettings.WIDTH // 2, center_y=375,
            sprite_path=(
                self.window.asset_manager.textures["instructions_button"]),
            parent_view=self)
        go_back = GoBack(
            center_x=ScreenSettings.WIDTH // 2, center_y=275,
            sprite_path=(
                self.window.asset_manager.textures["return_button"]),
            parent_view=self)
        exit = Exit(center_x=ScreenSettings.WIDTH // 2, center_y=175,
                    sprite_path=(
                        self.window.asset_manager.textures["exit_button"]),
                    parent_view=self)

        # Put buttons on a button list
        self.button_list.append(pause)
        self.button_list.append(resume)
        self.button_list.append(instructions_button)
        self.button_list.append(go_back)
        self.button_list.append(exit)

        if self.previous_view.code_found:
            self.create_cheat_button()

    def on_key_press(self, symbol: int, _modifiers: int) -> None:
        # Go back on the game
        if symbol == arcade.key.ESCAPE:
            if self.window:
                self.window.show_view(self.previous_view)

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

        # Draw buttons
        self.button_list.draw()

    def on_update(self, delta_time: float) -> None:
        # Update the sprites to check if user touch it or not
        self.button_list.update()
        for sprite in self.button_list:
            if hasattr(sprite, "on_update"):
                sprite.on_update(delta_time)

    def create_cheat_button(self) -> None:
        cheat = Cheat(
            center_x=ScreenSettings.WIDTH // 2, center_y=575,
            sprite_path=self.window.asset_manager.textures["cheat_button"],
            parent_view=self
        )
        self.button_list.append(cheat)
