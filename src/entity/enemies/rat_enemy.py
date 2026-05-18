# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  rat_enemy.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:04:53 by roandrie        #+#    #+#               #
#  Updated: 2026/05/18 10:35:33 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from ..entity import Entity, Movable, Enemy


class RatEnemy(Entity, Movable, Enemy):
    def __init__(
        self, spawn_point: tuple[int, int],
        sprite_path: str,
        scale: float = 1.0,
        speed: float = 100.0,
        is_edible: bool = False
    ) -> None:

        Entity.__init__(
            self,
            spawn_point=spawn_point,
            sprite_path_or_texture=sprite_path,
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
