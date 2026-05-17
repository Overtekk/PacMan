# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  fox_enemy.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 18:54:32 by roandrie        #+#    #+#               #
#  Updated: 2026/05/17 16:01:18 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from ..entity import Entity, Movable, Enemy


class FoxEnemy(Entity, Movable, Enemy):
    def __init__(
        self, spawn_point: tuple[int, int],
        sprite_path: str,
        scale: float = 1.0,
        speed: float = 0.0,
        is_edible: bool = False
    ) -> None:

        Entity.__init__(
            self,
            spawn_point=spawn_point,
            sprite_path=sprite_path,
            scale=scale
        )

        Movable.__init__(
            self, speed=speed
        )

        Enemy.__init__(
            self, is_edible=is_edible
        )

    def update(delta: float) -> None:
        pass

    def move(self, direction: tuple[float, float]) -> None:
        pass
