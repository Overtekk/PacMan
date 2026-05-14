# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_settings.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 21:34:15 by roandrie        #+#    #+#               #
#  Updated: 2026/05/14 21:35:09 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from enum import Enum


class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    PAUSE = "pause"
    FINISH = "finish"

    def __str__(self) -> str:
        return self.value
