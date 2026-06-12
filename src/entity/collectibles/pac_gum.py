# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  pac_gum.py                                        :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:06:12 by roandrie        #+#    #+#               #
#  Updated: 2026/06/12 11:45:54 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from ..entity import Collectible
from src.utils import SuperCalculator


class Pacgum(Collectible):
    def __init__(
        self, spawn_point: tuple[int, int],
        sprite_path: str | arcade.Texture,
        calculator: SuperCalculator,
        scale: float = 1.0,
        score: int = 0
    ) -> None:
        """Initialize a standard Pacgum item.

        Args:
            spawn_point (tuple[int, int]): Grid coordinates for spawning.
            sprite_path (str | arcade.Texture): Path to texture or Texture
            object.
            calculator (SuperCalculator): Utility instance for coordinates
            calculations.
            scale (float, optional): Visual scale factor. Defaults to 1.0.
            score (int, optional): Score rewarded upon collection. Defaults to
            0.
        """

        super().__init__(
            spawn_point=spawn_point,
            sprite_data=sprite_path,
            calculator=calculator,
            scale=scale,
            score=score
        )
