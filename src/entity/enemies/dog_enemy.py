# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  dog_enemy.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:05:06 by roandrie        #+#    #+#               #
#  Updated: 2026/05/18 13:12:31 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from ..entity import Enemy


class DogEnemy(Enemy):
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

    def die(self) -> None:
        pass
