# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  sprites_loader.py                                 :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/15 10:55:38 by roandrie        #+#    #+#               #
#  Updated: 2026/05/18 09:49:02 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pathlib
from pathlib import Path

from src.utils import check_path, check_folder, print_error, is_file_png

DEFAULT_SPRITES_PATH = "assets/sprites/"

REQUIERED_SPRITES: dict[str, str] = {
    "pacgum": "collectibles/pacgum.png",
    "super_pacgum": "collectibles/super_pacgum.png",

    "game_over_screen": "end/game_over.png",
    "victory_screen": "end/victory.png",

    "cat_enemy": "enemies/enemy_cat.png",
    "cat_enemy_dead": "enemies/enemy_cat_dead.png",
    "cat_enemy_eatable": "enemies/enemy_cat_eatable.png",

    "rat_enemy": "enemies/enemy_rat.png",
    "rat_enemy_dead": "enemies/enemy_rat_dead.png",
    "rat_enemy_eatable": "enemies/enemy_rat_eatable.png",

    "dog_enemy": "enemies/enemy_dog.png",
    "dog_enemy_dead": "enemies/enemy_dog_dead.png",
    "dog_enemy_eatable": "enemies/enemy_dog_eatable.png",

    "fox_enemy": "enemies/enemy_fox.png",
    "fox_enemy_dead": "enemies/enemy_fox_dead.png",
    "fox_enemy_eatable": "enemies/enemy_fox_eatable.png",

    "exit_button": "main_menu/exit.png",
    "highscores_button": "main_menu/highscores.png",
    "instructions_button": "main_menu/instructions.png",
    "logo": "main_menu/logo.png",
    "start_button": "main_menu/start.png",

    "maze_wall_corner": "maze/corner_wall.png",
    "maze_four_wall": "maze/four_wall.png",
    "maze_triple_wall": "maze/triple_wall.png",
    "maze_inside_wall": "maze/inside_wall.png",
    "maze_wall": "maze/wall.png",

    "pause_button": "pause/pause.png",
    "resume_button": "pause/resume.png",
    "return_button": "pause/return.png",

    "player": "player/player.png",
}


def check_assets_folder() -> None:
    try:
        check_folder("assets")
        check_folder("assets/sprites")
    except ValueError as e:
        print_error(e)


class SpritesLoader():
    def __init__(
        self,
        default_path: str = DEFAULT_SPRITES_PATH
    ) -> None:

        self.default_path: Path = pathlib.Path(default_path)

        # Check 'assets' folder
        check_assets_folder()

        self.textures: dict[str, Path] = {}
        self.load_sprites()

    def load_sprites(self) -> None:
        for sprite_name, relative_path in REQUIERED_SPRITES.items():

            full_path = self.default_path / relative_path

            verified_path = check_path(str(full_path))

            if not is_file_png(full_path):
                raise ValueError(
                    f"Wrong file extension for '{full_path}'.\n"
                    "😑"
                )


            self.textures[sprite_name] = verified_path
