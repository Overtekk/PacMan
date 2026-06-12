# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  check_path.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/15 11:25:53 by roandrie        #+#    #+#               #
#  Updated: 2026/06/12 11:42:19 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

"""Module providing path validation functions for files and directories."""

import pathlib
from pathlib import Path

from .files import is_file_exist, is_folder_exist, can_read_file


def check_path(path_str: str) -> Path:
    """Verify if a file path exists, its parent directory exists, and it is
    readable.

    Args:
        path_str (str): The string representation of the file path to verify.

    Returns:
        Path: The validated pathlib.Path object.

    Raises:
        ValueError: If the parent directory doesn't exist, if the file doesn't
            exist, or if the file cannot be read due to permissions.
    """
    filepath: Path = pathlib.Path(path_str)
    folder_parent: Path = filepath.parent

    check_folder(folder_parent)

    if not is_file_exist(filepath):
        raise ValueError(
            f"File '{filepath}' do not exist.\n"
        )

    if not can_read_file(filepath):
        raise ValueError(
            f"Permission error for '{filepath}'. Can't read.\n"
        )

    return filepath


def check_folder(path_str: Path | str) -> None:
    """Verify if a directory path exists and is readable.

    Args:
        path_str (Path | str): The path to the directory as a string or Path
        object.

    Raises:
        ValueError: If the folder doesn't exist or cannot be read due to
        permissions.
    """
    folderpath: Path = pathlib.Path(path_str)

    if not is_folder_exist(folderpath):
        raise ValueError(
            f"Folder '{folderpath}' do not exist."
        )

    if not can_read_file(folderpath):
        raise ValueError(
            f"Permission error for '{folderpath}'. Can't read.\n"
        )
