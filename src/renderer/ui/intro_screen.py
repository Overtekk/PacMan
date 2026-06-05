# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  intro_screen.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/05 11:10:24 by roandrie        #+#    #+#               #
#  Updated: 2026/06/05 17:09:21 by roandrie        ###   ########.fr        #
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

        self.textures = texture_list

        self.center_x = center_x
        self.center_y = center_y
        self.color = (44, 156, 44)

        self.animation_timer: float = 0.0
        self.current_texture_index: int = 0

    def update_animation(self, delta_time: float, is_speaking: bool) -> None:
        if is_speaking:
            self.animation_timer += delta_time
            if self.animation_timer > 0.1:
                self.animation_timer -= 0.1
                self.current_texture_index = (
                    (self.current_texture_index + 1) % len(self.textures)
                )
                self.texture = self.textures[self.current_texture_index]
        else:
            self.current_texture_index = 0
            self.texture = self.textures[0]


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
        self.speaker_map: list[str] = [
            'none',
            'daddy',
            'childs',
            'daddy',
            'childs',
            'daddy',
            'childs',
            'daddy',
            'childs',
            'daddy',
            'childs',
            'daddy',
            'childs',
            'daddy',
            'daddy',
            'daddy'
        ]

        self.dialogue_index: int = 0

        # - Private variables -
        self._dialogue_text: str = ""
        self._index: int = 0
        self._timer: float = 0.0
        self._txt_show_speed: float = 0.00

        # New Control variables
        self._is_typing: bool = False
        self._pause_timer: float = 0.0
        self._pending_next_dialogue: bool = False

    def build_ui(self) -> None:
        # Create the background screen
        self._create_ui_elements()

        self.text: arcade.Text = arcade.Text(
            "",
            x=ScreenSettings.WIDTH // 2, y=(ScreenSettings.HEIGHT // 2),
            color=arcade.color.WHITE_SMOKE, font_size=35,
            font_name='fibberish', align='center', anchor_x='center',
            anchor_y='center'
        )

        self.audio_manager.play_sound('calling', loop=True)
        self._load_dialogue(self.dialogue_index)

        self._pause_timer = 3.0

    def on_update(self, delta_time) -> None:
        if self._pause_timer > 0.0:
            self._pause_timer -= delta_time
            if self._pause_timer <= 0.0:
                self._pause_timer = 0.0
                self._on_pause_finished()

        if self._is_typing:
            self._timer += delta_time
            if self._timer > self._txt_show_speed:
                chars_to_add = int(self._timer // self._txt_show_speed)
                self._timer -= chars_to_add * self._txt_show_speed
                self._index += chars_to_add

                if self._index >= len(self._dialogue_text):
                    self._finish_typing()
                else:
                    self.text.text = self._dialogue_text[0:self._index]
        else:
            if self._pause_timer <= 0.0:
                self._auto_skip_timer += delta_time
                if self._auto_skip_timer >= 2.0:
                    self._next_dialogue()

        daddy_speaking = False
        childs_speaking = False

        if self._is_typing and self.dialogue_index < len(self.speaker_map):
            speaker = self.speaker_map[self.dialogue_index]
            if speaker == 'daddy':
                daddy_speaking = True
            elif speaker == 'childs':
                childs_speaking = True

        if hasattr(self, 'daddy'):
            self.daddy.update_animation(delta_time, daddy_speaking)
            self.child1.update_animation(delta_time, childs_speaking)
            self.child2.update_animation(delta_time, childs_speaking)
            self.child3.update_animation(delta_time, childs_speaking)

    def on_key_press(self, symbol: int, _modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            self.audio_manager.stop_sound('music_intro')
            self.audio_manager.stop_sound('dialogue_sound')
            self.audio_manager.stop_sound('calling')

            from src.game_engine.game_engine import GameEngine

            self.window.game_session = GameEngine()
            self.window.show_view(self.window.game_session)

        if self._pause_timer > 0.0:
            return

        if symbol == arcade.key.SPACE:
            if self._is_typing:
                self._finish_typing()
            else:
                self._next_dialogue()

    def on_draw(self) -> None:
        self.clear()

        # Draw background
        self.fixed_sprites.draw()
        self.sprites_lst.draw()

        self.text.draw()

    # :---------------:
    #  PRIVATE METHODS
    # :---------------:

    def _on_pause_finished(self) -> None:
        if self.dialogue_index == 0 and not self._pending_next_dialogue:
            self.audio_manager.stop_sound('calling')
            self.audio_manager.play_sound('join_call')

            self.text.text = ""
            self._is_typing = False
            self._pause_timer = 0.8
            self._pending_next_dialogue = True
            self._auto_skip_timer: float = 0.0

        elif self._pending_next_dialogue:
            self._pending_next_dialogue = False
            self.dialogue_index += 1
            self.daddy.visible = True
            self._load_dialogue(self.dialogue_index)

    def _next_dialogue(self) -> None:
        self.dialogue_index += 1
        if self.dialogue_index < len(self.dialogue_list):
            self._load_dialogue(self.dialogue_index)
        else:
            self.audio_manager.stop_sound('music_intro')

            from src.game_engine.game_engine import GameEngine

            self.window.game_session = GameEngine()
            self.window.show_view(self.window.game_session)

    def _load_dialogue(
        self, dialogue_index: int, text_speed: float = 0.06
    ) -> None:

        self._dialogue_text = self.dialogue_list[dialogue_index]
        self.text.text = ""
        self._index = 0
        self._timer = 0
        self._txt_show_speed = text_speed
        self._is_typing = True

        self._auto_skip_timer = 0.0

        if dialogue_index > 0:
            self.audio_manager.play_sound('dialogue_sound', loop=True)
        if dialogue_index == 1:
            self.audio_manager.play_sound('music_intro', 0.2, True)

    def _finish_typing(self) -> None:
        self._is_typing = False
        self._index = len(self._dialogue_text)
        self.text.text = self._dialogue_text

        self._auto_skip_timer = 0.0

        self.audio_manager.stop_sound('dialogue_sound')

        if self.dialogue_index == 11:
            self._next_dialogue()
            self.child1.visible = False
            self.child2.visible = False
            self.child3.visible = False
            self.audio_manager.play_sound('leave_call')

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

