# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  config_loader.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 16:57:57 by roandrie        #+#    #+#               #
#  Updated: 2026/05/27 15:29:07 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from pathlib import Path

from .config_schema import GameConfig

from src.utils import (
    can_read_file, can_write_to_file, is_folder_exist, is_file_exist,
    check_file_extension
    )
from src.utils.display import print_error


mandatory_keys: list[str] = [
    "highscore_filename",
    "live",
    "pacgum_points",
    "super_pacgum_points",
    "ghost_points",
    "seed",
    "level_max_time",
    "level"
]


def load_config(filepath: Path) -> GameConfig:
    # SECURITY: create the Path object
    filepath: Path = Path(filepath)

    # Check 'data' folder
    if not is_folder_exist(filepath.parent):

        _print_default_error_message(f"'{filepath.parent}' doesn't exist.")
        return _create_default_config()

    # Check permissions of 'data' folder
    if (not can_read_file(filepath.parent) or not
            can_write_to_file(filepath.parent)):

        raise ValueError(f"Missing permissions for '{filepath.parent}'")

    # Check if config file exist
    if not is_file_exist(filepath):

        _print_default_error_message(f"'{filepath}' doesn't exist.")
        return _create_default_config()

    # Check if config file have json extension
    if not check_file_extension(filepath, 'json'):

        _print_default_error_message(f"'{filepath}' is not '.json'")
        return _create_default_config()

    # Check permission of config file
    if not can_read_file(filepath) or not can_write_to_file(filepath):

        _print_default_error_message(f"Permission error for '{filepath}'.")
        return _create_default_config()

    # Check for missing keys
    missing_keys: list[str] = []

    for key in mandatory_keys:
        if key not in filepath.read_text():
            missing_keys.append(key)

    if missing_keys:
        _print_default_error_message(f"Missing mandatory keys {missing_keys}.")
        return _create_default_config()

    # Pydantic validation
    try:
        return GameConfig.model_validate_json(filepath.read_text())
    except Exception as e:

        _print_default_error_message(f"Configuration error: {e}")
        return _create_default_config()


def _create_default_config() -> GameConfig:
    return GameConfig()


def _print_default_error_message(error: str) -> None:
    error += "\nLet's play with the default config ! 🐨"

    print_error(error)
