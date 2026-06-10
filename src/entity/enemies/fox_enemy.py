# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  fox_enemy.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 18:54:32 by roandrie        #+#    #+#               #
#  Updated: 2026/06/10 11:48:29 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from ..entity import Enemy
from ..player import Player
from ..logics.Fox_brain import FoxBrain
from ..logics.StateMachine import EnemyState
from src.utils import SuperCalculator


class FoxEnemy(Enemy):
    def __init__(
        self, spawn_point: tuple[int, int],
        sprite_sheet_move: list[arcade.Texture],
        sprite_sheet_eatable: list[arcade.Texture],
        sprite_sheet_died: list[arcade.Texture],
        sprite_sheet_angry: list[arcade.Texture],
        maze_bitmap: dict[tuple[int, int], int],
        calculator: SuperCalculator,
        player_ref: Player,
        scale: float,
        speed: float,
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
            is_edible=is_edible,
        )

        self.sprite_sheet_angry = sprite_sheet_angry
        self.enemy_type = "fox"

        self.sprite.texture = self.textures[1]
        self.brain = FoxBrain(self)

    def _update_sprite(self) -> None:
        if self.mode == EnemyState.RESPAWN:
            self.sprite.texture = self.sprite_sheet_died[
                self.current_texture_index
            ]
        elif self.mode == EnemyState.RUNAWAY:
            self.sprite.texture = self.sprite_sheet_eatable[
                self.current_texture_index
            ]
        elif self.mode == EnemyState.ANGRY:
            self.sprite.texture = self.sprite_sheet_angry[
                self.current_texture_index
            ]
        elif not self._wait_revive:
            self.sprite.texture = self.textures[self.current_texture_index]
