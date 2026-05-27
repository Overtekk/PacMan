# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  entity.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 18:09:46 by roandrie        #+#    #+#               #
#  Updated: 2026/05/27 09:28:17 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from abc import ABC, abstractmethod

from .logics.StateMachine import EnemyState
from src.utils import SuperCalculator

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.entity.player import Player


class Entity(ABC):
    def __init__(
        self, spawn_point: tuple[int, int],
        sprite_path_or_texture: str | arcade.Texture,
        calculator: SuperCalculator,
        scale: float = 1.0
    ) -> None:

        self.calculator = calculator

        # Logical coordinates
        self.spawn_point: tuple[int, int] = spawn_point
        self._x: float = float(spawn_point[0])
        self._y: float = float(spawn_point[1])

        # Create the sprite
        self.sprite = arcade.Sprite(
            path_or_texture=sprite_path_or_texture,
            scale=float(scale)
        )

        # Sync visual position with logical position
        self.sprite.center_x = self._x
        self.sprite.center_y = self._y

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @x.setter
    def x(self, new_value: float) -> None:
        self._x = new_value
        self.sprite.center_x = self._x

    @y.setter
    def y(self, new_value: float) -> None:
        self._y = new_value
        self.sprite.center_y = self._y

    def update(self, delta_time: float) -> None:
        pass


class Movable(Entity):
    def __init__(
        self,
        spawn_point: tuple[int, int],
        sprite_sheet: list[arcade.Texture],
        calculator: SuperCalculator,
        scale: float = 1.0,
        speed: float = 100.0
    ) -> None:

        self.textures: list[arcade.Texture] = sprite_sheet
        self.current_texture_index: int = 0

        super().__init__(spawn_point, self.textures[0], calculator, scale)

        self._base_facing: float = self.sprite.scale_x
        self._base_angle: float = self.sprite.angle

        self.speed: float = speed

        self._can_move: bool = False
        self._current_direction: tuple[float, float] = (0.0, 0.0)
        self._next_direction: tuple[float, float] = (0.0, 0.0)

        self._animation_timer = 0.0

    def update(self, delta_time: float) -> None:
        # Calulate the movement vector
        dx = self._current_direction[0] * self.speed * delta_time
        dy = self._current_direction[1] * self.speed * delta_time
        self.x += dx
        self.y += dy

        self._update_animation(delta_time)

    def respawn(self) -> None:
        self.x, self.y = self.spawn_point

    def reset_animation(self) -> None:
        self.sprite.scale_x = self._base_facing
        self.sprite.angle = self._base_angle
        self.sprite.texture = self.textures[0]
        self.current_texture_index = 0

    @abstractmethod
    def die(self) -> None:
        pass


