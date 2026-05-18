# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  test_enemy.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/18 12:57:45 by roandrie        #+#    #+#               #
#  Updated: 2026/05/18 13:07:22 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from test_player import TestPlayer
from src.entity import CatEnemy


if __name__ == "__main__":
    player_test: TestPlayer = TestPlayer()

    sheet = player_test.sprites_list.textures["enemy_cat"]

    enemy1: CatEnemy = CatEnemy(
        spawn_point=(0, 0),
        sprite_sheet=sheet,
        scale=1
    )


    arcade.run()
