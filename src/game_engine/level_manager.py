# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  level_manager.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 20:04:01 by roandrie        #+#    #+#               #
#  Updated: 2026/05/19 13:53:56 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any

import arcade

from pathlib import Path

from src.config import GameConfig
from src.entity import Player, CatEnemy, FoxEnemy, RatEnemy, DogEnemy
from src.renderer.screen_settings import ScreenSettings
from src.renderer.sprites_loader import load_sprite_sheet
from src.maze import MazeFactory


class LevelManager():
    def __init__(self, game_window: arcade.Window) -> None:

        self.config: GameConfig = game_window.game_config
        self.asset_manager: dict[str, Path] = game_window.sprites_list

        self.enemies_list: list[str, Any] = {}

    def create_level(
        self, level_name: str, maze_width: int, maze_height: int
    ) -> list[list[int]]:

        # Empty the previous variables
        self.wall_data = None
        self.player = None
        if self.enemies_list:
            for enemy in self.enemies_list:
                self.enemies_list[enemy] = None

        level: list[list[int]] = self._create_maze_level(
            width=maze_width, height=maze_height
        )
        self._create_entity()

        return level

    def _create_maze_level(self, width: int, height: int) -> list[list[int]]:
        # Instanciate the MazeFactory object
        factory = MazeFactory()

        # Create the Maze
        wall_data: list[list[int]] = factory.generate_maze(
            width, height,
            self.asset_manager.textures,
            ScreenSettings.WIDTH,ScreenSettings.HEIGHT
        )

        return wall_data

    def _create_entity(self) -> None:
        # Create the player
        self.player: Player = Player(
            spawn_point=(0, 0),
            sprite_sheet=load_sprite_sheet(
                textures=self.asset_manager.textures["player"],
                sprite_width=308/6, sprite_height=63,
                sprites_columns=6, sprites_count=6
            ),
            scale=1
        )

        # Create enemies
        self.cat_enemy: CatEnemy = CatEnemy(
            spawn_point=(0, 0),
            sprite_sheet=load_sprite_sheet(
                textures=self.asset_manager.textures["cat_enemy"],
                sprite_width=96/3, sprite_height=32,
                sprites_columns=3, sprites_count=3
            ),
            scale=1.2,
            speed=101
        )
        self.enemies_list["cat_enemy"] = self.cat_enemy

        self.dog_enemy: DogEnemy = DogEnemy(
            spawn_point=(0, 0),
            sprite_sheet=load_sprite_sheet(
                textures=self.asset_manager.textures["dog_enemy"],
                sprite_width=96/3, sprite_height=30,
                sprites_columns=3, sprites_count=3
            ),
            scale=1.2,
            speed=101
        )
        self.enemies_list["dog_enemy"] = self.dog_enemy

        self.fox_enemy: FoxEnemy = FoxEnemy(
            spawn_point=(0, 0),
            sprite_sheet=load_sprite_sheet(
                textures=self.asset_manager.textures["fox_enemy"],
                sprite_width=96/3, sprite_height=32,
                sprites_columns=3, sprites_count=3
            ),
            scale=1.2,
            speed=101
        )
        self.enemies_list["fox_enemy"] = self.fox_enemy

        self.rat_enemy: RatEnemy = RatEnemy(
            spawn_point=(0, 0),
            sprite_sheet=load_sprite_sheet(
                textures=self.asset_manager.textures["rat_enemy"],
                sprite_width=96/3, sprite_height=32,
                sprites_columns=3, sprites_count=3
            ),
            scale=1.2,
            speed=101
        )
        self.enemies_list["rat_enemy"] = self.rat_enemy

    # create the level
    # create the player, ennemis and collectibles
    # handle respawn, level restart, level start
