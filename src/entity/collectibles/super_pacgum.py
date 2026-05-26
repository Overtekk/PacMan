# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  super_pacgum.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:09:02 by roandrie        #+#    #+#               #
#  Updated: 2026/05/26 16:57:05 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any

from pathlib import Path

from ..entity import Collectible
from ..player import Player
from ..logics.StateMachine import EnemyState
from src.utils import SuperCalculator


class SuperPacgum(Collectible):
    def __init__(
        self, spawn_point: tuple[int, int],
        sprite: str | Path,
        calculator: SuperCalculator,
        scale: float = 1.0,
        score: int = 0
    ) -> None:

        super().__init__(
            spawn_point=spawn_point,
            sprite_data=sprite,
            calculator=calculator,
            scale=scale,
            score=score

        )

    def activate_power(
        self, player_reference: Player, enemies_reference: list[str, Any]
    ) -> None:

        player_reference.invincible = True

        for enemy in enemies_reference.values():
            enemy.mode = EnemyState.RUNAWAY
