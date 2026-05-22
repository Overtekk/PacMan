# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  entity.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 18:09:46 by roandrie        #+#    #+#               #
#  Updated: 2026/05/21 15:21:59 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from abc import ABC, abstractmethod

from .enemies.logics.StateMachine import EnemyState


class Entity(ABC):
    def __init__(
        self, spawn_point: tuple[int, int],
        sprite_path_or_texture: str | arcade.Texture,
        scale: float = 1.0
    ) -> None:

        # Logical coordinates
        self.spawn_point: tuple[int, int] = spawn_point
        self._x: float = float(spawn_point[0])
        self._y: float = float(spawn_point[1])

        # On utilise 'texture=' au lieu de 'filename='
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

    def update(self, delta: float) -> None:
        pass

    def respawn(self) -> None:
        self.x, self.y = self.spawn_point


class Movable(Entity):
    def __init__(
        self,
        spawn_point: tuple[int, int],
        sprite_sheet: list[arcade.Texture],
        scale: float = 1.0,
        speed: float = 100.0
    ) -> None:

        self.textures: list[arcade.Texture] = sprite_sheet
        self.current_texture_index: int = 0

        super().__init__(spawn_point, self.textures[0], scale)

        self.speed: float = speed

        self._can_move: bool = False
        self._current_direction: tuple[float, float] = (0.0, 0.0)

        self._animation_timer = 0.0

    def move(self, direction: tuple[float, float]) -> None:
        # Change the current direction of the entity
        if self._can_move:
            self._current_direction = direction
        else:
            self._current_direction = (0.0, 0.0)

    def update(self, delta: float) -> None:
        # Calulate the movement vector
        dx = self._current_direction[0] * self.speed * delta
        dy = self._current_direction[1] * self.speed * delta
        self.x += dx
        self.y += dy

        self._update_animation(delta)
        self._update_sprite_facing()

    def _update_animation(self, delta: float) -> None:
        # Verify that the sprite is moving
        if (self._can_move and
                (self._current_direction[0] != 0 or
                 self._current_direction[1] != 0)):

            # Set the timer and update current texture
            self._animation_timer += delta

            if self._animation_timer > 0.05:
                self.current_texture_index = ((self.current_texture_index + 1)
                                                % len(self.textures))

                self.sprite.texture = self.textures[self.current_texture_index]

                self._animation_timer = 0

    def _update_sprite_facing(self) -> None:
        # Get the base scale of the sprite
        base_scale: float = abs(self.sprite.scale_x)

        # Move the facing in each direction based on the angle
        match self._current_direction:
            case (1.0, 0.0):
                self.sprite.angle = 0
                self.sprite.scale_x = base_scale

            case (-1.0, 0.0):
                self.sprite.angle = 0
                self.sprite.scale_x = -base_scale


    @abstractmethod
    def die(self) -> None:
        pass


class Enemy(Movable):
    def __init__(
        self,
        spawn_point: tuple[int, int],
        sprite_sheet: list[arcade.Texture],
        scale: float = 1.0,
        speed: float = 80.0,
        is_edible: bool = False,
        mode: EnemyState = EnemyState.WANDER
    ) -> None:

        super().__init__(spawn_point, sprite_sheet, scale, speed)

        self._is_edible: bool = is_edible
        self._mode = mode

        self._move_timer: float = 0.0

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


class Collectible(Entity):
    def __init__(
        self,
        spawn_point: tuple[int, int],
        sprite_data: str | arcade.Texture,
        scale: float = 1.0,
        score: int = 0
    ) -> None:

        super().__init__(spawn_point, sprite_data, scale)

        self._score: int = score
        self._collected: bool = False

    @property
    def score(self) -> int:
        return self._score

    @abstractmethod
    def activate_power(self) -> None:
        pass