class Enemy(Movable):
    def __init__(
        self,
        spawn_point: tuple[int, int],
        sprite_sheet_move: list[arcade.Texture],
        sprite_sheet_eatable: list[arcade.Texture],
        sprite_sheet_died: list[arcade.Texture],
        maze_bitmap: dict[tuple[int, int], str],
        calculator: SuperCalculator,
        player_reference: "Player",
        scale: float = 1.0,
        speed: float = 80.0,
        is_edible: bool = False,
        enemy_state: EnemyState = EnemyState.WAIT
    ) -> None:

        super().__init__(
            spawn_point, sprite_sheet_move, calculator, scale, speed
        )

        self.player_ref = player_reference

        self.sprite_sheet_eatable = sprite_sheet_eatable
        self.sprite_sheet_died = sprite_sheet_died

        self.maze_bitmap = maze_bitmap

        self._is_edible: bool = is_edible
        self._mode = enemy_state

        self._move_timer: float = 0.0

        self.last_movement: tuple[float, float] = (0.0, 0.0)

    @property
    def is_edible(self) -> bool:
        return self._is_edible

    @is_edible.setter
    def is_edible(self, value: bool) -> None:
        self._is_edible = value

    @property
    def mode(self) -> EnemyState:
        return self._mode

    @mode.setter
    def mode(self, new_state: EnemyState) -> None:
        self._mode = new_state

    def update(self, delta_time: float) -> None:
        self._state_machine()
        self._update_sprite()
        super().update(delta_time)

    def _state_machine(self) -> None:
        if self.mode == EnemyState.WAIT:
            pass

        elif self.mode == EnemyState.WANDER:
            pass

        elif self.mode == EnemyState.SEARCH:
            pass

        elif self.mode == EnemyState.CHASE:
            self._chase_player(self.player_ref)

        elif self.mode == EnemyState.RUNAWAY:
            pass

        elif self.mode == EnemyState.RESPAWN:
            self._return_to_spawnpoint()

    def _chase_player(self, player: "Player") -> None:
        # Convert player position from pixels to grid
        conv_player_pos: tuple[float, float] = (
            self.calculator.get_pixel_to_grid_any(player.x, player.y)
        )

        # Convert his position from pixels to grid
        conv_x, conv_y = self.calculator.get_pixel_to_grid_entity(self)

        # Prevent return to last position
        if (conv_x, conv_y) == self.last_movement:
            return

        self.last_movement = (conv_x, conv_y)

        # Check all available walls
        open_walls: dict[tuple[int, int], tuple[int, int]] = (
            self.calculator.check_open_wall(conv_x, conv_y, self.maze_bitmap)
        )

        # Move to the only wall available
        if len(open_walls) == 1:
            self._next_direction = list(open_walls.keys()).pop()
            return

        # Remove the inverted direction from the current one (avoiding loop)
        if not self._current_direction == (0.0, 0.0):
            curr_dir_x: float = self._current_direction[0] * -1
            curr_dir_y: float = self._current_direction[1] * -1

            if (curr_dir_x, curr_dir_y) in open_walls:
                open_walls.pop((curr_dir_x, curr_dir_y))

        # Variable to compare and store the result
        best_distance: float = float('+inf')
        direction: tuple[float, float] = (0.0, 0.0)

        for key, coords in open_walls.items():
            # Calculate the distance between coords and spawnpoint
            distance: float = (
                self.calculator.get_euclidean_distance(coords, conv_player_pos)
            )

            # Compare result and store it
            if best_distance > distance:
                best_distance = distance
                direction = key

        self._next_direction = direction

    def _return_to_spawnpoint(self) -> None:
        # Convert the spawnpoint from pixels to grid
        conv_spawn_point: tuple[float, float] = (
            self.calculator.get_pixel_to_grid_any(self.spawn_point[0],
                                                  self.spawn_point[1])
        )

        # Convert its position from pixels to grid
        conv_x, conv_y = self.calculator.get_pixel_to_grid_entity(self)

        # Prevent return to last position
        if (conv_x, conv_y) == self.last_movement:
            return

        self.last_movement = (conv_x, conv_y)

        # Check that the entity is not arrived
        if (conv_x, conv_y) == conv_spawn_point:
            print("youhou")
            self.mode = EnemyState.WAIT
            return

        # Check all available walls
        open_walls: dict[tuple[int, int], tuple[int, int]] = (
            self.calculator.check_open_wall(conv_x, conv_y, self.maze_bitmap)
        )

        # Move to the only wall available
        if len(open_walls) == 1:
            self._next_direction = list(open_walls.keys()).pop()
            return

        # Remove the inverted direction from the current one (avoiding loop)
        if not self._current_direction == (0.0, 0.0):
            curr_dir_x: float = self._current_direction[0] * -1
            curr_dir_y: float = self._current_direction[1] * -1

            if (curr_dir_x, curr_dir_y) in open_walls:
                open_walls.pop((curr_dir_x, curr_dir_y))

        # Variable to compare and store the result
        best_distance: float = float('+inf')
        direction: tuple[float, float] = (0.0, 0.0)

        for key, coords in open_walls.items():
            # Calculate the distance between coords and spawnpoint
            distance: float = (
                self.calculator.get_euclidean_distance(coords,
                                                       conv_spawn_point)
            )

            # Compare result and store it
            if best_distance > distance:
                best_distance = distance
                direction = key

        self._next_direction = direction

    def _update_animation(self, delta_time: float) -> None:
        match self._current_direction:
            case (1.0, 0.0):
                self.current_texture_index = 0
            case (-1.0, 0.0):
                self.current_texture_index = 1
            case (0.0, -1.0):
                self.current_texture_index = 2
            case (0.0, 1.0):
                self.current_texture_index = 3

    def _update_sprite(self) -> None:
        if self.mode == EnemyState.RESPAWN:
            self.sprite.texture = self.sprite_sheet_died[self.current_texture_index]
        elif self.mode == EnemyState.RUNAWAY:
            self.sprite.texture = self.sprite_sheet_eatable[self.current_texture_index]
        else:
            self.sprite.texture = self.textures[self.current_texture_index]


class Collectible(Entity):
    def __init__(
        self,
        spawn_point: tuple[int, int],
        sprite_data: str | arcade.Texture,
        calculator: SuperCalculator,
        scale: float = 1.0,
        score: int = 0
    ) -> None:

        super().__init__(spawn_point, sprite_data, calculator, scale)

        self.sprite.parent = self

        self._score: int = score

    @property
    def score(self) -> int:
        return self._score
