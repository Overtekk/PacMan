# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  super_pacgum.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:09:02 by roandrie        #+#    #+#               #
#  Updated: 2026/05/18 09:45:03 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from ..entity import Entity, Collectible


class SuperPacgum(Entity, Collectible):
    def __init__(
        self, spawn_point: tuple[int, int],
        sprite_path: str,
        scale: float = 1.0,
        score: int = 0
    ) -> None:

        Entity.__init__(
            self, spawn_point=spawn_point,
            sprite_path_or_texture=sprite_path,
            scale=scale
        )

        Collectible.__init__(
            self, score=score
        )

    def activate_power(self) -> None:
        pass
