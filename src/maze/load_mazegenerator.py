# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  load_mazegenerator.py                             :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 18:02:01 by roandrie        #+#    #+#               #
#  Updated: 2026/06/15 13:45:38 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import sys
from pathlib import Path
from typing import Any

MazeGenerator: Any = None


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
    # Check if installed in python files
    global MazeGenerator

    if hasattr(sys, '_MEIPASS'):
        root_dir = Path(sys._MEIPASS)
    else:
        candidate = Path(__file__).resolve().parent.parent.parent
        if (candidate / "mazegenerator").exists():
            root_dir = candidate
        else:
            root_dir = Path(__file__).resolve().parent.parent

    whl_path = root_dir / "mazegenerator" / "mazegenerator-2.0.2-py3-none-any.whl"

    if not whl_path.exists():
        raise ValueError(
            f"Can´t find wheel file: {whl_path}\n"
        )

    if str(whl_path) not in sys.path:
        sys.path.insert(0, str(whl_path))

    try:
        import mazegenerator

        if hasattr(mazegenerator, "MazeGenerator"):
            MazeGenerator = mazegenerator.MazeGenerator
        else:
            raise ValueError(
                "Module 'mazegenerator' has no attribute 'MazeGenerator'"
            )

    except ImportError:
        raise ValueError(
            "Maze Generator package not found in the current environment.\n"
            "Please ensure it is installed via your dependencies.\n"
            "🫤"
        )


def get_maze_class() -> Any:
    """Returns the loaded MazeGenerator class."""
    global MazeGenerator
    return MazeGenerator
