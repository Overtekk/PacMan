# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_window.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 20:09:11 by roandrie        #+#    #+#               #
#  Updated: 2026/06/03 13:14:49 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from .screen_settings import ScreenSettings, ScreenState
from src.config import GameConfig
from src.utils import SpritesLoader, AudioLoader
from src.renderer import MainMenu, LogoScreen
from src.audio import AudioManager


class GameWindow(arcade.Window):
    def __init__(
        self,
        config: GameConfig,
        sprites_list: SpritesLoader,
        audio_list: AudioLoader
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
        self.audio_manager = audio_list
        self.audio_player = AudioManager(self)

        self._screen_state = ScreenState.MENU
        self.show_view(LogoScreen(self))

    @property
    def screen_state(self) -> str:
        return self._screen_state

    @screen_state.setter
    def screen_state(self, new_state: ScreenState) -> None:
        self._screen_state = new_state

    def show_main_menu(self) -> None:
        self.show_view(MainMenu())
