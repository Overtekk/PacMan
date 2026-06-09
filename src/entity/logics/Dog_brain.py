# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Dog_brain.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: roandrie <roandrie@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/06/09 11:38:05 by roandrie          #+#    #+#              #
#    Updated: 2026/06/09 11:39:04 by roandrie         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from .brain import EnemyBrain
from ..logics.StateMachine import EnemyState
from src import game_config
from src.utils import print_log

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.entity.enemies.dog_enemy import DogEnemy


class DogBrain(EnemyBrain):
    def __init__(self, enemy: 'DogEnemy') -> None:
        super().__init__(enemy)

    def update(self, delta_time: float) -> None:
        pass

        super().update(delta_time)

    # :---------------:
    #  PRIVATE METHODS
    # :---------------:

