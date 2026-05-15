# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  leaderboard_loader.py                             :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 17:49:50 by roandrie        #+#    #+#               #
#  Updated: 2026/05/15 14:52:55 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from pathlib import Path
from src.utils import can_read_file, can_write_to_file
from src.utils import is_folder_exist, is_file_exist, is_file_json
from src.leaderboard.leaderboard_schema import Leaderboard
from src.utils.display import print_error, print_success


def leaderboard_loader(filepath_str: str) -> None:
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
        if not is_file_json(filepath):
            raise ValueError(f"'{filepath}' must be a json.")
        else:
            try:
                Leaderboard.model_validate_json(filepath.read_text())
            except Exception:
                print_error(f"'{filepath}''s content is invalid.\n"
                            "Let's recreate it!")
                create_leaderboard_file(filepath)


def create_leaderboard_file(filepath: Path) -> None:
    with open(filepath, "w") as f:
        f.write("")
    print_success(f"{filepath} created with success!")

    # if file do not exist, create it with all valid informations
