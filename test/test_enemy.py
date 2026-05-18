# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  test_enemy.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/18 12:57:45 by roandrie        #+#    #+#               #
#  Updated: 2026/05/18 15:37:03 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from test_player import TestPlayer
from src.entity import CatEnemy


if __name__ == "__main__":
    player_test: TestPlayer = TestPlayer()

    sheet =  arcade.SpriteSheet(player_test.sprites_list.textures["dog_enemy"])

    frame_width = 32
    frame_height = 32

    textures_list: list[arcade.Texture] = sheet.get_texture_grid(
        size=(frame_width, frame_height),
        columns=1,
        count=1
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
