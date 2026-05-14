# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  entity.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 18:09:46 by roandrie        #+#    #+#               #
#  Updated: 2026/05/14 21:30:56 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from abc import ABC, abstractmethod
from pathlib import Path


class Entity(ABC):
    def __init__(
        self, spawn_point: tuple[int, int],
        sprite_path: Path,
        scale: float = 1.0
    ) -> None:

        # Logical coordinates
        self.spawn_point: tuple[int, int] = spawn_point
        self._x: float = float(spawn_point[0])
        self._y: float = float(spawn_point[1])

        # Visual representation (Composition)
        self.sprite = arcade.Sprite(filename=sprite_path, scale=scale)

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


class Movable(ABC):
    def __init__(
        self, speed: float = 0.0
    ) -> None:

        self.speed: float = speed

    @abstractmethod
    def move(self, direction: tuple[float, float]) -> None:
        pass

    @abstractmethod
    def die(self) -> None:
        pass


class Enemy(ABC):
    def __init__(
        self, is_edible: bool = False
    ) -> None:

        self._is_edible: bool = is_edible

    @property
    def is_edible(self) -> bool:
        return self._is_edible

    @is_edible.setter
    def is_edible(self, value: bool) -> None:
        self._is_edible = value


class Collectible(ABC):
    def __init__(
        self, score: int = 0
    ) -> None:

        self._score: int = score
        self._collected: bool = False

    @property
    def score(self) -> int:
        return self._score

    @abstractmethod
    def activate_power(self) -> None:
        pass
