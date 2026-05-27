# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  resources_loader.py                               :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/15 10:55:38 by roandrie        #+#    #+#               #
#  Updated: 2026/05/27 14:28:27 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade
import pathlib
from pathlib import Path

from ..utils import (
    check_path, check_folder, print_error, check_file_extension
)

DEFAULT_SPRITES_PATH: str = "assets/sprites/"
DEFAULT_FONT_PATH: str = "assets/fonts/"

REQUIERED_SPRITES: dict[str, str] = {
    "pacgum": "collectibles/pacgum.png",
    "super_pacgum": "collectibles/super_pacgum.png",

    "game_over_screen": "end/game_over.png",
    "victory_screen": "end/victory.png",
    "pacman_victory": "end/pacman_victory.png",
    "glasses": "end/glasses_victory.png",
    "dead_pacman": "end/dead_pacman.png",
    "ghosts_win": "end/ghosts_win.png",

    "enemy_cat_move": "enemies/enemy_cat_move.png",
    "enemy_cat_eatable": "enemies/enemy_cat_eatable.png",
    "enemy_cat_died": "enemies/enemy_cat_died.png",

    "enemy_rat_move": "enemies/enemy_rat_move.png",
    "enemy_rat_eatable": "enemies/enemy_rat_eatable.png",
    "enemy_rat_died": "enemies/enemy_rat_died.png",

    "enemy_dog_move": "enemies/enemy_dog_move.png",
    "enemy_dog_eatable": "enemies/enemy_dog_eatable.png",
    "enemy_dog_died": "enemies/enemy_dog_died.png",

    "enemy_fox_move": "enemies/enemy_fox_move.png",
    "enemy_fox_eatable": "enemies/enemy_fox_eatable.png",
    "enemy_fox_died": "enemies/enemy_fox_died.png",

    "eyes": "enemies/eyes.png",

    "exit_button": "main_menu/exit.png",
    "highscores_button": "main_menu/highscores.png",
    "instructions_button": "main_menu/instructions.png",
    "logo": "main_menu/logo.png",
    "start_button": "main_menu/start.png",
    "cheat_button": "main_menu/cheat_mode.png",
    "gullman": "main_menu/gullman.png",

    "extra_lives": "cheat_menu/cheat_extra_lives.png",
    "freeze_ghost": "cheat_menu/cheat_freeze.png",
    "invincibility": "cheat_menu/cheat_invincibility.png",
    "next_level": "cheat_menu/cheat_next_level.png",
    "speed_up": "cheat_menu/cheat_speed_up.png",

    "maze_wall_corner": "maze/corner_wall.png",
    "maze_four_wall": "maze/four_wall.png",
    "maze_triple_wall": "maze/triple_wall.png",
    "maze_inside_wall": "maze/inside_wall.png",
    "maze_wall": "maze/wall.png",
    "life": "maze/heart.png",

    "pause_button": "pause/pause.png",
    "resume_button": "pause/resume.png",
    "return_button": "pause/return.png",

    "player": "player/player.png",
}

REQUIERED_FONTS: dict[str, str] = {
    "pressStart2P": "PressStart2P.ttf",
    "fibberish": "fibberish.ttf",
    "Kaph": "Kaph-Regular.ttf"
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

            full_path: Path = self.default_path / relative_path

            verified_path: Path = check_path(str(full_path))

            if not check_file_extension(full_path, 'png'):
                raise ValueError(
                    f"Wrong file extension for '{full_path}'.\n"
                    "😑"
                )

            self.textures[sprite_name] = verified_path


class FontLoader():
    def __init__(
        self,
        default_path: str = DEFAULT_FONT_PATH
    ) -> None:

        self.default_path: Path = pathlib.Path(default_path)

        # check 'assets' folder
        check_assets_folder()

        self.load_fonts()

    def load_fonts(self) -> None:
        for relative_path in REQUIERED_FONTS.values():

            full_path: Path = self.default_path / relative_path

            verified_path: Path = check_path(str(full_path))

            if not check_file_extension(full_path, 'ttf'):
                raise ValueError(
                    f"Wrong file extension for '{full_path}'.\n"
                    "😑"
                )

            arcade.load_font(verified_path)


def load_sprite_sheet(
    textures: dict[str, Path],
    sprite_width: int, sprite_height: int,
    sprites_columns: int, sprites_count: int
) -> list[arcade.Texture]:

    sheet =  arcade.SpriteSheet(textures)

    textures_list: list[arcade.Texture] = sheet.get_texture_grid(
        size=(sprite_width, sprite_height),
        columns=sprites_columns,
        count=sprites_count
    )

    return textures_list
