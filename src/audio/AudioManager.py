# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  AudioManager.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/01 15:30:02 by roandrie        #+#    #+#               #
#  Updated: 2026/06/02 15:41:57 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade
import random

from src import game_config
from src.utils import print_log


class AudioManager():
    def __init__(self, game_window: arcade.Window) -> None:
        pass

        self.audio_dict: dict[str, arcade.Sound] = (
            game_window.audio_manager.audio
        )
        self._init_audio()

    def play_sound(self, audio_name: str, volume: float = 1.0) -> None:
        if audio_name in self.audio_dict:

            arcade.play_sound(
                sound=self.audio_dict[audio_name],
                volume=volume,
            )

        else:
            if game_config.debug_mode:
                self._sound_not_found_error(audio_name)

    def play_random_sound(
        self, list_sounds: list[str], volume: float = 1.0
    ) -> None:
        for audio_name in list_sounds:
            if audio_name not in self.audio_dict:
                if game_config.debug_mode:
                    self._sound_not_found_error(audio_name)
                list_sounds.remove(audio_name)

        random_sound: str = random.choice(list_sounds)
        arcade.play_sound(
            sound=self.audio_dict[random_sound],
            volume=volume
        )


    # :---------------:
    #  PRIVATE METHODS
    # :---------------:

    def _init_audio(self) -> None:
        audios_to_init: list[str] = [
            'eat', 'eat1', 'eat2', 'eat3', 'fah', 'dead1'
        ]

        for audio_name in audios_to_init:
            self.play_sound(audio_name, 0)

    def _sound_not_found_error(self, audio_name: str) -> None:
        print_log(f"{audio_name} not found... 😂")
