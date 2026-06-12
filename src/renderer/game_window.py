# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_window.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 20:09:11 by roandrie        #+#    #+#               #
#  Updated: 2026/06/12 12:51:17 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from .screen_settings import ScreenSettings, ScreenState
from src.config import GameConfig
from src.utils import SpritesLoader, AudioLoader
from src.renderer import MainMenu, LogoScreen
from src.audio import AudioManager


class GameWindow(arcade.Window):
    """
    Central engine orchestration window class handling asset storage, sound
    setups, and view management.
    """
    def __init__(
        self,
        config: GameConfig,
        sprites_list: SpritesLoader,
        audio_list: AudioLoader
    ) -> None:
        """Configures OS window contexts, resolution sizes, VSync states,
        and boots up splash view sequences.

        Args:
            config (GameConfig): Game engine mechanics configuration instance.
            sprites_list (SpritesLoader): System utility parsing and storing
            reference texture files.
            audio_list (AudioLoader): Sound layout utility mapping raw source
            audio assets.
        """

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
    def screen_state(self) -> ScreenState:
        """Gets the structural Enum tracking identification node of the active
        running screen context.

        Returns:
            ScreenState: Active global state marker values.
        """
        return self._screen_state

    @screen_state.setter
    def screen_state(self, new_state: ScreenState) -> None:
        """Sets the structural target state tracking identity flag onto the
        window process.

        Args:
            new_state (ScreenState): The state flag to apply.
        """
        self._screen_state = new_state

    def show_main_menu(self) -> None:
        """
        Transitions application frame contexts away from splashes into the
        interaction main menus.
        """
        self.show_view(MainMenu())
