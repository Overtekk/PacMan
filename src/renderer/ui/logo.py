# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  logo.py                                           :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/03 09:48:39 by roandrie        #+#    #+#               #
#  Updated: 2026/06/03 10:36:13 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from pathlib import Path

from .base_menu import BaseMenu
from src.renderer.screen_settings import ScreenSettings
from src.audio import AudioManager


class DisplayLogo(arcade.Sprite):
    def __init__(
        self, center_x: float, center_y: float, sprite_path: Path,
        parent_view: arcade.View, scale: float = 1.5, anchor_x: str = 'left',
        anchor_y: str = 'top'
    ) -> None:

        super().__init__(
            path_or_texture=sprite_path, scale=scale, anchor_x=anchor_x,
            anchor_y=anchor_y
        )

        self.center_x = center_x
        self.center_y = center_y

        self.parent_view = parent_view


class LogoScreen(BaseMenu):
    def __init__(self, previous_view: arcade.View) -> None:
        super().__init__()

        self.previous_view = previous_view

        # - Private variables -
        self._timer: float = 5.0
        self._fading: int = 255
        self._FADING_SPEED: float = 100
        self._sound_played: bool = False

    def on_update(self, delta_time) -> None:
        self._timer -= delta_time

        # Remove opacity based on time
        if self._timer > 3.0:
            self._fading -= self._FADING_SPEED * delta_time
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
            self._fading += self._FADING_SPEED * delta_time
            if self._fading > 255:
                self._fading = 255

        if self._timer < 0.0:
            self._fading = 255
            self.previous_view.show_main_menu()

    def build_ui(self) -> None:
        self._create_elements()

    def on_draw(self) -> None:
        # Draw the elements
        self.button_list.draw()
        for text in self.text_lst:
            text.draw()

        # Draw the black rectangle
        arcade.draw_lrbt_rectangle_filled(
            0.0, ScreenSettings.WIDTH, 0.0, ScreenSettings.HEIGHT,
            (0,0,0, self._fading)
        )

    # :---------------:
    #  PRIVATE METHODS
    # :---------------:

    def _create_elements(self) -> None:
        # Init the audios elements
        self.audio_manager: AudioManager = AudioManager(self.window)

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
        self.audio_manager.play_sound('starting', 1.0)
