# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  Fox_brain.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/08 11:42:52 by roandrie        #+#    #+#               #
#  Updated: 2026/06/08 13:25:05 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from .brain import EnemyBrain
from ..logics.StateMachine import EnemyState
from src import game_config
from src.utils import print_log

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.entity.enemies.fox_enemy import FoxEnemy


class FoxBrain(EnemyBrain):
    def __init__(self, enemy: 'FoxEnemy') -> None:
        super().__init__(enemy)

        self.detection_radius: float = (game_config.fox_detection_radius *
                                        self.enemy.calculator.maze_tile_size)

    def update(self, delta_time: float) -> None:
        if self.enemy.mode in [EnemyState.WANDER, EnemyState.CHASE]:
            updated_coords: list[tuple[float, float]] = self._update_coords()

            radius_distance: float = (
                self.enemy.calculator.get_euclidean_distance(updated_coords[0],
                                                             updated_coords[1])
                )

            if radius_distance > self.detection_radius:
                self.enemy.mode == EnemyState.CHASE

                if game_config.debug_mode:
                    print_log(f"Changed state for {self.enemy} to CHASE")

            else:
                self.enemy.mode == EnemyState.WANDER

                if game_config.debug_mode:
                    print_log(f"Changed state for {self.enemy} to WANDER")

        super().update(delta_time)

    # :---------------:
    #  PRIVATE METHODS
    # :---------------:

    def _update_coords(self) -> list[tuple[float, float]]:
        coords: list[tuple[float, float]] = []

        self_pxl_coords: tuple[float, float] = (
            self.enemy.x, self.enemy.y
        )
        coords.append(self_pxl_coords)

        player_pxl_coords: tuple[float, float] = (
            self.enemy.player_ref.x, self.enemy.player_ref.y
        )
        coords.append(player_pxl_coords)

        return coords

