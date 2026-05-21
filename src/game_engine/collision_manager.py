# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  collision_manager.py                              :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 20:04:13 by roandrie        #+#    #+#               #
#  Updated: 2026/05/21 14:12:04 by roandrie        ###   ########.fr        #
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
        if self.player_reference._current_direction != (0, 0):
            if not self.check_for_collisions(
                self.player_reference,
                self.player_reference._current_direction
            ):
                self.player_reference._current_direction = (0, 0)

    def check_for_collisions(
        self, entity: Entity, direction: tuple[int, int]
    ) -> bool:
        # Get the entity position (x, y) and convert them from pixel coords to
        # grid coords
        pos_x: int = int((entity.x - self.offset_x) // self.tile_size)
        pos_y: int = int((self.maze_height - 1) -
                            ((entity.y - self.offset_y) // self.tile_size))

        # Add the direction to the actual position, and convert back to pixel
        # coords
        dest_x: int = ((pos_x + direction[0]) * 2) + 1
        dest_y: int = ((pos_y - direction[1]) * 2) + 1

        # Check if the destination is open
        if self.maze_bitemap[dest_x, dest_y] == 0:
            return True
        return False

    # use check_for_collisions_with_list to handle all collisions
    # avoid player and ennemis to travel throught walls
    # detect player and collectibles
    # detect player and enemy
