from test.test_gamestate import Test
import arcade
from argparse import Namespace
from src.parser import load_arguments
from src.config import GameConfig
from src.maze import load_mazegenerator
from src.renderer import SpritesLoader, GameWindow
from src.leaderboard import leaderboard_loader


if __name__ == "__main__":
    args: Namespace = load_arguments()
    game_config: GameConfig = args.config_file

    sprite_loader: SpritesLoader = SpritesLoader()

    leaderboard_loader(str(game_config.highscore_filename))

    load_mazegenerator()

    game_window: GameWindow = GameWindow(
        config=game_config,
        sprites_list=sprite_loader
    )

    test = Test()
    game_window.show_view(test)
    arcade.run()
