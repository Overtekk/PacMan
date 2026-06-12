# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  super_pacgum.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:09:02 by roandrie        #+#    #+#               #
#  Updated: 2026/06/12 11:46:12 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from ..entity import Collectible
from src.utils import SuperCalculator


class SuperPacgum(Collectible):
    def __init__(
        self, spawn_point: tuple[int, int],
        sprite: str | arcade.Texture,
        calculator: SuperCalculator,
        scale: float = 1.0,
        score: int = 0
    ) -> None:
        """Initialize a Super Pacgum item capable of triggering state changes.

        Args:
            spawn_point (tuple[int, int]): Grid coordinates for spawning.
            sprite (str | arcade.Texture): Path to texture or Texture object.
            calculator (SuperCalculator): Utility instance for coordinates
            calculations.
            scale (float, optional): Visual scale factor. Defaults to 1.0.
            score (int, optional): Score rewarded upon collection. Defaults to
            0.
        """

        super().__init__(
            spawn_point=spawn_point,
            sprite_data=sprite,
            calculator=calculator,
            scale=scale,
            score=score
        )

        self._is_activate: bool = False

    @property
    def is_activate(self) -> bool:
        """Check if the super pacgum effects are currently activated.

        Returns:
            bool: True if activated, False otherwise.
        """
        return self._is_activate
