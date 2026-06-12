# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  pause_menu.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:41:43 by roandrie        #+#    #+#               #
#  Updated: 2026/06/12 12:47:51 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade
import PIL.Image

from pathlib import Path

from .base_menu import BaseMenu
from .base_button import BaseButton
from src.renderer.ui.instructions_screen import InstructionsScreen
from src.renderer.screen_settings import ScreenSettings
from src.renderer.ui.cheat_menu import CheatMenu
from src.audio import AudioManager


class GoBack(BaseButton):
    """
    Button action handling active core scene exit tasks to drop back to main
    menus.
    """
    def __init__(self,
                 center_x: float,
                 center_y: float,
                 sprite_path: Path,
                 parent_view: arcade.View) -> None:
        """Initializes the main menu navigation escape button."""

        super().__init__(center_x=center_x, center_y=center_y,
                         sprite_path=sprite_path, parent_view=parent_view)

    def on_click(self) -> None:
        """
        Exits active parameters to load clean instance setups of the main
        menus.
        """
        # Go back on menu
        from src.renderer.ui.main_menu import MainMenu
        if self.parent_view.window:
            self.parent_view.window.show_view(MainMenu())


class InstructionsButton(BaseButton):
    """
    Button swapping view fields into active player instructions manual boards.
    """
    def __init__(self,
                 center_x: float,
                 center_y: float,
                 sprite_path: Path,
                 parent_view: arcade.View) -> None:
        """Initializes help manual display route button selectors."""

        super().__init__(center_x=center_x, center_y=center_y,
                         sprite_path=sprite_path, parent_view=parent_view)

    def on_click(self) -> None:
        """
        Pushes help manuals onto visual layouts without dropping gameplay
        parameters.
        """
        # Go on instructions menu
        instructions = InstructionsScreen(previous_view=self.parent_view)
        if self.parent_view.window:
            self.parent_view.window.show_view(instructions)


class Resume(BaseButton):
    """
    Button triggering immediate context restorations to jump back into running
    gaming modules.
    """
    def __init__(self,
                 center_x: float,
                 center_y: float,
                 sprite_path: Path,
                 parent_view: arcade.View) -> None:
        """Initializes active session confirmation buttons."""

        super().__init__(center_x=center_x, center_y=center_y,
                         sprite_path=sprite_path, parent_view=parent_view)

    def on_click(self) -> None:
        """Resumes active matching sound loops and drops menu focus layers."""
        # Go back on the game
        if self.parent_view.window:
            if (hasattr(self.parent_view, 'audio_manager')
               and hasattr(self.parent_view, 'level_sound')):
                self.parent_view.audio_manager.resume_sound(
                    self.parent_view.level_sound
                )
                self.parent_view.window.show_view(self.parent_view)


class Cheat(BaseButton):
    """
    Hidden button opening developer modes if validation key inputs verify
    successfully.
    """
    def __init__(
        self,
        center_x: float,
        center_y: float,
        sprite_path: Path,
        parent_view: arcade.View,
        background: arcade.Texture
    ) -> None:
        """Initializes developers configuration menu parameters.

        Args:
            center_x (float): Horizontal element anchor coordinate.
            center_y (float): Vertical element anchor coordinate.
            sprite_path (Path): Asset file track routing location.
            parent_view (arcade.View): Stored target parent panel views.
            background (arcade.Texture): Frozen screenshot wallpaper asset
            snapshot.
        """

        super().__init__(
            center_x=center_x, center_y=center_y, sprite_path=sprite_path,
            parent_view=parent_view
        )

        self.background = background

    def on_click(self) -> None:
        """
        Loads and swaps contexts into visual debugging panels on click
        verification.
        """
        # Go on cheat menu
        cheat = CheatMenu(
            previous_view=self.parent_view, background=self.background
        )
        if self.parent_view.window:
            self.parent_view.window.show_view(cheat)


