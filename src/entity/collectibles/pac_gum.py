# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  pac_gum.py                                        :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:06:12 by roandrie        #+#    #+#               #
#  Updated: 2026/05/18 11:10:00 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from ..entity import Collectible


class Pacgum(Collectible):
    def __init__(
        self, spawn_point: tuple[int, int],
        sprite_sheet: str,
        scale: float = 1.0,
        score: int = 0
    ) -> None:

        super().__init__(
            spawn_point=spawn_point,
            sprite_data=sprite_sheet,
            scale=scale,
            score=score

        )

    def activate_power(self) -> None:
        pass
