# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  test_enemy.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/18 12:57:45 by roandrie        #+#    #+#               #
#  Updated: 2026/05/18 16:21:10 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from test_player import TestPlayer
from src.entity import CatEnemy
from src.renderer import load_sprite_sheet


if __name__ == "__main__":
    player_test: TestPlayer = TestPlayer()

    textures_list = load_sprite_sheet(
        textures=player_test.sprites_list.textures["dog_enemy"],
        sprite_width=32, sprite_height=32, sprites_columns=1, sprites_count=1
    )

    enemy1: CatEnemy = CatEnemy(
        spawn_point=(500, 500),
        sprite_sheet=textures_list,
        scale=1.2
    )

    enemy1._can_move = True

    player_test.enemy_list.append(enemy1.sprite)
    player_test.enemies_data.append(enemy1)


    arcade.run()
