# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  pac-man.py                                        :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/12 16:50:43 by roandrie        #+#    #+#               #
#  Updated: 2026/05/22 10:53:21 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from argparse import Namespace

import sys
import arcade

from src.utils import print_error, SpritesLoader, FontLoader
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

        # Check if sprites are available and store them
        sprite_loader: SpritesLoader = SpritesLoader()

        # Load fonts
        FontLoader()

        # Load the leaderboard
        leaderboard_loader(str(game_config.highscore_filename))

        # Check if the maze generator is installed
        load_mazegenerator()

        # Create the game window (we keep the variable to avoid problem with
        # the garbage collector)
        game_window: GameWindow = GameWindow(  # noqa
            config=game_config,
            sprites_list=sprite_loader
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
