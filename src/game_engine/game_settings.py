# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_settings.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 21:34:15 by roandrie        #+#    #+#               #
#  Updated: 2026/06/03 12:56:33 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from enum import Enum, auto


class GameState(Enum):
    SETUP = auto()
    STARTING = auto()
    PLAYING = auto()
    RESPAWN = auto()
    PAUSE = auto()
    FINISH = auto()


class LevelState(Enum):
    LEVEL_COMPLETED = auto()
    PLAYER_DIED = auto()
    CONTINUE = auto()
