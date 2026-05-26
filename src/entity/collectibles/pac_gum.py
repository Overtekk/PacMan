# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  pac_gum.py                                        :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:06:12 by roandrie        #+#    #+#               #
#  Updated: 2026/05/26 16:28:26 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from pathlib import Path

from ..entity import Collectible
from src.utils import SuperCalculator


class Pacgum(Collectible):
    def __init__(
        self, spawn_point: tuple[int, int],
        sprite_path: str | Path,
        calculator: SuperCalculator,
        scale: float = 1.0,
        score: int = 0
    ) -> None:

        super().__init__(
            spawn_point=spawn_point,
            sprite_data=sprite_path,
            calculator=calculator,
            scale=scale,
            score=score

        )

    def activate_power(self) -> None:
        pass
