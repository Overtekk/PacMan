# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  calculator.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/25 18:21:02 by roandrie        #+#    #+#               #
#  Updated: 2026/05/27 13:28:46 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any

from math import sqrt


class SuperCalculator():
    def __init__(
        self,
        maze_offset_x: float, maze_offset_y: float,
        maze_tile_size: float, maze_height: int,
        debug_mode: bool
    ) -> None:

        self.maze_offset_x = maze_offset_x
        self.maze_offset_y = maze_offset_y
        self.maze_tile_size = maze_tile_size
        self.maze_height = maze_height

        self.debug_mode = debug_mode

    def get_pixel_to_grid_entity(self, entity: Any) -> tuple[float, float]:
        # Convert pixels to grid
        pos_x: int = int(
            (entity.x - self.maze_offset_x) // self.maze_tile_size
        )
        pos_y: int = int(
            (self.maze_height - 1) -
                ((entity.y - self.maze_offset_y) // self.maze_tile_size)
        )

        # Convert index to extended grid
        convert_x: int = (pos_x * 2) + 1
        convert_y: int = (pos_y * 2) + 1

        return (convert_x, convert_y)

    def get_pixel_to_grid_any(self, x: float, y: float) -> tuple[float, float]:
        # Convert pixels to grid
        pos_x: int = int((x - self.maze_offset_x) // self.maze_tile_size)
        pos_y: int = int(
            (self.maze_height - 1) -
                ((y - self.maze_offset_y) // self.maze_tile_size)
        )

        # Convert index to extended grid
        convert_x: int = (pos_x * 2) + 1
        convert_y: int = (pos_y * 2) + 1

        return (convert_x, convert_y)

    def get_grid_to_pixel(self, x: int, y: int) -> tuple[float, float]:

        x = (x * self.maze_tile_size + self.maze_tile_size / 2 + self.maze_offset_x)
        y = ((self.maze_height - 1 - y) * self.maze_tile_size + self.maze_tile_size / 2 + self.maze_offset_y)

        return (x, y)

    def get_euclidean_distance(
        self, point1: tuple[float, float], point2: tuple[float, float]
    ) -> float:
        distance: float = 0.0

        for i in range(len(point1)):
            distance += (point2[i] - point1[i]) ** 2
        return sqrt(distance)

    def check_open_wall(
        self, x: int, y: int, maze_bitemap: dict[tuple[int, int], int],
    ) -> dict[tuple[int, int], tuple[int, int]]:
        open_wall: dict[tuple[int, int], tuple[int, int]] = {}

        # West
        if maze_bitemap[(x + 1, y)] == 0:
            open_wall[(1, 0)] = (x + 1, y)

        # East
        if maze_bitemap[(x - 1, y)] == 0:
            open_wall[(-1, 0)] = (x - 1, y)

        # South
        if maze_bitemap[(x, y + 1)] == 0:
            open_wall[(0, -1)] = (x, y + 1)

        # North
        if maze_bitemap[(x, y - 1)] == 0:
            open_wall[(0, 1)] = (x, y - 1)

        return open_wall
