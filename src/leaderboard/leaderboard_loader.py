# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  leaderboard_loader.py                             :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 17:49:50 by roandrie        #+#    #+#               #
#  Updated: 2026/06/12 12:12:59 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from pathlib import Path

from src.utils import can_read_file, can_write_to_file
from src.utils import is_folder_exist, is_file_exist, check_file_extension
from src.leaderboard.leaderboard_schema import Leaderboard
from src.utils.display import print_error, print_success


def leaderboard_loader(filepath_str: str) -> None:
    """Verifies layout safety permissions, structural presence, and schema
    integrity.

    Ensures target directories are present, directory permissions allow
    read/write
    operations, and validates existing files against the Pydantic structural
    model.
    Recreates corruption artifacts safely when formatting exceptions occur.

    Args:
        filepath_str (str): System absolute or relative string path to target
        JSON asset.

    Raises:
        ValueError: If directory permissions prevent reading/writing, or if the
            target path lacks a valid '.json' extension framework.
    """
    filepath: Path = Path(filepath_str)
    filepath_parent: Path = filepath.parent

    if not is_folder_exist(filepath_parent):
        filepath_parent.mkdir(mode=511, parents=True, exist_ok=True)

    if (not can_read_file(filepath_parent) or not
            can_write_to_file(filepath_parent)):
        raise ValueError(f"Missing permissions for: '{filepath_parent}'")

    if not is_file_exist(filepath):
        print_error(f"'{filepath}' does not exist.\nLet's create it!")
        create_leaderboard_file(filepath)

    else:
        if not check_file_extension(filepath, 'json'):
            raise ValueError(f"'{filepath}' must be a json.")

        else:
            try:
                Leaderboard.model_validate_json(filepath.read_text())
            except Exception:
                print_error(f"'{filepath}''s content is invalid.\n"
                            "Let's recreate it!")
                create_leaderboard_file(filepath)


def create_leaderboard_file(filepath: Path) -> None:
    """Safely initializes an empty persistent data layer file on disk
    workspace.

    Args:
        filepath (Path): Explicit Path framework reference targeting
        destination.
    """
    with open(filepath, "w") as f:
        f.write("")
    print_success(f"{filepath} created with success!")
