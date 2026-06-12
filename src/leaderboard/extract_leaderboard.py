# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  extract_leaderboard.py                            :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/18 13:30:21 by anacharp        #+#    #+#               #
#  Updated: 2026/06/12 11:29:46 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from pathlib import Path
from typing import Any
from src.utils import can_read_file
from src.utils import is_folder_exist, is_file_exist, check_file_extension
from src.leaderboard.update_leaderboard import open_leaderboard


def extract_leaderboard(filepath_str: str) -> Any:
    """Read and format the leaderboard file into a human-readable string.

    Validates the file path and permissions before reading. Returns an
    error message string if any check fails.

    Args:
        filepath_str (str): Path to the leaderboard JSON file.

    Returns:
        Any: A formatted string listing all scores, an empty-state message,
            or an error message if the file cannot be read.
    """
    filepath: Path = Path(filepath_str)
    filepath_parent: Path = filepath.parent
    if not is_folder_exist(filepath_parent):
        return "Oops.. the folder doesn't exist"

    if not can_read_file(filepath_parent):
        return "Oops... readding permissions are invalid"

    if not is_file_exist(filepath):
        return "Oops... this file doesn't exist"

    if not check_file_extension(filepath, 'json'):
        return "Oops... this file is not a json"

    else:
        leaderboard_content = ""
        extract_content = open_leaderboard(filepath_str)
        for score, lst in extract_content.items():
            for dic in lst:
                leaderboard_content += (
                    f"{dic['player_name']}: {dic['player_score']}\n"
                )
        if not leaderboard_content:
            return "No highscores. Play."
        else:
            return leaderboard_content
