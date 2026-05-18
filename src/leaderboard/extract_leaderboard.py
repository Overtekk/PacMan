# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  extract_leaderboard.py                            :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/18 13:30:21 by anacharp        #+#    #+#               #
#  Updated: 2026/05/18 16:00:31 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from pathlib import Path
from typing import Any
from src.utils import can_read_file
from src.utils import is_folder_exist, is_file_exist, is_file_json
from src.leaderboard.update_leaderboard import open_leaderboard


def extract_leaderboard(filepath_str: str) -> Any:
    filepath: Path = Path(filepath_str)
    filepath_parent: Path = filepath.parent
    if not is_folder_exist(filepath_parent):
        return "Oops.. the folder doesn't exist"

    if not can_read_file(filepath_parent):
        return "Oops... readding permissions are invalid"

    if not is_file_exist(filepath):
        return "Oops... this file doesn't exist"

    if not is_file_json(filepath):
        return "Oops... this file is not a json"

    else:
        leaderboard_content = ""
        extract_content = open_leaderboard(filepath_str)
        for score, lst in extract_content.items():
            for dic in lst:
                leaderboard_content += f"{dic['player_name']}: {dic['player_score']}\n"
        if not leaderboard_content:
            return "No highscores. Play."
        else:
            return leaderboard_content
