# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_window.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 20:09:11 by roandrie        #+#    #+#               #
#  Updated: 2026/05/27 14:11:55 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from src.config import GameConfig
from src.utils import SpritesLoader
from .screen_settings import ScreenSettings, ScreenState
from src.renderer import MainMenu


class GameWindow(arcade.Window):
    def __init__(
        self,
        config: GameConfig,
        sprites_list: SpritesLoader,
    ) -> None:

        super().__init__(
            width=ScreenSettings.WIDTH,
            height=ScreenSettings.HEIGHT,
            title="Pac-Man",
            vsync=True,
            center_window=True
        )

        self.game_config = config
        self.asset_manager = sprites_list

        self._screen_state = ScreenState.MENU
        self.show_view(MainMenu())

    @property
    def screen_state(self) -> str:
        return self._screen_state

    @screen_state.setter
    def screen_state(self, new_state: ScreenState) -> None:
        self._screen_state = new_state
