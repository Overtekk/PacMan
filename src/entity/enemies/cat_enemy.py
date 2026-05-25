# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  cat_enemy.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:04:41 by roandrie        #+#    #+#               #
#  Updated: 2026/05/25 18:33:03 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from ..entity import Enemy
from src.utils import SuperCalculator


class CatEnemy(Enemy):
    def __init__(
        self, spawn_point: tuple[int, int],
        sprite_sheet: list[arcade.Texture],
        maze_bitmap: dict[tuple[int, int], str],
        calculator: SuperCalculator,
        scale: float = 1.0,
        speed: float = 100.0,
        is_edible: bool = False
    ) -> None:

        super().__init__(
            spawn_point=spawn_point,
            sprite_sheet=sprite_sheet,
            maze_bitmap=maze_bitmap,
            calculator=calculator,
            scale=scale,
            speed=speed,
            is_edible=is_edible
        )

    def die(self) -> None:
        pass
