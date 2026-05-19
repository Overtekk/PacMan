# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  level_manager.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 20:04:01 by roandrie        #+#    #+#               #
#  Updated: 2026/05/19 17:03:30 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any

import arcade

from pathlib import Path

from src.config import GameConfig
from src.entity import Player, CatEnemy, FoxEnemy, RatEnemy, DogEnemy
from src.renderer.screen_settings import ScreenSettings
from src.renderer.sprites_loader import load_sprite_sheet
from src.maze import MazeFactory, generate_bytes_maze


class LevelManager():
    def __init__(self, game_window: arcade.Window) -> None:

        self.config: GameConfig = game_window.game_config
        self.asset_manager: dict[str, Path] = game_window.asset_manager

        self.enemies_list: list[str, Any] = {}

    def create_level(
        self, level_name: str, maze_width: int, maze_height: int
    ) -> list[list[int]]:

        # Store the maze width & height in the class
        self.maze_width = maze_width
        self.maze_height = maze_height

        # Create the level
        generated_level: list[list[int]] = self._create_maze_level()

        # Create all entities
        self._create_entity()

        return generated_level

    # :---------------:
    #  PRIVATE METHODS
    # :---------------:

    def _create_maze_level(self) -> list[list[int]]:
        # Instanciate the MazeFactory object
        self.factory = MazeFactory()

        # Create the Maze
        wall_data: list[list[int]] = self.factory.generate_maze(
            self.maze_width, self.maze_height,
            self.asset_manager.textures,
            ScreenSettings.WIDTH,ScreenSettings.HEIGHT
        )
        # Store the maze in bytes for later calculations
        self.byte_maze: dict = generate_bytes_maze(
            self.factory.grid_data,
            self.maze_width, self.maze_height,
        )

        return wall_data

    def _create_entity(self) -> None:
        # Get the spawn positions of all entities
        spawn_positions: dict[str, tuple[int, int]] = (
            self._get_spawn_positions()
        )

        # Create the player
        self.player: Player = Player(
            spawn_point=spawn_positions["player"],
            sprite_sheet=load_sprite_sheet(
                textures=self.asset_manager.textures["player"],
                sprite_width=308/6, sprite_height=63,
                sprites_columns=6, sprites_count=6
            ),
            scale=0.6
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

    def _get_spawn_positions(self) -> dict[str, tuple[int, int]]:
        spawn_dict: dict[str, tuple[int, int]] = {}

        # Get the maze center
        col_center: int = self.maze_width // 2
        row_center: int = self.maze_height // 2

        if self.byte_maze[row_center * 2 + 1, col_center * 2 + 1] == 0:
            player_x, player_y = self.factory.get_pixel_coordinates(
                col_center, row_center
            )

        for y in range(row_center):
            for x in range(col_center):
                coords = (y, x)

                if self.byte_maze[coords] == 0:
                    print(0)
                else:
                    print(1)

        spawn_dict["player"] = (player_x, player_y)

        return spawn_dict

    # create the level
    # create the player, ennemis and collectibles
    # handle respawn, level restart, level start
