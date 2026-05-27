# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  files.py                                          :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/15 09:23:24 by roandrie        #+#    #+#               #
#  Updated: 2026/05/27 14:32:47 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

"""
File system utility functions.

This module provides helper functions to perform basic file system checks,
including verifying the existence of files and directories, and validating
file extensions for JSON compatibility.
"""

import pathlib
import os


def is_folder_exist(path_to_folder: pathlib.Path) -> bool:
    """
    Check if a given path exists and is a directory.

    Args:
        path_to_folder (pathlib.Path): The path to verify.

    Returns:
        bool: True if the path exists and is a directory, False otherwise.
    """
    return path_to_folder.exists() and path_to_folder.is_dir()


def is_file_exist(file: pathlib.Path) -> bool:
    """
    Check if a given path exists and is a regular file.

    Args:
        file (pathlib.Path): The file path to verify.

    Returns:
        bool: True if the path exists and is a file, False otherwise.
    """
    return file.exists() and file.is_file()

def check_file_extension(file: pathlib.Path, extension: str) -> bool:
    """
    Check if a file has the intended extension.

    Args:
        file (pathlib.Path): The file path to check.

    Returns:
        bool: True if the file suffix is right, False otherwise.
    """
    if not extension.startswith('.'):
        extension = f".{extension}"
    return file.suffix == extension

def can_read_file(file: pathlib.Path) -> bool:
    """
    Check if a file have the permission to be read

    Args:
        file (pathlib.Path): The file path to check.

    Returns:
        bool: True if the file have the read permission, False otherwise.
    """
    return os.access(file, os.R_OK)


def can_write_to_file(file: pathlib.Path) -> bool:
    """
    Check if a file have the permission to be writted

    Args:
        file (pathlib.Path): The file path to check.

    Returns:
        bool: True if the file have the write permission, False otherwise.
    """
    return os.access(file, os.W_OK)


def can_execute_file(file: pathlib.Path) -> bool:
    """
    Check if a file have the permission to be executed

    Args:
        file (pathlib.Path): The file path to check.

    Returns:
        bool: True if the file have the execution permission, False otherwise.
    """
    return os.access(file, os.X_OK)
