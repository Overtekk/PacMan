# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  calculator.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/25 18:21:02 by roandrie        #+#    #+#               #
#  Updated: 2026/05/25 18:53:50 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any


class SuperCalculator():
    def __init__(
        self,
        maze_offset_x: float, maze_offset_y: float,
        maze_tile_size: float, maze_height: int
    ) -> None:

        self.maze_offset_x = maze_offset_x
        self.maze_offset_y = maze_offset_y
        self.maze_tile_size = maze_tile_size
        self.maze_height = maze_height

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
