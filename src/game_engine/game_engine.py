# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_engine.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:20:06 by roandrie        #+#    #+#               #
#  Updated: 2026/05/14 21:20:20 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade


class GameEngine(arcade.View):
    def __init__(self) -> None:
        super().__init()

    # main loop of the game, orchestor
    # move all entity
    # verify gamestate, levelmanager

    def update(delta: float) -> None:
        pass

    def setup() -> None:
        pass
