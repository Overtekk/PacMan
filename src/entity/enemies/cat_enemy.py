# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  cat_enemy.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:04:41 by roandrie        #+#    #+#               #
#  Updated: 2026/05/14 21:31:10 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from pathlib import Path

from ..entity import Entity, Movable, Enemy

class CatEnemy(Entity, Movable, Enemy):
    def __init__(
        self, spawn_point: tuple[int, int],
        sprite_path: Path,
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
