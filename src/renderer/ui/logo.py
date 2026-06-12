# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  logo.py                                           :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/03 09:48:39 by roandrie        #+#    #+#               #
#  Updated: 2026/06/12 12:38:41 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from pathlib import Path

from .base_menu import BaseMenu
from src.renderer.screen_settings import ScreenSettings
from src.audio import AudioManager


class DisplayLogo(arcade.Sprite):
    """Sprite responsible for rendering the studio or game splash logo."""
    def __init__(
        self, center_x: float, center_y: float, sprite_path: Path,
        parent_view: arcade.View, scale: float = 1.5, anchor_x: str = 'left',
        anchor_y: str = 'top'
    ) -> None:
        """Initializes the display logo sprite.

        Args:
            center_x (float): Initial horizontal center position.
            center_y (float): Initial vertical center position.
            sprite_path (Path): Path to the logo image asset.
            parent_view (arcade.View): The active parent Arcade view container.
            scale (float): Rendering scale multiplier.
            anchor_x (str): Horizontal boundary texture anchor position.
            anchor_y (str): Vertical boundary texture anchor position.
        """

        super().__init__(
            path_or_texture=sprite_path, scale=scale, anchor_x=anchor_x,
            anchor_y=anchor_y
        )

        self.center_x = center_x
        self.center_y = center_y

        self.parent_view = parent_view


class LogoScreen(BaseMenu):
    """
    Splash screen displaying studio branding with fading transitions and
    introductory sound hooks.
    """
    def __init__(self, previous_view: arcade.View) -> None:
        """Initializes the splash screen state controls.

        Args:
            previous_view (arcade.View): View to return or redirect to after
            presentation.
        """
        super().__init__()

        self.previous_view = previous_view

        # - Private variables -
        self._timer: float = 5.0
        self._fading: int = 255
        self._FADING_SPEED: float = 100
        self._sound_played: bool = False

    def on_update(self, delta_time: float) -> None:
        """Manages the alpha fading sequence segments before redirecting to
        the menu view.

        Args:
            delta_time (float): Time step delta since last frame update.
        """
        self._timer -= delta_time

        # Remove opacity based on time
        if self._timer > 3.0:
            self._fading -= int(self._FADING_SPEED * delta_time)
            if self._fading < 0:
                self._fading = 0

        # Remove opacity
        if self._timer > 1.0 and self._timer <= 3.0:
            self._fading = 0

            if not self._sound_played:
                self._play_sound()
                self._sound_played = True

        # Re-add opacity
        if self._timer > 0.0 and self._timer <= 1.0:
            self._fading += int(self._FADING_SPEED * delta_time)
            if self._fading > 255:
                self._fading = 255

        if self._timer < 0.0:
            self._fading = 255
            if hasattr(self.previous_view, 'show_main_menu'):
                self.previous_view.show_main_menu()

    def build_ui(self) -> None:
        """
        Builds branding texts and structural components for the splash screen
        layout.
        """
        self._create_elements()

    def on_draw(self) -> None:
        """
        Renders the logo graphical nodes, brand texts, and overlays the fading
        mask block.
        """
        # Draw the elements
        self.button_list.draw()
        for text in self.text_lst:
            text.draw()

        # Draw the black rectangle
        arcade.draw_lrbt_rectangle_filled(
            0.0, ScreenSettings.WIDTH, 0.0, ScreenSettings.HEIGHT,
            (0, 0, 0, self._fading)
        )

    def on_key_press(self, symbol: int, _modifiers: int) -> None:
        """
        Allows users to skip the brand sequence immediately using standard
        keys.
        """
        if symbol == arcade.key.SPACE or symbol == arcade.key.ESCAPE:
            self._timer = 0.0

    # :---------------:
    #  PRIVATE METHODS
    # :---------------:

    def _create_elements(self) -> None:
        """
        Initializes branding texts, credits, and links the underlying audio
        managers.
        """
        # Init the audios elements
        self.audio_manager: AudioManager = self.window.audio_player

        # Create texts
        team_name = arcade.Text(
            text="a Haute-Daugue Supremacy game", x=ScreenSettings.WIDTH // 2,
            y=(ScreenSettings.HEIGHT // 2) - 150,
            color=arcade.color.WHITE_SMOKE, font_size=20,
            font_name='Kaph', anchor_x='center', anchor_y='top', italic=True
        )
        members = arcade.Text(
            text="anacharp & roandrie", x=ScreenSettings.WIDTH // 2,
            y=(ScreenSettings.HEIGHT // 2) - 200,
            color=arcade.color.WHITE_SMOKE, font_size=10,
            font_name='Kaph', anchor_x='center', anchor_y='top', italic=True
        )

        self.text_lst.append(team_name)
        self.text_lst.append(members)

        # Create images
        logo = DisplayLogo(
            center_x=ScreenSettings.WIDTH // 2,
            center_y=(ScreenSettings.HEIGHT // 2) + 100,
            sprite_path=self.window.asset_manager.textures['background'],
            parent_view=self,
            scale=1
        )

        self.button_list.append(logo)

    def _play_sound(self) -> None:
        """
        Dispatches an initialization splash chime sound effect via the manager.
        """
        self.audio_manager.play_random_sound(
            ['starting', 'starting2'], 1.0
        )
