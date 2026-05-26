# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  fox_enemy.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 18:54:32 by roandrie        #+#    #+#               #
#  Updated: 2026/05/26 10:12:50 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from ..entity import Enemy
from src.utils import SuperCalculator


class FoxEnemy(Enemy):
    def __init__(
        self, spawn_point: tuple[int, int],
        sprite_sheet_move: list[arcade.Texture],
        sprite_sheet_eatable: list[arcade.Texture],
        sprite_sheet_died: list[arcade.Texture],
        maze_bitmap: dict[tuple[int, int], str],
        calculator: SuperCalculator,
        scale: float = 1.0,
        speed: float = 100.0,
        is_edible: bool = False
    ) -> None:

        super().__init__(
            spawn_point=spawn_point,
            sprite_sheet_move=sprite_sheet_move,
            sprite_sheet_eatable=sprite_sheet_eatable,
            sprite_sheet_died=sprite_sheet_died,
            maze_bitmap=maze_bitmap,
            calculator=calculator,
            scale=scale,
            speed=speed,
            is_edible=is_edible
        )

        self.sprite.texture = self.textures[1]

    def die(self) -> None:
        pass
