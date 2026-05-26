# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  screen_settings.py                                :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 20:14:34 by roandrie        #+#    #+#               #
#  Updated: 2026/05/26 11:30:56 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from enum import Enum, auto


class ScreenSettings:
    WIDTH = 1280
    HEIGHT = 720


class ScreenState(Enum):
    MENU = "menu"
    GAME = "game"
    PAUSE = "pause"
    GAME_OVER = "game_over"
    LEADERBOARD_MENU = "leaderboard_menu"
    FINISH = "finish"
    CHEAT_MENU = "cheat_menu"

    def __str__(self) -> str:
        return self.value

class CollectiblesType(Enum):
    PACGUM = auto()
    SUPER_PACGUM = auto()
