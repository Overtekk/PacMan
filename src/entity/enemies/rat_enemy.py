# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  rat_enemy.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:04:53 by roandrie        #+#    #+#               #
#  Updated: 2026/05/29 11:32:28 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from ..entity import Enemy
from ..player import Player
from src.utils import SuperCalculator


class RatEnemy(Enemy):
    def __init__(
        self, spawn_point: tuple[int, int],
        sprite_sheet_move: list[arcade.Texture],
        sprite_sheet_eatable: list[arcade.Texture],
        sprite_sheet_died: list[arcade.Texture],
        maze_bitmap: dict[tuple[int, int], str],
        calculator: SuperCalculator,
        player_ref: Player,
        scale: float = 1.0,
        speed: float = 100.0,
        is_edible: bool = False
    ) -> None:

        super().__init__(
            spawn_point=spawn_point,
            sprite_sheet_move=sprite_sheet_move,
            sprite_sheet_eatable=sprite_sheet_eatable,
            sprite_sheet_died=sprite_sheet_died,
            maze_bitmap=maze_bitmap,
            calculator=calculator,
            player_reference=player_ref,
            scale=scale,
            speed=speed,
            is_edible=is_edible
        )

        # Spawn right, facing right
        self.sprite.texture = self.textures[1]

    def die(self) -> None:
        pass
