# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  StateMachine.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/18 14:58:28 by roandrie        #+#    #+#               #
#  Updated: 2026/05/25 16:53:35 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from enum import Enum, auto


class EnemyState(Enum):
    WAIT = auto()
    WANDER = auto()
    CHASE = auto()
    RUNAWAY = auto()
    RESPAWN = auto()
    SEARCH = auto()
