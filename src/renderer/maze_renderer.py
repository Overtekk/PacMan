# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  maze_renderer.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:18:31 by roandrie        #+#    #+#               #
#  Updated: 2026/05/21 14:36:27 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any

import arcade


class Wall(arcade.Sprite):
    def __init__(
        self,
        sprite_path: str,
        angle: float = 0,
        center_x: float = 0,
        center_y: float = 0,
        tile_size: int = 0
    ) -> None:

        super().__init__(
            sprite_path,
            center_x=center_x,
            center_y=center_y
        )

        self.angle = angle
        self.scale = tile_size / self.texture.width


class GameRenderer():
    def __init__(self) -> None:

        self.walls_sprites: arcade.SpriteList = arcade.SpriteList()
        self.entities_sprites: arcade.SpriteList[Any] = arcade.SpriteList()

    def draw(self) -> None:
        self.walls_sprites.draw()
        self.entities_sprites.draw()

    def wall_generator(
        self,
        wall_data: list[tuple[str, float, float, float]]
    ) -> None:

        for sprite_path, angle, x, y, tile_size in wall_data:
            wall: arcade.Sprite = Wall(sprite_path, angle, x, y, tile_size)

            self.walls_sprites.append(wall)

    def setup_entities(self, entity_sprite: arcade.Sprite) -> None:
        self.entities_sprites.append(entity_sprite)


#=self.window.asset_manager.textures["start_button"],
