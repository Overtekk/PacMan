# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_settings.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 21:34:15 by roandrie        #+#    #+#               #
#  Updated: 2026/05/25 10:25:28 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from enum import Enum, auto


class GameState(Enum):
    SETUP = auto()
    STARTING = auto()
    PLAYING = auto()
    PAUSE = auto()
    FINISH = auto()

