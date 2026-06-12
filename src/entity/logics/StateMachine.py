# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  StateMachine.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/18 14:58:28 by roandrie        #+#    #+#               #
#  Updated: 2026/06/12 11:55:42 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from enum import Enum, auto


class EnemyState(Enum):
    """
    Enumeration identifying all operational behavior states for an enemy AI.
    """
    WAIT = auto()
    WANDER = auto()
    CHASE = auto()
    RUNAWAY = auto()
    RESPAWN = auto()
    SEARCH = auto()
    ANGRY = auto()
