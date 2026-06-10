# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  pac-man.py                                        :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/12 16:50:43 by roandrie        #+#    #+#               #
#  Updated: 2026/06/08 16:24:50 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.utils import print_error, SpritesLoader, FontLoader, AudioLoader
try:
    import arcade
except ModuleNotFoundError:
    print_error("Can't start the program out of a venv" \
    "\nPlease use: source .venv/bin/activate" \
    "\nOr use: uv run python pac-man.py data/config.json")
    exit()
from argparse import Namespace

import sys
import src.game_config

from src.parser import load_arguments
from src.config import GameConfig
from src.maze import load_mazegenerator
from src.renderer import GameWindow
from src.leaderboard import leaderboard_loader


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

    # except Exception as e:
    #     print_error(f"Critical error: {e}")
    #     return 1


if __name__ == "__main__":
    try:
        sys.exit(main())

    except KeyboardInterrupt:
        print_error("\nProgram interrupted by user.")
        sys.exit(130)
