# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  entity.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 18:09:46 by roandrie        #+#    #+#               #
#  Updated: 2026/06/02 11:05:12 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from abc import ABC, abstractmethod

from .logics.StateMachine import EnemyState
from .logics.brain import EnemyBrain
from src.utils import SuperCalculator, print_log
from src import game_config

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

    @x.setter
    def x(self, new_value: float) -> None:
        self._x = new_value
        self.sprite.center_x = self._x

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, new_value: float) -> None:
        self._y = new_value
        self.sprite.center_y = self._y

    @abstractmethod
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

        self.can_move: bool = False
        self._base_facing: float = self.sprite.scale_x
        self._base_angle: float = self.sprite.angle
        self.speed: float = speed

        self.current_direction: tuple[float, float] = (0.0, 0.0)
        self._next_direction: tuple[float, float] = (0.0, 0.0)
        self._animation_timer = 0.0

    def update(self, delta_time: float) -> None:
        dx = self.current_direction[0] * self.speed * delta_time
        dy = self.current_direction[1] * self.speed * delta_time
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
    def _update_animation(self, delta_time: float) -> None:
        pass

    @abstractmethod
    def die(self, delta_time: float) -> None:
        pass


class Enemy(Movable):
    def __init__(
        self,
        spawn_point: tuple[int, int],
        sprite_sheet_move: list[arcade.Texture],
        sprite_sheet_eatable: list[arcade.Texture],
        sprite_sheet_died: list[arcade.Texture],
        maze_bitmap: dict[tuple[int, int], int],
        calculator: SuperCalculator,
        player_reference: "Player",
        scale: float,
        speed: float,
        is_edible: bool = False,
        enemy_state: EnemyState = EnemyState.WAIT
    ) -> None:

        super().__init__(
            spawn_point, sprite_sheet_move, calculator, scale, speed
        )

        self.sprite_sheet_eatable = sprite_sheet_eatable
        self.sprite_sheet_died = sprite_sheet_died
        self.maze_bitmap = maze_bitmap
        self.player_ref = player_reference
        self._is_edible = is_edible
        self._mode = enemy_state

        self.base_speed = speed

        self.sprite.parent = self

        self._died: bool = False

        # Internal AI components
        self.brain = EnemyBrain(self)
        self._timer_chase: float = 0.0
        self._loose_chance: float = 0.7
        self._wait_revive: bool = False
        self._revive_timer: float = 0.0
        self.last_movement: tuple[float, float] = (0.0, 0.0)
        self._debug_raycast: tuple[float, float] = (0.0, 0.0)

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

    @property
    def died(self) -> bool:
        return self._died

    def update(self, delta_time: float) -> None:
        # Delegate logic execution to the brain
        if self.can_move:
            self.brain.update(delta_time)
        else:
            self._next_direction = (0.0, 0.0)
            self.current_direction = (0.0, 0.0)

        self._update_sprite()

        # Apply physics calculations from Movable
        super().update(delta_time)

    def die(self, delta_time: float) -> None:
        if self._is_edible:
            self._died = True
            self._is_edible = False
            self.mode = EnemyState.RESPAWN

            if game_config.debug_mode:
                print_log(f"Changed state for {self} to RESPAWN")

    def _update_animation(self, _delta_time: float) -> None:
        match self.current_direction:
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
            self.sprite.texture = self.sprite_sheet_died[
                self.current_texture_index
            ]
        elif self.mode == EnemyState.RUNAWAY:
            self.sprite.texture = self.sprite_sheet_eatable[
                self.current_texture_index
            ]
        elif not self._wait_revive:
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

    def update(self, delta_time: float) -> None:
        pass
