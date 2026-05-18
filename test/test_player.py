# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  test_player.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/17 15:16:38 by roandrie        #+#    #+#               #
#  Updated: 2026/05/18 16:23:52 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any

import arcade

from src.renderer import ScreenSettings, SpritesLoader
from src.entity import Player
from src.renderer import load_sprite_sheet


class TestPlayer(arcade.Window):
    def __init__(self) -> None:

        super().__init__(
            width=ScreenSettings.WIDTH,
            height=ScreenSettings.HEIGHT,
            title="Pac-Man",
            vsync=True,
            center_window=True
        )

        self.sprites_list: SpritesLoader = SpritesLoader()

        textures_list = load_sprite_sheet(
            self.sprites_list.textures["player"], 308 / 6, 63, 6, 6
        )

        self.player: Player = Player(
            (ScreenSettings.WIDTH // 2, ScreenSettings.HEIGHT // 2),
            textures_list,
            1
        )

        self.player_list: arcade.SpriteList = arcade.SpriteList()
        self.player_list.append(self.player.sprite)
        self.player._can_move = True

        self.enemy_list: arcade.SpriteList = arcade.SpriteList()

        self.enemies_data: list[Any] = []

    def on_draw(self) -> None:
        self.clear()
        self.player_list.draw()
        self.enemy_list.draw()

    def on_update(self, delta_time) -> None:
        self.player.update(delta_time)

        for enemy in self.enemies_data:
            enemy.update(delta_time)

    def on_key_press(self, symbol: int, _modifiers: int) -> None:
        if symbol == arcade.key.UP or symbol == arcade.key.W:
            self.player.move((0, 1))

        elif symbol == arcade.key.DOWN or symbol == arcade.key.S:
            self.player.move((0, -1))

        elif symbol == arcade.key.LEFT or symbol == arcade.key.A:
            self.player.move((-1, 0))

        elif symbol == arcade.key.RIGHT or symbol == arcade.key.D:
            self.player.move((1, 0))


if __name__ == "__main__":
    t: TestPlayer = TestPlayer()

    arcade.run()
