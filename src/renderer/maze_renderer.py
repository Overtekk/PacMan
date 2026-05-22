# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  maze_renderer.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:18:31 by roandrie        #+#    #+#               #
#  Updated: 2026/05/22 11:27:47 by anacharp        ###   ########.fr        #
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

        self.walls: arcade.SpriteList = arcade.SpriteList()
        self.entities: arcade.SpriteList[Any] = arcade.SpriteList()

    def draw(self) -> None:
        self.walls.draw()
        self.entities.draw()

    def wall_generator(
        self,
        wall_data: list[tuple[str, float, float, float]]
    ) -> None:
        self.walls.clear()
        self.entities.clear()
        for sprite_path, angle, x, y, tile_size in wall_data:
            wall = Wall(sprite_path, angle, x, y, tile_size)

            self.walls.append(wall)

    def setup_entities(self, entity_sprite: arcade.Sprite) -> None:
        self.entities.append(entity_sprite)


#=self.window.asset_manager.textures["start_button"],
