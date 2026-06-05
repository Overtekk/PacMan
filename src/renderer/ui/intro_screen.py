# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  intro_screen.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/05 11:10:24 by roandrie        #+#    #+#               #
#  Updated: 2026/06/05 16:37:07 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from pathlib import Path

from .base_menu import BaseMenu
from src.renderer.screen_settings import ScreenSettings
from src.utils import load_sprite_sheet
from src.audio import AudioManager


class CallBackground(arcade.Sprite):
    def __init__(
        self, center_x: float, center_y: float, sprite_path: Path,
        scale: float = 1.5, anchor_x: str = 'left',
        anchor_y: str = 'top'
    ) -> None:

        super().__init__(
            path_or_texture=sprite_path, scale=scale, anchor_x=anchor_x,
            anchor_y=anchor_y
        )

        self.center_x = center_x
        self.center_y = center_y


class SeagullSprite(arcade.Sprite):
    def __init__(
        self, center_x: float, center_y: float,
        texture_list: list[arcade.Texture],
        scale: float = 1.5, anchor_x: str = 'left',
        anchor_y: str = 'top'
    ) -> None:

        super().__init__(
            path_or_texture=texture_list[0], scale=scale, anchor_x=anchor_x,
            anchor_y=anchor_y
        )

        self.center_x = center_x
        self.center_y = center_y
        self.color = (44, 156, 44)


class IntroScreen(BaseMenu):
    def __init__(self, previous_view: arcade.View) -> None:
        super().__init__()

        self.previous_view = previous_view
        self.audio_manager: AudioManager = self.window.audio_player

        # Sprites list
        self.fixed_sprites: list[arcade.Sprite] = arcade.SpriteList()
        self.sprites_lst: list[arcade.Sprite] = arcade.SpriteList()

        # Dialogues
        self.dialogue_list: list[str] = [
            '...',
            'Yes? What do you want?',
            'We are hungry daddy!!',
            'And what do you want me to do?',
            'Go find some fishes please. We want to eat that.',
            'And how much do you want?',
            'Hum.... about a millions of it!!!',
            'What!?',
            'And watch out for the other animals.',
            'Why?',
            'They want to kidnappe you.',
            'But I never say..',
            'Ok thanks you daddy! Byyyye!!',
            'Wait!',
            '...',
            'Well... I will go find fishes for them.'
        ]

        self.dialogue_index: int = 0

        # - Private variables -
        self._dialogue_text: str = ""
        self._index: int = 0
        self._timer: float = 0.0
        self._txt_show_speed: float = 0.00
        self._pause: bool = False
        self._pause_timer: float = 0.0
        self._continue_auto: bool = False

    def build_ui(self) -> None:
        # Create the background screen
        self._create_ui_elements(                                                 )

        self.text: arcade.Text = arcade.Text(
            "",
            x=ScreenSettings.WIDTH // 2, y=(ScreenSettings.HEIGHT // 2),
            color=arcade.color.WHITE_SMOKE, font_size=35,
            font_name='fibberish', align='center', anchor_x='center',
            anchor_y='center'
        )

        self.audio_manager.play_sound('calling', loop=True)

        self._pause = True
        self._pause_timer = 3.0
        self._load_dialogue(self.dialogue_index)

    def on_update(self, delta_time) -> None:
        self._timer += delta_time

        if self._continue_auto and not self._pause:
            if self._timer > 2.0:
                self.dialogue_index += 1
                self._continue_auto = False
                self._timer = 0
                self._load_dialogue(self.dialogue_index)

        if (self._timer > self._txt_show_speed and
                self._index < len(self._dialogue_text)):
            self._index += 1
            self._timer -= self._txt_show_speed
            self.text.text = self._dialogue_text[0:self._index]

        if self._index >= len(self._dialogue_text) and not self._continue_auto:
            print('t')
            self.audio_manager.stop_sound('dialogue_sound')
            self._continue_auto = True
            self._timer = 0

        if self._pause:
            if self._timer > self._pause_timer:
                self._pause = False

                self._event(self.dialogue_index)

    def on_key_press(self, symbol: int, _modifiers: int) -> None:
        if symbol == arcade.key.SPACE and not self._pause:
            if self._index < len(self._dialogue_text):
                self._index = len(self._dialogue_text)
                self.text.text = self._dialogue_text
            else:
                self.dialogue_index += 1
                if len(self.dialogue_list) > self.dialogue_index:
                    self._load_dialogue(self.dialogue_index)
                else:
                    pass # leave

    def on_draw(self) -> None:
        self.clear()

        # Draw background
        self.fixed_sprites.draw()

        self.sprites_lst.draw()

        self.text.draw()

    # :---------------:
    #  PRIVATE METHODS
    # :---------------:

    def _load_dialogue(
        self, dialogue_index: int, text_speed: float = 0.06
    ) -> None:

        self._dialogue_text = self.dialogue_list[dialogue_index]
        self.text.text = ""
        self._index = 0
        self._timer = 0
        self._txt_show_speed = text_speed

        if not self.dialogue_index == 0:
            self.audio_manager.stop_sound('dialogue_sound')
            self.audio_manager.play_sound('dialogue_sound', loop=True)

    def _create_ui_elements(self) -> None:
        background = CallBackground(
            ScreenSettings.WIDTH // 2, (ScreenSettings.HEIGHT // 2) + 200,
            self.window.asset_manager.textures['call_background'], scale=0.3
        )

        self.fixed_sprites.append(background)

        self.daddy = SeagullSprite(
            (ScreenSettings.WIDTH // 2) - 250,
            (ScreenSettings.HEIGHT // 2) + 240,
            load_sprite_sheet(
                self.window.asset_manager.textures['player'],
                sprite_width=192/6, sprite_height=32,
                sprites_columns=6, sprites_count=6
            ), scale=4
        )

        self.daddy.visible = False
        self.sprites_lst.append(self.daddy)

        self.child1 = SeagullSprite(
            (ScreenSettings.WIDTH // 2) + 231,
            (ScreenSettings.HEIGHT // 2) + 318,
            load_sprite_sheet(
                self.window.asset_manager.textures['player'],
                sprite_width=192/6, sprite_height=32,
                sprites_columns=6, sprites_count=6
            ), scale=2
        )
        self.child2 = SeagullSprite(
            (ScreenSettings.WIDTH // 2) + 250,
            (ScreenSettings.HEIGHT // 2) + 240,
            load_sprite_sheet(
                self.window.asset_manager.textures['player'],
                sprite_width=192/6, sprite_height=32,
                sprites_columns=6, sprites_count=6
            ), scale=2
        )
        self.child3 = SeagullSprite(
            (ScreenSettings.WIDTH // 2) + 296,
            (ScreenSettings.HEIGHT // 2) + 180,
            load_sprite_sheet(
                self.window.asset_manager.textures['player'],
                sprite_width=192/6, sprite_height=32,
                sprites_columns=6, sprites_count=6
            ), scale=2
        )

        self.child1.scale_x = -1
        self.child2.scale_x = -1
        self.child3.scale_x = -1

        self.sprites_lst.append(self.child1)
        self.sprites_lst.append(self.child2)
        self.sprites_lst.append(self.child3)

    def _event(self, index: int) -> None:
        match index:
            case 0:
                self.audio_manager.stop_sound('calling')
                self.audio_manager.play_sound('join_call')
                self.daddy.visible = True
                self.dialogue_index += 1
                self._load_dialogue(self.dialogue_index)
