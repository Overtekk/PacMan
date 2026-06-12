# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  screen_settings.py                                :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 20:14:34 by roandrie        #+#    #+#               #
#  Updated: 2026/06/12 12:51:47 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from enum import Enum, auto


class ScreenSettings:
    """
    Static configuration class mapping pixel bounds constraints onto the active
    canvas environment.
    """
    WIDTH = 1280
    HEIGHT = 720


class ScreenState(Enum):
    """
    Enum flags indexing unique architectural screens to direct scene display
    routes.
    """
    MENU = "menu"
    GAME = "game"
    PAUSE = "pause"
    GAME_OVER = "game_over"
    LEADERBOARD_MENU = "leaderboard_menu"
    FINISH = "finish"
    CHEAT_MENU = "cheat_menu"

    def __str__(self) -> str:
        """Returns the localized string value associated with the configuration
          state name.

        Returns:
            str: The raw internal string representation.
        """
        return self.value


class CollectiblesType(Enum):
    """Enum class distinguishing collision evaluation flags for game items."""
    PACGUM = auto()
    SUPER_PACGUM = auto()
