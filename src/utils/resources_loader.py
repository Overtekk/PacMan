# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  resources_loader.py                               :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/15 10:55:38 by roandrie        #+#    #+#               #
#  Updated: 2026/06/03 16:30:09 by roandrie        ###   ########.fr        #
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
DEFAULT_AUDIO_PATH: str = "assets/audio/"

REQUIERED_SPRITES: dict[str, str] = {
    "ocean": "background/ocean.png",

    "extra_lives_off": "cheat_buttons/cheat_extra_lives_off.png",
    "freeze_ghost_off": "cheat_buttons/cheat_freeze_off.png",
    "invincibility_off": "cheat_buttons/cheat_invincibility_off.png",
    "next_level_off": "cheat_buttons/cheat_next_level_off.png",
    "speed_up_off": "cheat_buttons/cheat_speed_up_off.png",
    "extra_time_off": 'cheat_buttons/cheat_extra_time_off.png',
    "extra_lives_on": "cheat_buttons/cheat_extra_lives_on.png",
    "freeze_ghost_on": "cheat_buttons/cheat_freeze_on.png",
    "invincibility_on": "cheat_buttons/cheat_invincibility_on.png",
    "next_level_on": "cheat_buttons/cheat_next_level_on.png",
    "speed_up_on": "cheat_buttons/cheat_speed_up_on.png",
    "extra_time_on": 'cheat_buttons/cheat_extra_time_on.png',

    "heart": "collectibles/heart.png",
    "pacgum": "collectibles/pacgum.png",
    "super_pacgum": "collectibles/super_pacgum.png",

    "dead_pacman": "end_elements/dead_pacman.png",
    "game_over_screen": "end_elements/game_over.png",
    "ghosts_win": "end_elements/ghosts_win.png",
    "glasses": "end_elements/glasses_victory.png",
    "pacman_victory": "end_elements/pacman_victory.png",
    "victory_screen": "end_elements/victory.png",

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

    "maze_wall_corner": "maze/corner_wall.png",
    "maze_four_wall": "maze/four_wall.png",
    "maze_triple_wall": "maze/triple_wall.png",
    "maze_inside_wall": "maze/inside_wall.png",
    "maze_wall": "maze/wall.png",

    "pause_button": "pause/pause.png",
    "resume_button": "pause/resume.png",
    "return_button": "pause/return.png",

    "player": "player/player.png",

    "background": "background.png"
}

REQUIERED_FONTS: dict[str, str] = {
    "pressStart2P": "PressStart2P.ttf",
    "fibberish": "fibberish.ttf",
    "Kaph": "Kaph-Regular.ttf"
}

REQUIERED_SOUNDS: dict[str, dict[str, str]] = {
    "fah": {
        "path": "fah.mp3",
        "streaming": False
    },
    "bruit": {
        "path": "bruit.mp3",
        "streaming": False
    },
    "eat": {
        "path": "eat.mp3",
        "streaming": False
    },
    "oh_oh": {
        "path": "oh_oh.ogg",
        "streaming": False
    },
    "starting": {
        "path": "starting.mp3",
        "streaming": True
    },
    "starting2": {
        "path": "starting2.mp3",
        "streaming": True
    },
    "gameover": {
        "path": "gameover/game_over.ogg",
        "streaming": False
    },
    "dead1": {
        "path": "player/dead_1.ogg",
        "streaming": False
    },
    "eat1": {
        "path": "player/eat_1.ogg",
        "streaming": False
    },
    "eat2": {
        "path": "player/eat_2.ogg",
        "streaming": False
    },
    "eat3": {
        "path": "player/eat_3.ogg",
        "streaming": False
    },
    "slurp1": {
        "path": "player/slurp_1.ogg",
        "streaming": False
    },
    "slurp2": {
        "path": "player/slurp_2.ogg",
        "streaming": False
    },
    "slurp3": {
        "path": "player/slurp_3.ogg",
        "streaming": False
    },
    "slurp4": {
        "path": "player/slurp_4.ogg",
        "streaming": False
    },
    "slurp5": {
        "path": "player/slurp_5.ogg",
        "streaming": False
    },
    "start_one": {
        "path": "start/1.ogg",
        "streaming": False
    },
    "start_two": {
        "path": "start/2.ogg",
        "streaming": False
    },
    "start_three": {
        "path": "start/3.ogg",
        "streaming": False
    },
    "start_go": {
        "path": "start/go.ogg",
        "streaming": False
    },
    "click1": {
        "path": "ui/click_1.ogg",
        "streaming": False
    },
    "points": {
        "path": "ui/points.mp3",
        "streaming": False
    },
    "gg1": {
        "path": "victory/gg_1.ogg",
        "streaming": False
    },
    "gg2": {
        "path": "victory/gg_2.ogg",
        "streaming": False
    },
    "gg3": {
        "path": "victory/gg_3.ogg",
        "streaming": False
    },
    "gg4": {
        "path": "victory/gg_4.ogg",
        "streaming": False
    },
    "victory": {
        "path": "victory/victory.mp3",
        "streaming": False
    },
    "levelcompleted": {
        "path": "victory/level_completed.mp3",
        "streaming": False
    },
    "music_mainmenu": {
        "path": "music/main_menu.mp3",
        "streaming": False
    },
    "enemydied": {
        "path": "enemy/died.mp3",
        "streaming": False
    },
    "enemyrespawn": {
        "path": "enemy/respawn.mp3",
        "streaming": False
    },
    "music_invincible": {
        "path": "music/invincible.mp3",
        "streaming": False
    },
}


def check_assets_folder() -> None:
    try:
        check_folder(Path("assets"))
        check_folder(Path("assets/sprites"))
    except ValueError as e:
        print_error(str(e))


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


class AudioLoader():
    def __init__(
        self,
        default_path: str = DEFAULT_AUDIO_PATH
    ) -> None:

        self.default_path: Path = pathlib.Path(default_path)

        # check 'assets' folder
        check_assets_folder()

        self.audio: dict[str, arcade.Sound] = {}
        self.load_audio()

    def load_audio(self) -> None:
        for audio_name, audio_data in REQUIERED_SOUNDS.items():

            relative_path = audio_data["path"]
            full_path: Path = self.default_path / relative_path

            verified_path: Path = check_path(str(full_path))

            if (not check_file_extension(full_path, 'mp3') and
                    not check_file_extension(full_path, 'ogg')):
                raise ValueError(
                    f"Wrong file extension for '{full_path}'.\n"
                    "😑"
                )

            self.audio[audio_name] = arcade.Sound(
                verified_path,
                streaming=audio_data["streaming"]
            )



def load_sprite_sheet(textures: dict[str, Path],
                      sprite_width: int,
                      sprite_height: int,
                      sprites_columns: int,
                      sprites_count: int) -> list[arcade.Texture]:

    sheet = arcade.SpriteSheet(textures)

    textures_list: list[arcade.Texture] = sheet.get_texture_grid(
        size=(sprite_width, sprite_height),
        columns=sprites_columns,
        count=sprites_count
    )

    return textures_list
