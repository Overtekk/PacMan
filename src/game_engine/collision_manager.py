# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  collision_manager.py                              :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 20:04:13 by roandrie        #+#    #+#               #
#  Updated: 2026/05/21 11:41:25 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any

from src.entity import Entity, Player
from src.renderer.screen_settings import ScreenSettings


class CollisionManager():
    def __init__(
        self,
        player_reference: Player,
        enemies_reference: list[str, Any],
        maze_bitemap: dict[tuple[int, int], str],
    ) -> None:

        self.player_reference: Player = player_reference
        self.enemies_reference: list[str, Any] = enemies_reference
        self.maze_bitemap: dict[tuple[int, int], str] = maze_bitemap

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
        pos_x: int = int((entity.x - ScreenSettings.OFFSET_X) //
                            ScreenSettings.TILE_SIZE)
        pos_y: int = int((entity.y - ScreenSettings.OFFSET_Y) //
                            ScreenSettings.TILE_SIZE)

        # Add the direction to the actual position, and convert back to pixel
        # coords
        dest_x: int = ((pos_x + direction[0]) * 2) + 1
        dest_y: int = ((pos_y + direction[1]) * 2) + 1

        # Check if the destination is open
        if self.maze_bitemap[dest_x, dest_y] == 0:
            return True
        return False

    # use check_for_collisions_with_list to handle all collisions
    # avoid player and ennemis to travel throught walls
    # detect player and collectibles
    # detect player and enemy
