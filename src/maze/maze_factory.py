# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  maze_factory.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/15 14:30:14 by roandrie        #+#    #+#               #
#  Updated: 2026/05/15 18:11:09 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.maze.load_mazegenerator import load_mazegenerator


WALL_SPRITES: dict[int, tuple[str, float]] = {
    1:  ("maze_wall", 0),
    2:  ("maze_wall", 90),
    3:  ("maze_wall_corner", 0),
    4:  ("maze_wall", 180),
    5:  ("maze_double_wall", 0),
    6:  ("maze_wall_corner", 90),
    7:  ("maze_triple_wall", 90),
    8:  ("maze_wall", -90),
    9:  ("maze_wall_corner", -90),
    10: ("maze_double_wall", 90),
    11: ("maze_triple_wall", 0),
    12: ("maze_wall_corner", 180),
    13: ("maze_triple_wall", -90),
    14: ("maze_triple_wall", 180),
    15: ("maze_four_wall", 0),
}

class MazeFactory:
    def __init__(self) -> None:
        self._maze_class = load_mazegenerator()

    def generate_maze(self, width: int, height: int,
                      textures: dict) -> list[list[int]]:
        tile_size = min(1280 // width,
                        720 // height)

        maze = self._maze_class((width, height))
        grid = maze._maze
        wall_data: list[tuple[str, float, float, float]] = []

        for row_index, row in enumerate(grid):
            for col_index, cell_value in enumerate(row):

                sprite_name, angle = WALL_SPRITES.get(
                    cell_value, ("maze_wall", 0)
                )
                sprite_path = str(textures[sprite_name])
                x = col_index * tile_size + tile_size / 2
                y = (height - 1 - row_index) * tile_size + tile_size / 2
                wall_data.append((sprite_path, angle, x, y, tile_size))
        return wall_data

