# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  load_mazegenerator.py                             :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 18:02:01 by roandrie        #+#    #+#               #
#  Updated: 2026/06/05 15:08:17 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any

from src.utils import (check_folder, check_path)


def _check_mazegenerator_file() -> None:
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
    # Check resources files on the computer
    _check_mazegenerator_file()

    # Check if installed in python files
    try:
        from mazegenerator import MazeGenerator
        return MazeGenerator
    except ImportError:
        raise ValueError(
            "Module 'mazegenerator' not installed. Please, install it first by"
            " using:\n"
            "'make' or 'uv sync'.\n"
            "🤫"
        )
