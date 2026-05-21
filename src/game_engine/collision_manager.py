# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  collision_manager.py                              :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 20:04:13 by roandrie        #+#    #+#               #
#  Updated: 2026/05/21 15:02:19 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any

from src.entity import Entity, Player


class CollisionManager():
    def __init__(
        self,
        player_reference: Player,
        enemies_reference: list[str, Any],
        maze_bitemap: dict[tuple[int, int], str],
        offset_x: int, offset_y: int, tile_size: int, maze_height: int
    ) -> None:

        self.player_reference = player_reference
        self.enemies_reference = enemies_reference
        self.maze_bitemap = maze_bitemap

        self.offset_x = offset_x
        self.offset_y = offset_y
        self.tile_size = tile_size
        self.maze_height = maze_height

    def update(self) -> None:
        # Check the collisions for the player
        direction = self.player_reference._current_direction

        # Check the collisions for the player
        if direction != (0.0, 0.0):
            if not self.check_for_collisions(self.player_reference, direction):
                self.player_reference._current_direction = (0.0, 0.0)
            else:
                self.snap_to_grid(self.player_reference, direction)

    def check_for_collisions(
        self, entity: Entity, direction: tuple[int, int]
    ) -> bool:
        # Get the entity position (x, y) and convert them from pixel coords to
        # grid coords
        pos_x: int = int((entity.x - self.offset_x) // self.tile_size)
        pos_y: int = int((self.maze_height - 1) -
                            ((entity.y - self.offset_y) // self.tile_size))

        # Calculation of the extended grid
        ext_x: int = (pos_x * 2) + 1
        ext_y: int = (pos_y * 2) + 1

        # Inverted Y (because Arcade Y=0 is bottom right)
        wall_x: int = ext_x + direction[0]
        wall_y: int = ext_y - direction[1]

        # Check if the destination is open
        if self.maze_bitemap.get((wall_x, wall_y), 1) == 0:
            return True
        return False

    def snap_to_grid(self, entity: Entity,
                     direction: tuple[float, float]) -> None:
        # Calculate the exact center of the current tile
        center_x: int = (((entity.x - self.offset_x) // self.tile_size) *
                    self.tile_size + (self.tile_size / 2) + self.offset_x)
        center_y: int = (((entity.y - self.offset_y) // self.tile_size) *
                    self.tile_size + (self.tile_size / 2) + self.offset_y)

        # Lock the perpendicular axis
        if direction == 0.0 and direction != 0.0:
            # Vertical movement: lock X to the center of the column
            entity.x = center_x
        elif direction == 0.0 and direction != 0.0:
            # Horizontal movement: lock Y to the center of the row
            entity.y = center_y


    # detect player and collectibles
    # detect player and enemy
