# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  AudioManager.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/01 15:30:02 by roandrie        #+#    #+#               #
#  Updated: 2026/06/08 11:18:56 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade
import random

from src import game_config
from src.utils import print_log

import pyglet.media as media


class AudioManager():
    def __init__(self, game_window: arcade.Window) -> None:
        pass

        self.audio_dict: dict[str, arcade.Sound] = (
            game_window.audio_manager.audio
        )

        # List of all active sounds
        self.active_players: dict[str, media.Player] = {}
        self._init_audio()

    def play_sound(
        self, audio_name: str, volume: float = 1.0, loop: bool = False
    ) -> None:
        if audio_name in self.audio_dict:

            player: media.Player = arcade.play_sound(
                sound=self.audio_dict[audio_name],
                volume=volume,
                loop=loop
            )
            if player is not None:
                self.active_players[audio_name] = player

        else:
            if game_config.debug_mode:
                self._sound_not_found_error(audio_name)

    def play_random_sound(
        self, list_sounds: list[str], volume: float = 1.0
    ) -> None:
        filtered_sound_list: list[str] = []

        for audio_name in list_sounds:
            if audio_name not in self.audio_dict:
                if game_config.debug_mode:
                    self._sound_not_found_error(audio_name)
                continue

            filtered_sound_list.append(audio_name)

        random_sound: str = random.choice(filtered_sound_list)
        player = arcade.play_sound(
            sound=self.audio_dict[random_sound],
            volume=volume
        )

        self.active_players[audio_name] = player

    def pause_sound(self, audio_name: str) -> None:
        if audio_name in self.active_players:
            player = self.active_players[audio_name]

            if player is not None:
                player.pause()

        else:
            if game_config.debug_mode:
                self._sound_not_found_error(audio_name)

    def resume_sound(self, audio_name: str) -> None:
        if audio_name in self.active_players:
            player = self.active_players[audio_name]

            if player is not None:
                player.play()

        else:
            if game_config.debug_mode:
                self._sound_not_found_error(audio_name)

    def stop_sound(self, audio_name: str) -> None:
        if audio_name in self.active_players:
            player = self.active_players[audio_name]

            if player is not None:
                arcade.stop_sound(player)

            del self.active_players[audio_name]

        else:
            if game_config.debug_mode:
                self._sound_not_found_error(audio_name)

    def stop_all_sounds(self) -> None:
        for player in self.active_players.values():
            arcade.stop_sound(player)
        self.active_players.clear()

    # :---------------:
    #  PRIVATE METHODS
    # :---------------:

    def _init_audio(self) -> None:
        audios_to_init: list[str] = [
            'eat', 'eat1', 'eat2', 'eat3', 'fah', 'dead1', 'gameover',
            'slurp1', 'slurp2', 'slurp3', 'slurp4', 'slurp5',
            'start_one', 'start_two', 'start_three', "start_go", 'click1',
            'gg1', 'gg2', 'gg3', 'gg4', 'oh_oh', 'victory', 'levelcompleted',
            'points', 'enemydied', 'enemyrespawn', 'calling', 'leave_call',
            'join_call', 'dialogue_sound_child'
        ]

        for audio_name in audios_to_init:
            self.play_sound(audio_name, 0)

    def _sound_not_found_error(self, audio_name: str) -> None:
        print_log(f"{audio_name} not found... 😂")
