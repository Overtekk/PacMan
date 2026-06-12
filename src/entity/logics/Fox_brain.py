# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  Fox_brain.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/08 11:42:52 by roandrie        #+#    #+#               #
#  Updated: 2026/06/12 10:26:19 by anacharp        ###   ########.fr        #
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

        self._get_radius()

    def update(self, delta_time: float) -> None:
        if (self.enemy.angry and not self.enemy.is_edible
           and not self.enemy.died):
            if self.enemy.mode in [EnemyState.RESPAWN, EnemyState.RUNAWAY]:
                return

            elif self.enemy.mode != EnemyState.ANGRY:
                self.enemy.mode = EnemyState.ANGRY

                if game_config.debug_mode:
                    print_log(f"Changed state for {self.enemy} to ANGRY")

        elif self.enemy.mode == EnemyState.WANDER:
            updated_coords: list[tuple[float, float]] = self._update_coords()

            radius_distance: float = (
                self.enemy.calculator.get_euclidean_distance(updated_coords[0],
                                                             updated_coords[1])
                )

            if radius_distance > self.detection_radius:
                self.enemy.mode = EnemyState.SEARCH

                if game_config.debug_mode:
                    print_log(f"Changed state for {self.enemy} to SEARCH")

            else:
                if self.enemy.mode != EnemyState.WANDER:
                    self.enemy.mode = EnemyState.WANDER

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

    def _get_radius(self) -> None:
        highest_x: float = float('-inf')

        for coords in self.enemy.maze_bitmap:
            x: int = coords[0]

            if highest_x < x:
                highest_x = x

        self.radius: float = highest_x * game_config.fox_detection_radius
        self.detection_radius: float = (
            self.radius * self.enemy.calculator.maze_tile_size
        )
