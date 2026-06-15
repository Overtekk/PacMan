# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  Cat_brain.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/09 11:39:21 by roandrie        #+#    #+#               #
#  Updated: 2026/06/15 08:45:24 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from .brain import EnemyBrain
from ..logics.StateMachine import EnemyState
from src import game_config
from src.utils import print_log

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.entity.enemies.cat_enemy import CatEnemy


class CatBrain(EnemyBrain):
    """
    Brain implementation specialized for Cat entitie.

    Feature search mode to find the player at all time.
    """

    def __init__(self, enemy: 'CatEnemy') -> None:
        """
        Initialize the cat brain and calculate its search thresholds.

        Args:
            enemy (CatEnemy): Controlled enemy entity reference.
        """
        super().__init__(enemy)

    def update(self, delta_time: float) -> None:
        """
        Overload update to add the search state.

        Args:
            delta_time (float): Time elapsed since the last frame update.
        """
        if game_config.debug_mode:
            if hasattr(self.enemy, '_debug_pathfinding'):
                if self.enemy.mode != EnemyState.SEARCH:
                    if len(self.enemy._debug_pathfinding) > 0:
                        self.enemy._debug_pathfinding.clear()

        if self.enemy.mode == EnemyState.WANDER:
            if self.enemy.mode != EnemyState.SEARCH:
                self.enemy.mode = EnemyState.SEARCH

                if game_config.debug_mode:
                        print_log(f"Changed state for {self.enemy} to SEARCH")

        super().update(delta_time)

    # :---------------:
    #  PRIVATE METHODS
    # :---------------:

    def _execute_search_state(self):
        """
        Get the updated coords from the player and call the pathfinding method.
        """
        update_coords: list[tuple[float, float]] = self._update_coords()

        self._go_to_position_better(update_coords)

    def _update_coords(self) -> tuple[int, int]:
        """
        Find the player coords and check if the cell +2 in front of him can be
        access, if not take the cell +1, or the player position.

        Returns:
            tuple[int, int]: the new player coordinates.
        """
        # Get the player grid coords
        player_coords_raw: tuple[int, int] = (
            self.enemy.calculator.get_pixel_to_grid_entity(
                self.enemy.player_ref
            ))
        player_x, player_y = (
            int(player_coords_raw[0]), int(player_coords_raw[1])
        )
        player_pos = (player_x, player_y)

        # Shorter variables
        player_curr_dir_x = int(self.enemy.player_ref.current_direction[0])
        player_curr_dir_y = int(self.enemy.player_ref.current_direction[1])
        player_curr_dir = (player_curr_dir_x, player_curr_dir_y)
        maze_bitmap = self.enemy.maze_bitmap

        # - CHECK IF WALL EXIST BETWEEN PLAYER AND CELL +1
        res_1 = self._check_cell(player_pos, player_curr_dir, maze_bitmap, 1)
        if res_1 is None:
            return (player_x, player_y)

        # - CHECK WITH MAX DISTANCE -
        res = self._check_cell(player_pos, player_curr_dir, maze_bitmap, 2)
        if res is not None:
            return res

        return res_1

    def _check_cell(
        self, player_pos: tuple[int, int], player_curr_dir: tuple[int, int],
        maze_bitmap: dict[tuple[int, int], int], distance: int
    ) -> tuple[int, int]:
        """Check if a cell is a close or open.

        Args:
            player_pos (tuple[int, int]): the player position
            player_curr_dir (tuple[int, int]): the current facing direction of
                                               the player.
            maze_bitmap (dict[tuple[int, int], int]): the bitmap of the maze
            distance (int): distance to check

        Returns:
            tuple[int, int]: player coords if wall is open, None if not.
        """
        player_dir_x = int(player_pos[0] + (player_curr_dir[0] * distance))
        player_dir_y = int(player_pos[1] + (player_curr_dir[1] * distance))

        if maze_bitmap.get((player_dir_x, player_dir_y), 1) == 0:
            return (player_dir_x, player_dir_y)

        return None
