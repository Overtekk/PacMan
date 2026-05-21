# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  collision_manager.py                              :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 20:04:13 by roandrie        #+#    #+#               #
#  Updated: 2026/05/21 15:17:56 by roandrie        ###   ########.fr        #
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
        direction: tuple[float, float] = (
            self.player_reference._current_direction
        )

        # If the player is not moving, do nothing
        if direction == (0.0, 0.0):
            return

        # Get the exact center of the current tile
        center_x, center_y = self._get_tile_center(self.player_reference)

        # Check if there is a wall in front
        path_is_clear = self._check_for_collisions(self.player_reference,
                                                   direction)

        if not path_is_clear:
            dx, dy = direction
            stop_x: bool = False
            stop_y: bool = False

            # Check if the player has reached or passed the center on their
            # movement axis
            if dx > 0 and self.player_reference.x >= center_x:
                stop_x = True
            elif dx < 0 and self.player_reference.x <= center_x:
                stop_x = True

            if dy > 0 and self.player_reference.y >= center_y:
                stop_y = True
            elif dy < 0 and self.player_reference.y <= center_y:
                stop_y = True

            # If the center is reached, snap to it and stop
            if stop_x or stop_y:
                self.player_reference.x = center_x
                self.player_reference.y = center_y
                self.player_reference._current_direction = (0.0, 0.0)

        else:
            # Snap the player
            # Path is clear, lock the perpendicular axis
            dx, dy = direction

            # Vertical movement: lock X to the center
            if dy != 0 and dx == 0:
                self.player_reference.x = center_x

            # Horizontal movement: lock Y to the center
            elif dx != 0 and dy == 0:
                self.player_reference.y = center_y

    # :---------------:
    #  PRIVATE METHODS
    # :---------------:

    def _check_for_collisions(
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

    def _snap_to_grid(self, entity: Entity,
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

    def _get_tile_center(self, entity: Entity) -> tuple[float, float]:
        # Calculate X center
        logic_x = (entity.x - self.offset_x) // self.tile_size
        center_x = ((logic_x * self.tile_size) + (self.tile_size / 2) +
                        self.offset_x)

        # Calculate Y center
        logic_y = (entity.y - self.offset_y) // self.tile_size
        center_y = ((logic_y * self.tile_size) + (self.tile_size / 2) +
                        self.offset_y)

        return center_x, center_y


    # detect player and collectibles
    # detect player and enemy
