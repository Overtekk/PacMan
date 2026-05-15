# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  check_path.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/15 11:25:53 by roandrie        #+#    #+#               #
#  Updated: 2026/05/15 11:54:48 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import pathlib
from pathlib import Path

from .files import is_file_exist, is_folder_exist, can_read_file, is_file_png


def check_path(path_str: str) -> Path:
    filepath: Path = pathlib.Path(path_str)
    folder_parent: Path = filepath.parent

    check_folder(folder_parent)

    if not is_file_exist(filepath):
        raise ValueError(
            f"File '{filepath}' do not exist.\n"
            "Can't load the sprite. 😡"
        )

    if not can_read_file(filepath):
        raise ValueError(
            f"Permission error for '{filepath}'. Can't read.\n"
            "Can't load the sprite. 😡"
        )

    if not is_file_png(filepath):
        raise ValueError(
            f"Wrong file extension for '{filepath}'.\n"
            "Can't load the sprite. 😡"
        )

    return filepath


def check_folder(path_str: Path) -> None:
    folderpath: Path = pathlib.Path(path_str)

    if not is_folder_exist(folderpath):
        raise ValueError(
            f"Folder '{folderpath}' do not exist."
            "Can't load sprites. 😔"
        )

    if not can_read_file(folderpath):
        raise ValueError(
            f"Permission error for '{folderpath}'. Can't read.\n"
            "Can't load sprites. 😔"
        )
