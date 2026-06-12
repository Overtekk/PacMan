# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  Cat_brain.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/09 11:39:21 by roandrie        #+#    #+#               #
#  Updated: 2026/06/12 15:40:16 by roandrie        ###   ########.fr        #
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
    def __init__(self, enemy: 'CatEnemy') -> None:
        super().__init__(enemy)

    def update(self, delta_time: float) -> None:
        if self.enemy._is_edible and not self.enemy.died:
            if self.enemy.mode in [EnemyState.RESPAWN, EnemyState.RUNAWAY]:
                return

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
        update_coords: list[tuple[float, float]] = self._update_coords()

        self._go_to_position_better(update_coords)

    def _update_coords(self) -> tuple[int, int]:
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
        player_dir_x = int(player_pos[0] + (player_curr_dir[0] * distance))
        player_dir_y = int(player_pos[1] + (player_curr_dir[1] * distance))

        if maze_bitmap.get((player_dir_x, player_dir_y), 1) == 0:
            return (player_dir_x, player_dir_y)

        return None
