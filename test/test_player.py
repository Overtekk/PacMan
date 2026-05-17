# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  test_player.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/17 15:16:38 by roandrie        #+#    #+#               #
#  Updated: 2026/05/17 16:26:15 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from src.renderer import ScreenSettings, SpritesLoader
from src.entity import Player
import pathlib


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

        # Calcul du chemin absolu (depuis la racine du système)
        raw_path = pathlib.Path(self.sprites_list.textures["player"])
        absolute_path = raw_path.resolve()

        self.player: Player = Player(
            (ScreenSettings.WIDTH // 2, ScreenSettings.HEIGHT // 2),
            str(absolute_path),
            1, 0, 3
        )

        self.player_list: arcade.SpriteList = arcade.SpriteList()
        self.player_list.append(self.player.sprite)

    def on_draw(self) -> None:
        self.clear()
        self.player_list.draw()

    def on_update(self, delta_time) -> None:
        self.player.update(delta_time)


if __name__ == "__main__":
    t: TestPlayer = TestPlayer()

    arcade.run()
