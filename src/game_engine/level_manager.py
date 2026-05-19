# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  level_manager.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 20:04:01 by roandrie        #+#    #+#               #
#  Updated: 2026/05/18 16:11:31 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.entity import Player


class LevelManager():
    def __init__(self) -> None:
        pass

    def _create_entity(self) -> None:
        self.player = Player(
            spawn_point=(0, 0),
            sprite_sheet="",
            scale=1
        )

    # create the level
    # create the player, ennemis and collectibles
    # handle respawn, level restart, level start
