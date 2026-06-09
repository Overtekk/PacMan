# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  Cat_brain.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/09 11:39:21 by roandrie        #+#    #+#               #
#  Updated: 2026/06/09 11:39:35 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from .brain import EnemyBrain
from ..logics.StateMachine import EnemyState
from src import game_config
from src.utils import print_log

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.entity.enemies.cat_enemy import CatEnemy


class CatBrain(EnemyBrain):
    def __init__(self, enemy: 'CatEnemy') -> None:
        super().__init__(enemy)

    def update(self, delta_time: float) -> None:
        pass

        super().update(delta_time)

    # :---------------:
    #  PRIVATE METHODS
    # :---------------:
