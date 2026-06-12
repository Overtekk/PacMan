# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  Cat_brain.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/09 11:39:21 by roandrie        #+#    #+#               #
#  Updated: 2026/06/12 10:34:55 by roandrie        ###   ########.fr        #
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
        self.enemy.mode = EnemyState.SEARCH
        if self.enemy._is_edible and not self.enemy.died:
            if self.enemy.mode in [EnemyState.RESPAWN, EnemyState.RUNAWAY]:
                return

        if game_config.debug_mode:
            if hasattr(self.enemy, '_debug_pathfinding'):
                if self.enemy.mode != EnemyState.SEARCH:
                    if len(self.enemy._debug_pathfinding) > 0:
                        self.enemy._debug_pathfinding.clear()

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
        target_grid = (player_x, player_y)

        if self.enemy.maze_bitmap.get((player_x + 1, player_y), 1) == 0:
            target_grid = (player_x + 1, player_y)

        elif self.enemy.maze_bitmap.get((player_x + 2, player_y), 1) == 0:
            target_grid = (player_x + 2, player_y)

        elif self.enemy.maze_bitmap.get((player_x - 1, player_y), 1) == 0:
            target_grid = (player_x - 1, player_y)

        elif self.enemy.maze_bitmap.get((player_x - 2, player_y), 1) == 0:
            target_grid = (player_x - 2, player_y)

        elif self.enemy.maze_bitmap.get((player_x, player_y + 1), 1) == 0:
            target_grid = (player_x, player_y + 1)

        elif self.enemy.maze_bitmap.get((player_x, player_y + 2), 1) == 0:
            target_grid = (player_x, player_y + 2)

        elif self.enemy.maze_bitmap.get((player_x, player_y - 1), 1) == 0:
            target_grid = (player_x, player_y - 1)

        elif self.enemy.maze_bitmap.get((player_x, player_y - 2), 1) == 0:
            target_grid = (player_x, player_y - 2)

        print(f'player pos={self.enemy.calculator.get_pixel_to_grid_entity(self.enemy.player_ref)} | target grid={target_grid}')
        return target_grid
