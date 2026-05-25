# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  calculator.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/25 18:21:02 by roandrie        #+#    #+#               #
#  Updated: 2026/05/25 18:25:47 by roandrie        ###   ########.fr        #
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

    def get_pixel_to_grid(self, entity: Any) -> tuple[float, float]:
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
