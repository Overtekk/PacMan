# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  collision_manager.py                              :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 20:04:13 by roandrie        #+#    #+#               #
#  Updated: 2026/05/21 14:45:34 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any

import arcade

from src.entity import Entity, Player


class CollisionManager():
    def __init__(
        self,
        player_reference: Player,
        enemies_reference: list[str, Any],
        walls_sprites_list: arcade.SpriteList[arcade.Sprite]
    ) -> None:

        self.player_reference = player_reference
        self.enemies_reference = enemies_reference
        self.walls_sprites_list = walls_sprites_list

    def update(self) -> None:
        # Check the collisions for the player
        if self.player_reference._current_direction != (0, 0):
            if not self.check_for_collisions(self.player_reference):
                self.player_reference._current_direction = (0, 0)

    def check_for_collisions(self, entity: Entity) -> bool:
        colliding_sprite: list[arcade.SpriteType] = (
            arcade.check_for_collision_with_list(
                sprite=entity.sprite,
                sprite_list=self.walls_sprites_list
            ))
        return len(colliding_sprite) == 0

    # use check_for_collisions_with_list to handle all collisions
    # avoid player and ennemis to travel throught walls
    # detect player and collectibles
    # detect player and enemy
