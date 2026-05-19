# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  level_manager.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 20:04:01 by roandrie        #+#    #+#               #
#  Updated: 2026/05/19 10:26:06 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.entity import Player
from src.renderer.sprites_loader import load_sprite_sheet


class LevelManager():
    def __init__(self) -> None:
        pass

    def create_level(
        self, level_name: str, maze_width: int, maze_height: int
    ) -> None:
        pass

    def _create_entity(self) -> None:
        # Create the player
        self.player = Player(
            spawn_point=(0, 0),
            sprite_sheet=load_sprite_sheet(
                ),
            scale=1
        )

    # create the level
    # create the player, ennemis and collectibles
    # handle respawn, level restart, level start
