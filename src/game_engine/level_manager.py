# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  level_manager.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 20:04:01 by roandrie        #+#    #+#               #
#  Updated: 2026/05/20 14:04:02 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any

import arcade

from pathlib import Path

from src.utils import print_warn
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
            scale=1
        )

        # Create enemies
        self.cat_enemy: CatEnemy = CatEnemy(
            spawn_point=spawn_positions["cat_enemy"],
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
            spawn_point=spawn_positions["dog_enemy"],
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
            spawn_point=spawn_positions["fox_enemy"],
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
            spawn_point=spawn_positions["rat_enemy"],
            sprite_sheet=load_sprite_sheet(
                textures=self.asset_manager.textures["rat_enemy"],
                sprite_width=96/3, sprite_height=32,
                sprites_columns=3, sprites_count=3
            ),
            scale=1.2,
            speed=101
        )
        self.enemies_list["rat_enemy"] = self.rat_enemy

    def _create_collectibles(self) -> None:
        # SuperPacgums
        pass

    def _get_spawn_positions(self) -> dict[str, tuple[int, int]]:
        spawn_dict: dict[str, tuple[int, int]] = {}

        # Placing the player
        raw_x, raw_y = self._get_raw_coords(
            "player", (self.maze_width // 2, self.maze_height // 2)
        )

        # Get the coordinates in pixel
        x, y = self.factory.get_pixel_coordinates(
            raw_x, raw_y
        )

        spawn_dict["player"] = (x, y)

        # Placing enemies
        #   FOX
        raw_x, raw_y = self._get_raw_coords(
            "fox_enemy", (self.maze_width - 1, self.maze_height - 1)
        )
        x, y = self.factory.get_pixel_coordinates(
            raw_x, raw_y
        )
        spawn_dict["fox_enemy"] = (x, y)

        #   CAT
        raw_x, raw_y = self._get_raw_coords(
            "cat_enemy", (0, 0)
        )
        x, y = self.factory.get_pixel_coordinates(
            raw_x, raw_y
        )
        spawn_dict["cat_enemy"] = (x, y)

        #   RAT
        raw_x, raw_y = self._get_raw_coords(
            "rat_enemy", (self.maze_width - 1, 0)
        )
        x, y = self.factory.get_pixel_coordinates(
            raw_x, raw_y
        )
        spawn_dict["rat_enemy"] = (x, y)

        #   DOG
        raw_x, raw_y = self._get_raw_coords(
            "dog_enemy", (0, self.maze_height - 1)
        )
        x, y = self.factory.get_pixel_coordinates(
            raw_x, raw_y
        )
        spawn_dict["dog_enemy"] = (x, y)

        return spawn_dict

    def _get_raw_coords(
        self, entity_name: str, coords: tuple[int, int]
    ) -> tuple[int, int]:

        x = coords[0]
        y = coords[1]

        extend_x = x * 2 + 1
        extend_y = y * 2 + 1

        # Is this position have cell open?
        if self.byte_maze[extend_x, extend_y] == 0:
            return ((extend_x - 1) // 2, (extend_y - 1) // 2)

        # Else, finding another valable position
        new_coords: tuple[int, int] = self._find_valid_position(
            entity_name, (extend_x, extend_y)
        )

        print_warn(
            f"Can't place the {entity_name} at {coords}. "
            f"📌 Placing at {new_coords}.\n"
        )

        new_x = (new_coords[0] - 1) // 2
        new_y = (new_coords[1] - 1) // 2

        return (new_x, new_y)

    def _find_valid_position(
        self, entity_name: str, start_coords: tuple[int, int]
    ) -> tuple[int, int]:
        row: int = start_coords[0]
        col: int = start_coords[1]
        case: int = 1

        # Find valid start position
        while True:

            if case >= 6:
                raise ValueError(
                    f"Can't place {entity_name}.\n"
                    "Maybe the maze is invalid? 👁️👁️"
                )

            # Check case: north
            if self.byte_maze.get((row, col + case), 1) == 0:
                valid_coords = (row, col + case)
                break

            # Check case: south
            elif self.byte_maze.get((row, col - case), 1) == 0:
                valid_coords = (row, col - case)
                break

            # Check case: west
            elif self.byte_maze.get((row - case, col), 1) == 0:
                valid_coords = (row - case, col)
                break

            # Check case: west-north
            elif self.byte_maze.get((row - case, col + case), 1) == 0:
                valid_coords = (row - case, col + case)
                break

            # Check case: west-south
            elif self.byte_maze.get((row - case, col - case), 1) == 0:
                valid_coords = (row - case, col - case)
                break

            # Check case: east
            if self.byte_maze.get((row + case, col), 1) == 0:
                valid_coords = (row + case, col)
                break

            # Check case: north-east
            elif self.byte_maze.get((row + case, col - case), 1) == 0:
                valid_coords = (row + case, col - case)
                break

            # Check case: south-east
            elif self.byte_maze.get((row + case, col + case), 1) == 0:
                valid_coords = (row + case, col + case)
                break

            case += 1

        return valid_coords

    # create the level
    # create the player, ennemis and collectibles
    # handle respawn, level restart, level start
