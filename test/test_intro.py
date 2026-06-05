# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  test_intro.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/05 11:36:40 by roandrie        #+#    #+#               #
#  Updated: 2026/06/05 11:43:19 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from src.renderer import ScreenSettings, ScreenState, GameWindow, IntroScreen
from src.config import GameConfig
from src.utils import SpritesLoader, AudioLoader, FontLoader, print_error
from src.renderer import MainMenu
from src.audio import AudioManager
from argparse import Namespace
import src.game_config
from src.parser import load_arguments
from src.maze import load_mazegenerator
from src.leaderboard import leaderboard_loader


class GameWindow(arcade.Window):  # noqa: F811
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
        self.show_view(IntroScreen(self))

    @property
    def screen_state(self) -> str:
        return self._screen_state

    @screen_state.setter
    def screen_state(self, new_state: ScreenState) -> None:
        self._screen_state = new_state

    def show_main_menu(self) -> None:
        self.show_view(MainMenu())


def main() -> int:
    try:
        # Check the argument, load and check the config
        args: Namespace = load_arguments()
        game_config: GameConfig = args.config_file
        src.game_config.debug_mode = args.debug

        # Check if sprites are available and store them
        sprite_loader: SpritesLoader = SpritesLoader()

        # Load fonts
        FontLoader()
        # Load audios
        audio_loader: AudioLoader = AudioLoader()

        # Load the leaderboard
        leaderboard_loader(str(game_config.highscore_filename))

        # Check if the maze generator is installed
        load_mazegenerator()

        # Create the game window (we keep the variable to avoid problem with
        # the garbage collector)
        game_window: GameWindow = GameWindow(  # noqa
            config=game_config,
            sprites_list=sprite_loader,
            audio_list=audio_loader
        )

        # Launch the main loop for the game
        arcade.run()

        return 0

    except ValueError as e:
        print_error(e)
        return 1


if __name__ == "__main__":
    main()



