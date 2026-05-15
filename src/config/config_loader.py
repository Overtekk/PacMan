# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  config_loader.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 16:57:57 by roandrie        #+#    #+#               #
#  Updated: 2026/05/15 11:57:13 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from pathlib import Path

from .config_schema import GameConfig
from src.utils import can_execute_file, can_read_file, can_write_to_file
from src.utils import is_folder_exist, is_file_exist, is_file_json
from src.utils.display import print_error


def load_config(filepath: Path) -> GameConfig:
    filepath = Path(filepath)

    if not is_folder_exist(filepath.parent):
        print_error(f"'{filepath.parent}' does not exist.\nLet's play with"
                    "default config")
        default_config = create_config()
        return default_config

    if not can_execute_file(filepath.parent)\
        or not can_read_file(filepath.parent)\
             or not can_write_to_file(filepath.parent):
        print_error(f"Not all permissions are granted for: '{filepath.parent}'"
                    ".\nLet's play with default config")
        default_config = create_config()
        return default_config

    if not is_file_exist(filepath):
        print_error(f"'{filepath}' does not exist.\nLet's play with default "
                    "config")
        default_config = create_config()
        return default_config

    if not is_file_json(filepath):
        print_error(f"'{filepath}' is not a .json.\nLet's play with default "
                    "config")
        default_config = create_config()
        return default_config

    if not can_execute_file(filepath) or not can_read_file(filepath)\
       or not can_write_to_file(filepath):
        print_error(f"Not all permissions are granted for: '{filepath}'.\n"
                    "Let's play with default config")
        default_config = create_config()
        return default_config

    try:
        config = GameConfig.model_validate_json(filepath.read_text())
    except Exception as e:
        print_error(f"{e}\nLet's play with default config")
        default_config = create_config()
        return default_config

    return config


def create_config() -> GameConfig:
    return GameConfig(level=[{
			"name": "level_1",
			"width": 20,
			"height": 10
		},
		{
			"name": "level_2",
			"width": 18,
			"height": 12
		},
		{
			"name": "level_3",
			"width": 10,
			"height": 10
		},
		{
			"name": "level_4",
			"width": 10,
			"height": 20
		},
		{
			"name": "level_5",
			"width": 15,
			"height": 21
		},
		{
			"name": "level_6",
			"width": 14,
			"height": 10
		},
		{
			"name": "level_7",
			"width": 15,
			"height": 10
		},
		{
			"name": "level_8",
			"width": 12,
			"height": 16
		},
		{
			"name": "level_9",
			"width": 14,
			"height": 10
		},
		{
			"name": "level_10",
			"width": 20,
			"height": 20
		}])
