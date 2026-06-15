# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  load_mazegenerator.py                             :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 18:02:01 by roandrie        #+#    #+#               #
#  Updated: 2026/06/15 09:15:12 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any

from src.utils import (check_folder, check_path)


def _check_mazegenerator_file() -> None:
    """Verifies that the compiled layout generation wheel file exists on disk.

    Raises:
        ValueError: If local module tracking folders or binary wheel
        distributions
            cannot be located inside project directory spaces.
    """
    try:
        check_folder("mazegenerator")
        check_path("mazegenerator/mazegenerator-2.0.2-py3-none-any.whl")

    except ValueError as e:
        raise ValueError(
            "Maze Generator not found. Have you installed it?\n"
            f"{e}",
            "\n🫤"
        )


def load_mazegenerator() -> Any | None:
    """Validates binary artifacts and dynamically loads the MazeGenerator
    runtime.

    Returns:
        Any | None: The uninstantiated type reference class constructor for
        MazeGenerator.

    Raises:
        ValueError: If local file verification checks fail, or if the module
            is missing from the active interpreter virtual environment
            site-packages.
    """
    # Check resources files on the computer
    _check_mazegenerator_file()

    # Check if installed in python files
    try:
        from mazegenerator import MazeGenerator  # type: ignore
        return MazeGenerator
    except ImportError:
        raise ValueError(
            "Module 'mazegenerator' not installed. Please, install it first by"
            " using:\n"
            "'make' or 'uv sync'.\n"
            "🤫"
        )
