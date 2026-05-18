# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  player.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 18:40:42 by roandrie        #+#    #+#               #
#  Updated: 2026/05/18 10:36:47 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from .entity import Entity, Movable
import arcade


class Player(Entity, Movable):
    def __init__(
        self, spawn_point: tuple[int, int],
        sprite_path: list[arcade.Texture],
        scale: float = 1.0,
        speed: float = 100.0,
    ) -> None:

        self.textures: list[arcade.Texture] = sprite_path
        self.current_texture_index: int = 0

        Entity.__init__(
            self,
            spawn_point=spawn_point,
            sprite_path_or_texture=self.textures[0],
            scale=scale
        )

        Movable.__init__(
            self,
            speed=speed
        )

    def update(self, delta: float) -> None:
        dx = self._current_direction[0] * self.speed * delta
        dy = self._current_direction[1] * self.speed * delta
        self.x += dx
        self.y += dy

    def die(self) -> None:
        self._can_move = False
        self.respawn()

