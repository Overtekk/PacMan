# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  maze_factory.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/15 14:30:14 by roandrie        #+#    #+#               #
#  Updated: 2026/05/19 10:19:20 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.maze.load_mazegenerator import load_mazegenerator
from typing import Any


WALL_SPRITES: dict[int, tuple[str, float]] = {
    "wall":  ("maze_wall", 0),
    "wall_90":  ("maze_wall", 90),
    "wall_180":  ("maze_wall", 180),
    "wall_270":  ("maze_wall", -90),

    "corner":  ("maze_wall_corner", 0),
    "corner_90":  ("maze_wall_corner", 90),
    "corner_180": ("maze_wall_corner", 180),
    "corner_270":  ("maze_wall_corner", -90),

    "triple_wall": ("maze_triple_wall", 0),
    "triple_wall_90":  ("maze_triple_wall", 90),
    "triple_wall_180": ("maze_triple_wall", 180),
    "triple_wall_270": ("maze_triple_wall", -90),

    "inside_wall": ("maze_inside_wall", 0),
    "inside_wall_90":  ("maze_inside_wall", 90),
    "inside_wall_180": ("maze_inside_wall", 180),
    "inside_wall_270": ("maze_inside_wall", -90),

    "four_wall": ("maze_four_wall", 0),
}

N = [1, 3, 5, 7, 9, 11, 13, 15]
S = [4, 5, 6, 7, 12, 13, 14, 15]
E = [2, 3, 6, 7, 10, 11, 14, 15]
W = [8, 9, 10, 11, 12, 13, 14, 15]

class MazeFactory:
    def __init__(self) -> None:
        self._maze_class = load_mazegenerator()

    def generate_maze(
        self, width: int, height: int, textures: dict,
        screen_width: int, screen_height: int, renderer
    ) -> list[list[int]]:
        tile_size = min(
            screen_width // width,
            screen_height // height
        ) - 5

        maze = self._maze_class((width, height))
        grid = maze._maze

        wall_data: list[tuple[str, float, float, float]] = []
        offset_x = (screen_width - width * tile_size) // 2
        offset_y = (screen_height - height * tile_size) // 2
        self.wall_sprites_list: list[str] = []

        for row_index, row in enumerate(grid):
            for col_index, cell_value in enumerate(row):

                x, y = self.get_pixel_coordinates(
                    col_index, row_index, tile_size, height, offset_x, offset_y
                )

                n = cell_value in N
                s = cell_value in S
                e = cell_value in E
                w = cell_value in W

                keys = []

                if not n and not e:
                    keys.append("inside_wall_180")
                if not w and not n:
                    keys.append("inside_wall_90")
                if not s and not w:
                    keys.append("inside_wall")
                if not e and not s:
                    keys.append("inside_wall_270")
                if n and e:
                    keys.append("corner")
                if s and e:
                    keys.append("corner_90")
                if n and w:
                    keys.append("corner_270")
                if s and w:
                    keys.append("corner_180")
                if n and not e and not w:
                    keys.append("wall")
                if n and e and w:
                    keys.append("triple_wall")
                if w and n and s:
                    keys.append("triple_wall_270")
                if s and e and w:
                    keys.append("triple_wall_180")
                if e and n and s:
                    keys.append("triple_wall_90")
                if s and not e and not w:
                    keys.append("wall_180")
                if w and not n and not s:
                    keys.append("wall_270")
                if e and not n and not s:
                    keys.append("wall_90")
                if n and s and e and w:
                    keys.append("four_wall")

                for key in keys:
                    sprite_name, angle = WALL_SPRITES[key]

                    sprite_path = str(textures[sprite_name])
                    self.wall_sprites_list.append(str(textures[sprite_name]))

                    wall_data.append((sprite_path, angle, x, y, tile_size))

        return wall_data


    def get_pixel_coordinates(
        self, col: int, row: int, tile_size: tuple[float, float], height: int,
        offset_x: int, offset_y: int
    ) -> tuple[int, int]:

        x = col * tile_size + tile_size / 2 + offset_x
        y = (height - 1 - row) * tile_size + tile_size / 2 + offset_y

        return (x, y)


def generate_ascii_maze(grid: Any, width, height) -> dict:
    rows = 2 * height + 1
    cols = 2 * width + 1
    ascii_grid = [[1] * cols for _ in range(rows)]
    close_or_open = {}

    for row_index, row in enumerate(grid):
        for col_index, cell_value in enumerate(row):
            n = cell_value in N
            s = cell_value in S
            e = cell_value in E
            w = cell_value in W

            ay = row_index * 2 + 1
            ax = col_index * 2 + 1

            ascii_grid[ay][ax] = 0

            if not n and row_index > 0:
                new_ay = ay - 1
                new_ax = ax
                ascii_grid[new_ay][new_ax] = 0
            if not s and row_index < height - 1:
                new_ay = ay + 1
                new_ax = ax
                ascii_grid[new_ay][new_ax] = 0
            if not e and col_index < width - 1:
                new_ay = ay
                new_ax = ax +1
                ascii_grid[new_ay][new_ax] = 0
            if not w and col_index > 0:
                new_ay = ay
                new_ax = ax - 1
                ascii_grid[new_ay][new_ax] = 0
    ascii_maze = []
    for row in ascii_grid:
        print("".join("1" if c == 1 else "0" for c in row))
        ascii_maze.append("".join("1" if c == 1 else "0" for c in row))

    for row_index, row in enumerate(ascii_maze):
        for col_index, cell_value in enumerate(row):
            close_or_open[(row_index, col_index)] = cell_value

    return close_or_open