class PauseMenu(BaseMenu):
    """
    Overlay interface locking update loops while executing menu options
    selections.
    """
    def __init__(self, previous_view: arcade.View) -> None:
        """
        Captures running screen snapshots to lock gameplay displays behind
        dark overlays.
        """
        super().__init__()
        self.previous_view = previous_view
        image: PIL.Image.Image = arcade.get_image()
        self.background = arcade.Texture(image)

        # Init the audios elements
        self.audio_manager: AudioManager = self.window.audio_player

        self.y = 2

    def build_ui(self) -> None:
        """
        Draws functional navigation routes and hooks extra fields if Easter
        eggs are found.
        """
        # Create buttons

        self.resume = Resume(
            center_x=ScreenSettings.WIDTH // 2, center_y=475,
            sprite_path=(self.window.asset_manager.textures["resume_button"]),
            parent_view=self.previous_view
        )

        self.instructions_button = InstructionsButton(
            center_x=ScreenSettings.WIDTH // 2, center_y=375,
            sprite_path=(
                self.window.asset_manager.textures["instructions_button"]
            ),
            parent_view=self
        )

        self.go_back = GoBack(
            center_x=ScreenSettings.WIDTH // 2, center_y=275,
            sprite_path=(self.window.asset_manager.textures["return_button"]),
            parent_view=self
        )

        # Put buttons on a button list
        self.button_list.append(self.resume)
        self.button_list.append(self.instructions_button)
        self.button_list.append(self.go_back)

        # Create the cheat button if KONAMI code have been entered
        if hasattr(self.previous_view, 'code_found'):
            if self.previous_view.code_found:
                self.create_cheat_button()

    def on_key_press(self, symbol: int, _modifiers: int) -> None:
        """
        Manages indexing positions across option structures via arrow keys.
        """
        # Go back on the game
        if symbol == arcade.key.ESCAPE:
            if self.window:
                if hasattr(self.previous_view, 'level_sound'):
                    self.audio_manager.resume_sound(
                        self.previous_view.level_sound
                    )
                self.window.show_view(self.previous_view)

        if symbol == arcade.key.DOWN:
            self.y += 1
        if symbol == arcade.key.UP:
            self.y -= 1

        if hasattr(self.previous_view, 'code_found'):
            if not self.previous_view.code_found:

                if self.y < 0:
                    self.y = 3
                if self.y == 4:
                    self.y = 1
                if self.y == 1:
                    self.resume.check_hover(self.resume.center_x,
                                            self.resume.center_y)
                else:
                    self.resume.color = arcade.color.WHITE
                if self.y == 2:
                    self.instructions_button.check_hover(
                        self.instructions_button.center_x,
                        self.instructions_button.center_y)
                else:
                    self.instructions_button.color = arcade.color.WHITE
                if self.y == 3:
                    self.go_back.check_hover(self.go_back.center_x,
                                             self.go_back.center_y)
                else:
                    self.go_back.color = arcade.color.WHITE

                if symbol == arcade.key.ENTER or symbol == arcade.key.SPACE:
                    if self.y == 1:
                        self.resume.on_click()
                    if self.y == 2:
                        self.instructions_button.on_click()
                    if self.y == 3:
                        self.go_back.on_click()
            else:
                if self.y < 0:
                    self.y = 4
                if self.y == 5:
                    self.y = 1
                if self.y == 1:
                    self.cheat.check_hover(self.cheat.center_x,
                                           self.cheat.center_y)
                else:
                    self.cheat.color = arcade.color.WHITE
                if self.y == 2:
                    self.resume.check_hover(self.resume.center_x,
                                            self.resume.center_y)
                else:
                    self.resume.color = arcade.color.WHITE
                if self.y == 3:
                    self.instructions_button.check_hover(
                        self.instructions_button.center_x,
                        self.instructions_button.center_y)
                else:
                    self.instructions_button.color = arcade.color.WHITE
                if self.y == 4:
                    self.go_back.check_hover(self.go_back.center_x,
                                             self.go_back.center_y)
                else:
                    self.go_back.color = arcade.color.WHITE

                if symbol == arcade.key.SPACE or symbol == arcade.key.ENTER:
                    if self.y == 1:
                        self.cheat.on_click()
                    if self.y == 2:
                        self.resume.on_click()
                    if self.y == 3:
                        self.instructions_button.on_click()
                    if self.y == 4:
                        self.go_back.on_click()

    def on_draw(self) -> None:
        """
        Blurs background elements using semi-transparent dark blocks before
        rendering control paths.
        """
        self.clear()

        # Draw the game background image
        if self.background:
            arcade.draw_texture_rect(
                self.background, arcade.XYWH(
                    self.window.width / 2, self.window.height / 2,
                    self.window.width, self.window.height)
            )

        # Draw a black rectangle with an opacity
        arcade.draw_rect_filled(
            arcade.XYWH(
                self.window.width / 2, self.window.height / 2,
                self.window.width, self.window.height),
            (0, 0, 0, 180)
        )

        # Draw buttons
        self.button_list.draw()

    def on_update(self, delta_time: float) -> None:
        """Handles structural update routines for child menu components."""
        # Update the sprites to check if user touch it or not
        self.button_list.update()
        for sprite in self.button_list:
            if hasattr(sprite, "on_update"):
                sprite.on_update(delta_time)
        for obj in self.button_list:
            if isinstance(obj, Cheat):
                self.resume.center_y = 400
                self.instructions_button.center_y = 300
                self.go_back.center_y = 200
                break

    def create_cheat_button(self) -> None:
        """Instantiates and registers the cheat button option into the menu
        layout.

        This method is dynamically invoked if the player successfully triggers
        the Konami code condition from the parent gameplay view.
        """
        self.cheat = Cheat(
            center_x=ScreenSettings.WIDTH // 2, center_y=500,
            sprite_path=self.window.asset_manager.textures["cheat_button"],
            parent_view=self, background=self.background
        )
        self.button_list.append(self.cheat)
