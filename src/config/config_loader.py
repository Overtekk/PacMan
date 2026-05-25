# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  config_loader.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 16:57:57 by roandrie        #+#    #+#               #
#  Updated: 2026/05/25 09:26:46 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from pathlib import Path

from .config_schema import GameConfig

from src.utils import can_read_file, can_write_to_file
from src.utils import is_folder_exist, is_file_exist, is_file_json
from src.utils.display import print_error


mandatory_keys: list[str] = [
    "highscore_filename", "live", "pacgum_points", "super_pacgum_points",
    "ghost_points", "seed", "level_max_time", "level"
]



def load_config(filepath: Path) -> GameConfig:
    filepath: Path = Path(filepath)

    if not is_folder_exist(filepath.parent):
        print_error(
            f"'{filepath.parent}' does not exist.\nLet's play with default "
            "config"
        )
        default_config: GameConfig = _create_config()
        return default_config

    if (not can_read_file(filepath.parent) or not
            can_write_to_file(filepath.parent)):
        raise ValueError(f"Missing permissions for: '{filepath.parent}'")

    if not is_file_exist(filepath):
        print_error(
            f"'{filepath}' does not exist.\nLet's play with default config"
        )
        default_config: GameConfig = _create_config()
        return default_config

    if not is_file_json(filepath):
        print_error(
            f"'{filepath}' is not a .json.\nLet's play with default config"
        )
        default_config: GameConfig = _create_config()
        return default_config

    if not can_read_file(filepath) or not can_write_to_file(filepath):
        print_error(
            f"Not all permissions are granted for: '{filepath}'.\n"
            "Let's play with default config"
        )
        default_config: GameConfig = _create_config()
        return default_config

    # Check for missing keys
    missing_keys: list[str] = []

    for k in mandatory_keys:
        if k not in filepath.read_text():
            missing_keys.append(k)

    if missing_keys:
        print_error(
            f"Missing key/s : {missing_keys}.\nLet's play with default config"
        )
        default_config = _create_config()
        return default_config

    # If no errors, check is json is valid
    try:
        config: GameConfig = (
            GameConfig.model_validate_json(filepath.read_text())
        )

    except Exception as e:
        print_error(f"{e}\nLet's play with default config")
        default_config: GameConfig = _create_config()
        return default_config

    return config


def _create_config() -> GameConfig:
    return GameConfig()
