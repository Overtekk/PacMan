# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  auto_main.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/15 11:27:45 by roandrie        #+#    #+#               #
#  Updated: 2026/06/15 14:58:01 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #
"""Used for automatically launch the game using 'run-pacman"""

from src.utils import print_error, SpritesLoader, FontLoader, AudioLoader
try:
    import arcade
except ModuleNotFoundError:
    print_error(
        "Can't start the program out of a venv"
        "\nPlease use: source .venv/bin/activate"
        "\nOr use: uv run python pac-man.py data/config.json"
    )
    exit()
from argparse import Namespace

import sys
import src.game_config

from pathlib import Path
from src.parser import load_arguments
from src.config import GameConfig
from src.maze import load_mazegenerator
from src.renderer import GameWindow
from src.leaderboard import leaderboard_loader


def main() -> int:
    try:
        root_dir = Path(__file__).resolve().parent.parent

        if len(sys.argv) == 1:
            default_config = root_dir / "data" / "config.json"
            sys.argv.append(str(default_config))

        # Check the argument, load and check the config
        args: Namespace = load_arguments()
        game_config: GameConfig = args.config_file
        src.game_config.debug_mode = args.debug

        highscore_path = Path(game_config.highscore_filename)
        if not highscore_path.is_absolute():
            highscore_path = root_dir / highscore_path
        game_config.highscore_filename = str(highscore_path)

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
        print_error(str(e))
        return 1

    except Exception as e:
        print_error(f"Critical error: {e}")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())

    except KeyboardInterrupt:
        print_error("\nProgram interrupted by user.")
        sys.exit(130)
