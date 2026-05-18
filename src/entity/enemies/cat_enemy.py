# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  cat_enemy.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:04:41 by roandrie        #+#    #+#               #
#  Updated: 2026/05/18 15:38:21 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade
import random

from ..entity import Enemy


class CatEnemy(Enemy):
    def __init__(
        self, spawn_point: tuple[int, int],
        sprite_sheet: list[arcade.Texture],
        scale: float = 1.0,
        speed: float = 100.0,
        is_edible: bool = False
    ) -> None:

        super().__init__(
            spawn_point=spawn_point,
            sprite_sheet=sprite_sheet,
            scale=scale,
            speed=speed,
            is_edible=is_edible
        )

    def update(self, delta: float) -> None:
        self.algo_random_direction(delta)
        super().update(delta)

    def algo_random_direction(self, delta: float) -> None:
        self._move_timer += delta

        if self._move_timer > 1:

            random_direction: int = random.randint(0, 3)

            direction: tuple[float, float] = (0, 0)

            match random_direction:
                case 0:
                    direction = (0, 1)

                case 1:
                    direction = (0, -1)

                case 2:
                    direction = (1, 0)

                case 3:
                    direction = (-1, 0)

            self.move(direction)

            self._move_timer = 0

    def die(self) -> None:
        pass
