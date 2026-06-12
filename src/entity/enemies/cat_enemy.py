# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  cat_enemy.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:04:41 by roandrie        #+#    #+#               #
#  Updated: 2026/06/12 11:46:33 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from ..entity import Enemy
from ..player import Player
from ..logics.Cat_brain import CatBrain
from src.utils import SuperCalculator


class CatEnemy(Enemy):
    def __init__(
        self, spawn_point: tuple[int, int],
        sprite_sheet_move: list[arcade.Texture],
        sprite_sheet_eatable: list[arcade.Texture],
        sprite_sheet_died: list[arcade.Texture],
        maze_bitmap: dict[tuple[int, int], int],
        calculator: SuperCalculator,
        player_ref: Player,
        scale: float,
        speed: float,
        is_edible: bool = False
    ) -> None:
        """Initialize the Cat enemy entity with its specific AI behavior.

        Args:
            spawn_point (tuple[int, int]): Grid coordinates for spawning.
            sprite_sheet_move (list[arcade.Texture]): Textures used during
            regular movement.
            sprite_sheet_eatable (list[arcade.Texture]): Textures used when
            vulnerable.
            sprite_sheet_died (list[arcade.Texture]): Textures used when
            defeated.
            maze_bitmap (dict[tuple[int, int], int]): Matrix representation of
            the maze walls.
            calculator (SuperCalculator): Utility instance for coordinates
            calculations.
            player_ref (Player): Reference to the player instance for
            targeting.
            scale (float): Visual scale factor.
            speed (float): Movement speed of the entity.
            is_edible (bool, optional): Initial vulnerability state. Defaults
            to False.
        """

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
            is_edible=is_edible,
        )

        self.brain = CatBrain(self)
