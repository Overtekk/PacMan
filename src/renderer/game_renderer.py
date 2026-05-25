# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_renderer.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:18:31 by roandrie        #+#    #+#               #
#  Updated: 2026/05/25 14:10:06 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any

import arcade

from src.renderer.screen_settings import ScreenSettings


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
        # Objects
        self.walls: arcade.SpriteList = arcade.SpriteList()
        self.entities: arcade.SpriteList[Any] = arcade.SpriteList()

        # Text
        self.timer_text: str = ""
        self.timer_size: float = 0.0

    def draw(self) -> None:
        self.walls.draw()
        self.entities.draw()

        if self.timer_size > 0 and self.timer_text:
            timer_text: arcade.Text = arcade.Text(
                text=self.timer_text,
                x=ScreenSettings.WIDTH / 2, y=ScreenSettings.HEIGHT / 2,
                color=arcade.color.WHITE_SMOKE, font_size=int(self.timer_size),
                anchor_x="center", anchor_y="center", font_name="fibberish"
            )
            timer_text.draw()

    def update(self, delta_time: float) -> None:
        REDUCE_SIZE_PIXELS: float = 150.0

        if self.timer_size > 0:
            if self.instant_text:
                self.timer_size -= (REDUCE_SIZE_PIXELS * delta_time) * 4
            else:
                self.timer_size -= REDUCE_SIZE_PIXELS * delta_time

            if self.timer_size < 0:
                self.timer_size = 0

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

    def trigger_time_text(self, text: str, instant_text: bool = False) -> None:
        TEXT_SIZE: float = 250.0

        self.timer_text = text
        self.timer_size = TEXT_SIZE
        self.instant_text = instant_text


#=self.window.asset_manager.textures["start_button"],
