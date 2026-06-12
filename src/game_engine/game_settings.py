# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_settings.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 21:34:15 by roandrie        #+#    #+#               #
#  Updated: 2026/06/12 12:08:12 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from enum import Enum, auto


class GameState(Enum):
    """Represents the global lifecycle phases of the main application engine.
    """
    SETUP = auto()
    STARTING = auto()
    PLAYING = auto()
    RESPAWN = auto()
    PAUSE = auto()
    FINISH = auto()


class LevelState(Enum):
    """
    Tracks frame-by-frame status changes inside the CollisionManager matrix
    loop.
    """
    LEVEL_COMPLETED = auto()
    PLAYER_DIED = auto()
    ENEMY_DIED = auto()
    CONTINUE = auto()
