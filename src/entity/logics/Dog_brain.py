# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  Dog_brain.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/10 11:49:59 by anacharp        #+#    #+#               #
#  Updated: 2026/06/12 09:42:32 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import random

from .brain import EnemyBrain
from ..logics.StateMachine import EnemyState
from src import game_config
from src.utils import print_log

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.entity.enemies.dog_enemy import DogEnemy


class DogBrain(EnemyBrain):
    def __init__(self, enemy: 'DogEnemy') -> None:
        super().__init__(enemy)

        self._get_radius()

    def update(self, delta_time: float) -> None:
        if not self.enemy.is_edible and not self.enemy.died:
            if self.enemy.mode in [EnemyState.RESPAWN, EnemyState.RUNAWAY]:
                pass

        elif self.enemy.mode == EnemyState.WANDER:
            updated_coords: list[tuple[float, float]] = self._update_coords()

            radius_distance: float = (
                self.enemy.calculator.get_euclidean_distance(updated_coords[0],
                                                             updated_coords[1])
                )

            if radius_distance > self.detection_radius:
                if self.enemy.mode != EnemyState.SEARCH:
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

        if (self.enemy.player_ref.sprite.angle == 0
           and self.enemy.player_ref.sprite.scale_x >= 0):
            player_pxl_coords: tuple[float, float] = (
                self.enemy.player_ref.x + 2, self.enemy.player_ref.y
            )
            coords.append(player_pxl_coords)
        elif (self.enemy.player_ref.sprite.angle == 0
              and self.enemy.player_ref.sprite.scale_x <= 0):
            player_pxl_coords: tuple[float, float] = (
                self.enemy.player_ref.x - 2, self.enemy.player_ref.y
            )
            coords.append(player_pxl_coords)
        elif (self.enemy.player_ref.sprite.angle == 90
              and self.enemy.player_ref.sprite.scale_x >= 0):
            player_pxl_coords: tuple[float, float] = (
                self.enemy.player_ref.x, self.enemy.player_ref.y + 2
            )
            coords.append(player_pxl_coords)
        elif (self.enemy.player_ref.sprite.angle == -90
              and self.enemy.player_ref.sprite.scale_x >= 0):
            player_pxl_coords: tuple[float, float] = (
                self.enemy.player_ref.x, self.enemy.player_ref.y - 2
            )
            coords.append(player_pxl_coords)
        return coords

    def _get_radius(self) -> None:
        highest_x: int = float('-inf')

        for coords in self.enemy.maze_bitmap:
            x: int = coords[0]

            if highest_x < x:
                highest_x = x

        self.radius: float = highest_x * game_config.dog_detection_radius
        self.detection_radius: float = (
            self.radius * self.enemy.calculator.maze_tile_size
        )

    def _go_to_position(self, pos_x: float, pos_y: float) -> None:
        open_walls = self._get_available_moves()
        if not open_walls:
            return

        # Pop single available move immediately to skip loop
        if len(open_walls) == 1:
            self.enemy._next_direction = list(open_walls.keys()).pop()
            return

        conv_pos: tuple[float, float] = (
            self.enemy.calculator.get_pixel_to_grid_any(pos_x, pos_y)
        )

        best_distance: float = float('inf')
        direction: tuple[float, float] = (0.0, 0.0)
        TURN_PENALTY: float = 0.2

        random_percent: float = 0.6
        if self.enemy.mode == EnemyState.CHASE:
            random_percent == 0.4
        if random.random() < random_percent:
            direction = random.choice(list(open_walls.keys()))
        else:
            for key, coords in open_walls.items():
                distance: float = self.enemy.calculator.get_euclidean_distance(
                    coords, conv_pos
                )

                # Apply momentum penalty if the path forces a turn
                if (key != self.enemy.current_direction and
                        self.enemy.current_direction != (0.0, 0.0)):
                    distance += TURN_PENALTY

                if distance < best_distance:
                    best_distance = distance
                    direction = key

        self.enemy._next_direction = direction
