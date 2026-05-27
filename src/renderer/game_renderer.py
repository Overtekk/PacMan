# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  game_renderer.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:18:31 by roandrie        #+#    #+#               #
#  Updated: 2026/05/26 18:55:41 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any

import arcade

from src.renderer.screen_settings import ScreenSettings, CollectiblesType
from src.renderer.ui.ui_screen import UIScreen


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
        self.walls: arcade.SpriteList[Any] = arcade.SpriteList()
        self.entities: arcade.SpriteList[Any] = arcade.SpriteList()
        self.pacgums: arcade.SpriteList[Any] = arcade.SpriteList()
        self.super_pacgums: arcade.SpriteList[Any] = arcade.SpriteList()

        # Text
        self.timer_text: str = ""
        self.timer_size: float = 0.0

        self.timer_text_obj: arcade.Text = arcade.Text(
            text=self.timer_text,
            x=ScreenSettings.WIDTH / 2, y=ScreenSettings.HEIGHT / 2,
            color=arcade.color.WHITE_SMOKE, font_size=int(self.timer_size),
            anchor_x="center", anchor_y="center", font_name="fibberish"
        )

        self.background = arcade.load_texture("assets/sprites/main_menu/ocean.png")


        # UI
        self.ui_screen = UIScreen(0, 0, 0)

    def draw(self) -> None:
        dark_tint = arcade.types.Color(140, 140, 140)
        arcade.draw_texture_rect(
            texture=self.background,
            rect=arcade.LBWH(0, 0, ScreenSettings.WIDTH, ScreenSettings.HEIGHT),
            color=dark_tint
        )
        self.pacgums.draw()
        self.super_pacgums.draw()
        self.walls.draw()
        self.entities.draw()

        if self.timer_size > 0 and self.timer_text:
            self.timer_text_obj.draw()
        # self.ui_screen.build_ui()
        self.ui_screen.on_draw()

    def update(self, delta_time: float) -> None:
        REDUCE_SIZE_PIXELS: float = 150.0

        if self.timer_size > 0:
            if self.instant_text:
                self.timer_size -= (REDUCE_SIZE_PIXELS * delta_time) * 4
                self.timer_text_obj.font_size = self.timer_size
            else:
                self.timer_size -= REDUCE_SIZE_PIXELS * delta_time
                self.timer_text_obj.font_size = self.timer_size

            if self.timer_size < 0:
                self.timer_size = 0
        self.timer_text_obj.text = self.timer_text

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

    def setup_collectibles(
        self, collectible_sprite: arcade.Sprite, collectible_type
    ) -> None:
        if collectible_type == CollectiblesType.PACGUM:
            self.pacgums.append(collectible_sprite)

        elif collectible_type == CollectiblesType.SUPER_PACGUM:
            self.super_pacgums.append(collectible_sprite)

    def trigger_time_text(self, text: str, instant_text: bool = False) -> None:
        TEXT_SIZE: float = 250.0

        self.timer_text = text
        self.timer_size = TEXT_SIZE
        self.instant_text = instant_text

    def update_ui(self, score, time, live):
        self.ui_screen.update(score, time, live)
