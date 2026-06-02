# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  level_manager.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 20:04:01 by roandrie        #+#    #+#               #
#  Updated: 2026/06/02 11:07:40 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any

import arcade

from pathlib import Path
from random import random

from src import game_config
from src.utils import print_warn, load_sprite_sheet, SuperCalculator
from src.config import GameConfig
from src.renderer.screen_settings import ScreenSettings
from src.maze import MazeFactory, generate_bytes_maze
from src.entity import (Player, CatEnemy, FoxEnemy, RatEnemy, DogEnemy,
                        Pacgum, SuperPacgum)


PLAYER_SCALE: float = 0.7
ENEMIES_SCALE: float = 0.7
PACGUM_SCALE: float = 0.7
SUPERPACGUM_SCALE: float = 0.8


class LevelManager():
    def __init__(self, game_window: arcade.Window) -> None:

        self.config: GameConfig = game_window.game_config
        self.asset_manager: dict[str, Path] = game_window.asset_manager

        self.enemies_list: list[str, Any] = {}
        self.pacgums_list: list[Pacgum] = []
        self.super_pacgums_list: list[SuperPacgum] = []

        self.PLAYER_SPEED: float = game_config.player_speed
        self.ENEMY_SPEED: float = game_config.enemy_speed

        self._pacgum_chance_spawning: float = 0.70

    def create_level(
        self, maze_width: int, maze_height: int, first_instance: bool = False
    ) -> list[list[int]]:

        # Store the maze width & height in the class
        self.maze_width = maze_width
        self.maze_height = maze_height

        # Create the level
        generated_level: list[list[int]] = self._create_maze_level(
            first_instance
        )

        # Create the calculator
        self.calculator = SuperCalculator(
            maze_offset_x=self.factory.offset_x,
            maze_offset_y=self.factory.offset_y,
            maze_tile_size=self.factory.tile_size,
            maze_height=self.factory.height,
        )

        # Create all entities
        self._create_entity()

        # Create all collectibles
        self._create_collectibles()

        return generated_level

    # :---------------:
    #  PRIVATE METHODS
    # :---------------:

    def _create_maze_level(
        self, first_instance: bool = False
    ) -> list[list[int]]:
        # Instanciate the MazeFactory object
        self.factory = MazeFactory()

        # Create the Maze
        if first_instance:
            wall_data: list[list[int]] = self.factory.generate_maze(
                self.maze_width, self.maze_height,
                self.asset_manager.textures,
                ScreenSettings.WIDTH, ScreenSettings.HEIGHT, self.config.seed
            )
        else:
            wall_data: list[list[int]] = self.factory.generate_maze(
                self.maze_width, self.maze_height,
                self.asset_manager.textures,
                ScreenSettings.WIDTH, ScreenSettings.HEIGHT
            )
        # Store the maze in bytes for later calculations
        self.maze_bitmap: dict[tuple[int, int], int] = generate_bytes_maze(
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
                sprite_width=192/6, sprite_height=32,
                sprites_columns=6, sprites_count=6
            ),
            calculator=self.calculator,
            scale=(self.factory.tile_size * PLAYER_SCALE) / 32,
            speed=self.PLAYER_SPEED * ((self.factory.tile_size * PLAYER_SCALE) / 32)
        )

        # Create enemies
        self.cat_enemy: CatEnemy = CatEnemy(
            spawn_point=spawn_positions["cat_enemy"],
            sprite_sheet_move=load_sprite_sheet(
                textures=self.asset_manager.textures["enemy_cat_move"],
                sprite_width=128/4, sprite_height=32,
                sprites_columns=4, sprites_count=4
            ),
            sprite_sheet_eatable=load_sprite_sheet(
                textures=self.asset_manager.textures["enemy_cat_eatable"],
                sprite_width=128/4, sprite_height=32,
                sprites_columns=4, sprites_count=4
            ),
            sprite_sheet_died=load_sprite_sheet(
                textures=self.asset_manager.textures["enemy_cat_died"],
                sprite_width=128/4, sprite_height=32,
                sprites_columns=4, sprites_count=4
            ),
            maze_bitmap=self.maze_bitmap,
            calculator=self.calculator,
            player_ref=self.player,
            scale=(self.factory.tile_size * ENEMIES_SCALE) / 32,
            speed=self.ENEMY_SPEED * ((self.factory.tile_size * ENEMIES_SCALE) / 32)
        )
        self.enemies_list["cat_enemy"] = self.cat_enemy

        self.dog_enemy: DogEnemy = DogEnemy(
            spawn_point=spawn_positions["dog_enemy"],
            sprite_sheet_move=load_sprite_sheet(
                textures=self.asset_manager.textures["enemy_dog_move"],
                sprite_width=128/4, sprite_height=32,
                sprites_columns=4, sprites_count=4
            ),
            sprite_sheet_eatable=load_sprite_sheet(
                textures=self.asset_manager.textures["enemy_dog_eatable"],
                sprite_width=128/4, sprite_height=32,
                sprites_columns=4, sprites_count=4
            ),
            sprite_sheet_died=load_sprite_sheet(
                textures=self.asset_manager.textures["enemy_dog_died"],
                sprite_width=128/4, sprite_height=32,
                sprites_columns=4, sprites_count=4
            ),
            maze_bitmap=self.maze_bitmap,
            calculator=self.calculator,
            player_ref=self.player,
            scale=(self.factory.tile_size * ENEMIES_SCALE) / 32,
            speed=self.ENEMY_SPEED * ((self.factory.tile_size * ENEMIES_SCALE) / 32)
        )
        self.enemies_list["dog_enemy"] = self.dog_enemy

        self.fox_enemy: FoxEnemy = FoxEnemy(
            spawn_point=spawn_positions["fox_enemy"],
            sprite_sheet_move=load_sprite_sheet(
                textures=self.asset_manager.textures["enemy_fox_move"],
                sprite_width=128/4, sprite_height=32,
                sprites_columns=4, sprites_count=4
            ),
            sprite_sheet_eatable=load_sprite_sheet(
                textures=self.asset_manager.textures["enemy_fox_eatable"],
                sprite_width=128/4, sprite_height=32,
                sprites_columns=4, sprites_count=4
            ),
            sprite_sheet_died=load_sprite_sheet(
                textures=self.asset_manager.textures["enemy_fox_died"],
                sprite_width=128/4, sprite_height=32,
                sprites_columns=4, sprites_count=4
            ),
            maze_bitmap=self.maze_bitmap,
            calculator=self.calculator,
            player_ref=self.player,
            scale=(self.factory.tile_size * ENEMIES_SCALE) / 32,
            speed=self.ENEMY_SPEED * ((self.factory.tile_size * ENEMIES_SCALE) / 32)
        )
        self.enemies_list["fox_enemy"] = self.fox_enemy

        self.rat_enemy: RatEnemy = RatEnemy(
            spawn_point=spawn_positions["rat_enemy"],
            sprite_sheet_move=load_sprite_sheet(
                textures=self.asset_manager.textures["enemy_rat_move"],
                sprite_width=128/4, sprite_height=32,
                sprites_columns=4, sprites_count=4
            ),
            sprite_sheet_eatable=load_sprite_sheet(
                textures=self.asset_manager.textures["enemy_rat_eatable"],
                sprite_width=128/4, sprite_height=32,
                sprites_columns=4, sprites_count=4
            ),
            sprite_sheet_died=load_sprite_sheet(
                textures=self.asset_manager.textures["enemy_rat_died"],
                sprite_width=128/4, sprite_height=32,
                sprites_columns=4, sprites_count=4
            ),
            maze_bitmap=self.maze_bitmap,
            calculator=self.calculator,
            player_ref=self.player,
            scale=(self.factory.tile_size * ENEMIES_SCALE) / 32,
            speed=self.ENEMY_SPEED * ((self.factory.tile_size * ENEMIES_SCALE) / 32)
        )
        self.enemies_list["rat_enemy"] = self.rat_enemy

        self.enemy_speed = self.ENEMY_SPEED * ((self.factory.tile_size * ENEMIES_SCALE) / 32)

    def _create_collectibles(self) -> None:
        self._create_super_pacgum()
        self._create_pacgum()

    def _create_pacgum(self) -> None:
        self.pacgums_list.clear()

        # List of coords where pacgums can't spawn on
        forbidden_coords: list[tuple[int, int]] = [
            (self.player.spawn_point)
        ]

        # Get each corners of the maze and add it to the forbidden list
        corners_coords_list: dict[str, tuple[int, int]] = (
            self._get_corners_coords_pixels()
        )
        for coords in corners_coords_list.values():
            forbidden_coords.append(coords)

        first: bool = True

        # Traverse all case
        for coords, byte in self.maze_bitmap.items():
            # Ignore closed cells
            if byte == 1:
                continue

            # Ignore pair coords (avoid duplication)
            if coords[0] % 2 == 0 or coords[1] % 2 == 0:
                continue

            # Convert grid coords to pixels coords
            conv_coords_x: int = (coords[0] - 1) // 2
            conv_coords_y: int = (coords[1] - 1) // 2

            conv_coords: tuple[int, int] = self.calculator.get_grid_to_pixel(
                conv_coords_x, conv_coords_y
            )

            # Check if the coords are not forbidden
            if conv_coords in forbidden_coords:
                continue

            # Create the collectible and add it to the list with a chance %
            if random() <= self._pacgum_chance_spawning or first:

                collectible: Pacgum = Pacgum(
                    spawn_point=conv_coords,
                    sprite_path=self.asset_manager.textures["pacgum"],
                    calculator=self.calculator,
                    scale=(self.factory.tile_size * PACGUM_SCALE) / 40,
                    score=self.config.pacgum_points
                )
                self.pacgums_list.append(collectible)
                first = False

    def _create_super_pacgum(self) -> None:
        self.super_pacgums_list.clear()

        # Get the coordinates of each corners
        corners_coords_list: dict[str, tuple[int, int]] = (
            self._get_corners_coords_pixels()
        )

        # Create a super_pacgum for each corners
        for coords in corners_coords_list.values():
            collectible: SuperPacgum = SuperPacgum(
                spawn_point=coords,
                sprite=self.asset_manager.textures["super_pacgum"],
                calculator=self.calculator,
                scale=(self.factory.tile_size * SUPERPACGUM_SCALE) / 40,
                score=self.config.super_pacgum_points
            )
            self.super_pacgums_list.append(collectible)

    def _get_spawn_positions(self) -> dict[str, tuple[int, int]]:
        spawn_dict: dict[str, tuple[int, int]] = {}

        # Placing the player
        raw_x, raw_y = self._get_raw_coords(
            "player", (self.maze_width // 2, self.maze_height // 2)
        )

        # Get the coordinates in pixel
        x, y = self.calculator.get_grid_to_pixel(
            raw_x, raw_y
        )

        spawn_dict["player"] = (x, y)

        # Placing enemies
        #   FOX
        raw_x, raw_y = self._get_raw_coords(
            "fox_enemy", (self.maze_width - 1, self.maze_height - 1)
        )
        x, y = self.calculator.get_grid_to_pixel(
            raw_x, raw_y
        )
        spawn_dict["fox_enemy"] = (x, y)

        #   CAT
        raw_x, raw_y = self._get_raw_coords(
            "cat_enemy", (0, 0)
        )
        x, y = self.calculator.get_grid_to_pixel(
            raw_x, raw_y
        )
        spawn_dict["cat_enemy"] = (x, y)

        #   RAT
        raw_x, raw_y = self._get_raw_coords(
            "rat_enemy", (self.maze_width - 1, 0)
        )
        x, y = self.calculator.get_grid_to_pixel(
            raw_x, raw_y
        )
        spawn_dict["rat_enemy"] = (x, y)

        #   DOG
        raw_x, raw_y = self._get_raw_coords(
            "dog_enemy", (0, self.maze_height - 1)
        )
        x, y = self.calculator.get_grid_to_pixel(
            raw_x, raw_y
        )
        spawn_dict["dog_enemy"] = (x, y)

        return spawn_dict

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
            if self.maze_bitmap.get((row, col + case), 1) == 0:
                valid_coords = (row, col + case)
                break

            # Check case: south
            elif self.maze_bitmap.get((row, col - case), 1) == 0:
                valid_coords = (row, col - case)
                break

            # Check case: west
            elif self.maze_bitmap.get((row - case, col), 1) == 0:
                valid_coords = (row - case, col)
                break

            # Check case: west-north
            elif self.maze_bitmap.get((row - case, col + case), 1) == 0:
                valid_coords = (row - case, col + case)
                break

            # Check case: west-south
            elif self.maze_bitmap.get((row - case, col - case), 1) == 0:
                valid_coords = (row - case, col - case)
                break

            # Check case: east
            if self.maze_bitmap.get((row + case, col), 1) == 0:
                valid_coords = (row + case, col)
                break

            # Check case: north-east
            elif self.maze_bitmap.get((row + case, col - case), 1) == 0:
                valid_coords = (row + case, col - case)
                break

            # Check case: south-east
            elif self.maze_bitmap.get((row + case, col + case), 1) == 0:
                valid_coords = (row + case, col + case)
                break

            case += 1

        return valid_coords

    def _get_corners_coords_pixels(self) -> dict[str, tuple[int, int]]:
        corners_coords_list: dict[str, tuple[int, int]] = {}

        raw_upper_left: tuple[int, int] = self._get_raw_coords(
            "Super Pacgum (upper left)", (0, 0)
        )
        upper_left: tuple[int, int] = self.calculator.get_grid_to_pixel(
            raw_upper_left[0], raw_upper_left[1]
        )
        corners_coords_list["upper_left"] = upper_left

        raw_down_left: tuple[int, int] = self._get_raw_coords(
            "Super Pacgum (upper left)", (0, self.maze_height - 1)
        )
        down_left: tuple[int, int] = self.calculator.get_grid_to_pixel(
            raw_down_left[0], raw_down_left[1]
        )
        corners_coords_list["down_left"] = down_left

        raw_upper_right: tuple[int, int] = self._get_raw_coords(
            "Super Pacgum (upper left)", (self.maze_width - 1, 0)
        )
        upper_right: tuple[int, int] = self.calculator.get_grid_to_pixel(
            raw_upper_right[0], raw_upper_right[1]
        )
        corners_coords_list["upper_right"] = upper_right

        raw_down_right: tuple[int, int] = self._get_raw_coords(
            "Super Pacgum (upper left)", (self.maze_width - 1,
                                          self.maze_height - 1)
        )
        down_right: tuple[int, int] = self.calculator.get_grid_to_pixel(
            raw_down_right[0], raw_down_right[1]
        )
        corners_coords_list["down_right"] = down_right

        return corners_coords_list

    def _get_raw_coords(
        self, entity_name: str, coords: tuple[int, int]
    ) -> tuple[int, int]:

        x = coords[0]
        y = coords[1]

        extend_x = x * 2 + 1
        extend_y = y * 2 + 1

        # Is this position have cell open?
        if self.maze_bitmap[extend_x, extend_y] == 0:
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
