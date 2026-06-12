# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  calculator.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/25 18:21:02 by roandrie        #+#    #+#               #
#  Updated: 2026/06/12 11:34:33 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any

from math import sqrt


class SuperCalculator():
    """Utility class for coordinate conversion and distance calculations.

    Handles all conversions between pixel coordinates used by Arcade
    and the grid coordinates used internally by the maze and AI logic.

    Attributes:
        maze_offset_x (float): Horizontal pixel offset of the maze origin.
        maze_offset_y (float): Vertical pixel offset of the maze origin.
        maze_tile_size (float): Size of a single tile in pixels.
        maze_height (int): Height of the maze in tiles.
    """
    def __init__(
        self,
        maze_offset_x: float, maze_offset_y: float,
        maze_tile_size: float, maze_height: int,
    ) -> None:
        """Initialize the SuperCalculator with maze layout parameters.

        Args:
            maze_offset_x (float): Horizontal pixel offset of the maze origin.
            maze_offset_y (float): Vertical pixel offset of the maze origin.
            maze_tile_size (float): Size of a single tile in pixels.
            maze_height (int): Height of the maze in tiles.
        """

        self.maze_offset_x = maze_offset_x
        self.maze_offset_y = maze_offset_y
        self.maze_tile_size = maze_tile_size
        self.maze_height = maze_height

    def get_pixel_to_grid_entity(self, entity: Any) -> tuple[float, float]:
        """Convert an entity's pixel position to extended grid coordinates.

        Args:
            entity (Any): Any entity with x and y pixel attributes.

        Returns:
            tuple[float, float]: The (x, y) position in the extended grid.
        """
        # Convert pixels to grid
        pos_x: int = int(
            (entity.x - self.maze_offset_x) // self.maze_tile_size
        )
        pos_y: int = int(
            (self.maze_height - 1) -
            ((entity.y - self.maze_offset_y) // self.maze_tile_size))

        # Convert index to extended grid
        convert_x: int = (pos_x * 2) + 1
        convert_y: int = (pos_y * 2) + 1

        return (convert_x, convert_y)

    def get_pixel_to_grid_any(self, x: float, y: float) -> tuple[float, float]:
        """Convert arbitrary pixel coordinates to extended grid coordinates.

        Args:
            x (float): Pixel x coordinate.
            y (float): Pixel y coordinate.

        Returns:
            tuple[float, float]: The (x, y) position in the extended grid.
        """
        # Convert pixels to grid
        pos_x: int = int((x - self.maze_offset_x) // self.maze_tile_size)
        pos_y: int = int(
            (self.maze_height - 1) -
            ((y - self.maze_offset_y) // self.maze_tile_size))

        # Convert index to extended grid
        convert_x: int = (pos_x * 2) + 1
        convert_y: int = (pos_y * 2) + 1

        return (convert_x, convert_y)

    def get_grid_to_pixel(self, x: float, y: float) -> tuple[int, int]:
        """Convert normal grid coordinates to pixel coordinates.

        Args:
            x (float): Grid x coordinate.
            y (float): Grid y coordinate.

        Returns:
            tuple[int, int]: The center pixel (x, y) of the corresponding tile.
        """

        new_x: float = (
            (x * self.maze_tile_size) +
            self.maze_tile_size / 2 + self.maze_offset_x
        )
        new_y: float = (
            (self.maze_height - 1 - y) *
            self.maze_tile_size + self.maze_tile_size / 2 + self.maze_offset_y
        )

        return (int(new_x), int(new_y))

    def get_euclidean_distance(
        self, point1: tuple[float, float], point2: tuple[float, float]
    ) -> float:
        """Compute the Euclidean distance between two points.

        Args:
            point1 (tuple[float, float]): First point as (x, y).
            point2 (tuple[float, float]): Second point as (x, y).

        Returns:
            float: The Euclidean distance between the two points.
        """
        distance: float = 0.0

        for i in range(len(point1)):
            distance += (point2[i] - point1[i]) ** 2
        return sqrt(distance)

    def check_open_wall(
        self, x: int, y: int, maze_bitemap: dict[tuple[int, int], int],
    ) -> dict[tuple[float, float], tuple[int, int]]:
        """Return all open neighbouring cells from a given extended grid
        position.

        Checks the four cardinal neighbours (N, S, E, W) in the extended
        maze bitmap and returns those that are passable (value 0).

        Args:
            x (int): Extended grid x coordinate of the current cell.
            y (int): Extended grid y coordinate of the current cell.
            maze_bitemap (dict[tuple[int, int], int]): The maze bitmap where
                0 means open and 1 means wall.

        Returns:
            dict[tuple[float, float], tuple[int, int]]: Mapping from direction
                vector to the extended grid coordinates of the open neighbour.
        """
        open_wall: dict[tuple[float, float], tuple[int, int]] = {}

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
