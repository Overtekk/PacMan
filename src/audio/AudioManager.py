# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  AudioManager.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/01 15:30:02 by roandrie        #+#    #+#               #
#  Updated: 2026/06/01 16:03:29 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from src import game_config
from src.utils import print_log


class AudioManager():
    def __init__(self, game_window: arcade.Window) -> None:
        pass

        self.audio_dict: dict[str, arcade.Sound] = (
            game_window.audio_manager.audio
        )

    def play_sound(self, audio_name: str, volume: float = 1.0) -> None:
        if audio_name in self.audio_dict:

            arcade.play_sound(
                sound=self.audio_dict[audio_name],
                volume=volume,
            )

        else:
            if game_config.debug_mode:
                print_log(
                    f"{audio_name} not found... 😂"
                )
