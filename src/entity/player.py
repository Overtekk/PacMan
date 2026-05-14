# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  player.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 18:40:42 by roandrie        #+#    #+#               #
#  Updated: 2026/05/14 21:30:12 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from pathlib import Path

from .entity import Entity, Movable

class Player(Entity, Movable):
    def __init__(
        self, spawn_point: tuple[int, int],
        sprite_path: Path,
        scale: float = 1.0,
        speed: float = 0.0,
        lives: int = 3
    ) -> None:

        Entity.__init__(
            self,
            spawn_point=spawn_point,
            sprite_path=sprite_path,
            scale=scale
        )

        Movable.__init__(
            self,
            speed=speed
        )

        self._lives: int = lives
        self._score: int = 0

    def update(self, delta: float) -> None:
        pass

    def move(self, direction: tuple[float, float]) -> None:
        pass

