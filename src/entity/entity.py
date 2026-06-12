# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  entity.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 18:09:46 by roandrie        #+#    #+#               #
#  Updated: 2026/06/12 11:26:47 by anacharp        ###   ########.fr        #
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
    """Abstract base class for all game entities.

    Handles the logical position and the associated Arcade sprite.
    Position properties keep the sprite in sync with the logical coordinates.

    Attributes:
        calculator (SuperCalculator): Coordinate conversion helper.
        spawn_point (tuple[int, int]): Initial pixel position.
        sprite (arcade.Sprite): The visual representation of the entity.
    """

    def __init__(
        self, spawn_point: tuple[int, int],
        sprite_path_or_texture: str | arcade.Texture,
        calculator: SuperCalculator,
        scale: float = 1.0
    ) -> None:
        """Initialize an Entity.

        Args:
            spawn_point (tuple[int, int]): Starting pixel coordinates (x, y).
            sprite_path_or_texture (str | arcade.Texture): Path to the sprite
                image or an already loaded Arcade Texture.
            calculator (SuperCalculator): Helper for coordinate conversions.
            scale (float, optional): Scale factor for the sprite. Defaults to
            1.0.
        """

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
        """float: Logical x position, kept in sync with the sprite."""
        return self._x

    @x.setter
    def x(self, new_value: float) -> None:
        self._x = new_value
        self.sprite.center_x = self._x

    @property
    def y(self) -> float:
        """float: Logical y position, kept in sync with the sprite."""
        return self._y

    @y.setter
    def y(self, new_value: float) -> None:
        self._y = new_value
        self.sprite.center_y = self._y

    @abstractmethod
    def update(self, delta_time: float) -> None:
        """Update the entity state for the current frame.

        Args:
            delta_time (float): Time elapsed since the last frame in seconds.
        """
        pass


class Movable(Entity):
    """Abstract entity that can move and be animated.

    Extends Entity with a sprite sheet, speed, directional movement,
    and an animation system.

    Attributes:
        textures (list[arcade.Texture]): Frames of the sprite sheet.
        can_move (bool): Whether movement is currently allowed.
        speed (float): Movement speed in pixels per second.
        current_direction (tuple[float, float]): Active movement vector.
        _next_direction (tuple[float, float]): Buffered next direction.
    """

    def __init__(
        self,
        spawn_point: tuple[int, int],
        sprite_sheet: list[arcade.Texture],
        calculator: SuperCalculator,
        scale: float = 1.0,
        speed: float = 100.0
    ) -> None:
        """Initialize a Movable entity.

        Args:
            spawn_point (tuple[int, int]): Starting pixel coordinates (x, y).
            sprite_sheet (list[arcade.Texture]): Ordered list of animation
            frames.
            calculator (SuperCalculator): Helper for coordinate conversions.
            scale (float, optional): Sprite scale factor. Defaults to 1.0.
            speed (float, optional): Movement speed in px/s. Defaults to 100.0.
        """

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
        """Move the entity and update the animation.

        Args:
            delta_time (float): Time elapsed since the last frame in seconds.
        """
        dx = self.current_direction[0] * self.speed * delta_time
        dy = self.current_direction[1] * self.speed * delta_time
        self.x += dx
        self.y += dy

        self._update_animation(delta_time)

    def respawn(self) -> None:
        """Teleport the entity back to its spawn point."""
        self.x, self.y = self.spawn_point

    def reset_animation(self) -> None:
        """Reset sprite orientation and texture to the initial state."""
        self.sprite.scale_x = self._base_facing
        self.sprite.angle = self._base_angle
        self.sprite.texture = self.textures[0]
        self.current_texture_index = 0

    @abstractmethod
    def _update_animation(self, delta_time: float) -> None:
        """Update the current animation frame.

        Args:
            delta_time (float): Time elapsed since the last frame in seconds.
        """
        pass

    @abstractmethod
    def die(self, delta_time: float) -> None:
        """Handle the death of this entity.

        Args:
            delta_time (float): Time elapsed since the last frame in seconds.
        """
        pass


class Enemy(Movable):
    """Movable enemy entity with AI, state machine, and multiple sprite sheets.

    Delegates movement logic to an EnemyBrain instance and switches between
    three sprite sheets depending on the current state (normal, eatable, died).

    Attributes:
        sprite_sheet_eatable (list[arcade.Texture]): Frames for eatable state.
        sprite_sheet_died (list[arcade.Texture]): Frames for died/respawn
        state.
        maze_bitmap (dict[tuple[int, int], int]): Walkability map of the maze.
        player_ref (Player): Reference to the player entity.
        base_speed (float): Default movement speed before modifiers.
        brain (EnemyBrain): AI brain handling state transitions and movement.
    """

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
        angry: bool = False,
        enemy_state: EnemyState = EnemyState.WAIT
    ) -> None:
        """Initialize an Enemy.

        Args:
            spawn_point (tuple[int, int]): Starting pixel coordinates (x, y).
            sprite_sheet_move (list[arcade.Texture]): Normal movement frames.
            sprite_sheet_eatable (list[arcade.Texture]): Eatable state frames.
            sprite_sheet_died (list[arcade.Texture]): Died/respawn state
            frames.
            maze_bitmap (dict[tuple[int, int], int]): Maze walkability map.
            calculator (SuperCalculator): Helper for coordinate conversions.
            player_reference (Player): Reference to the player entity.
            scale (float): Sprite scale factor.
            speed (float): Base movement speed in px/s.
            is_edible (bool, optional): Whether the enemy can be eaten.
                Defaults to False.
            angry (bool, optional): Whether the enemy starts in angry mode.
                Defaults to False.
            enemy_state (EnemyState, optional): Initial AI state.
                Defaults to EnemyState.WAIT.
        """

        super().__init__(
            spawn_point, sprite_sheet_move, calculator, scale, speed
        )

        self.sprite_sheet_eatable = sprite_sheet_eatable
        self.sprite_sheet_died = sprite_sheet_died
        self.maze_bitmap = maze_bitmap
        self.player_ref = player_reference

        self.base_speed = speed

        self.sprite.parent = self

        # - Private variables -
        self._died: bool = False
        self._is_edible = is_edible
        self._angry = angry
        self._mode = enemy_state
        self._timer_check_respawn: float = game_config.enemy_check_res_timer
        self._have_respawned: bool = False

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
        """bool: Whether the enemy can currently be eaten by the player."""
        return self._is_edible

    @is_edible.setter
    def is_edible(self, value: bool) -> None:
        self._is_edible = value

    @property
    def mode(self) -> EnemyState:
        """EnemyState: Current AI state of the enemy."""
        return self._mode

    @mode.setter
    def mode(self, new_state: EnemyState) -> None:
        self._mode = new_state

    @property
    def died(self) -> bool:
        """bool: Whether the enemy has been eaten and is in its died state."""
        return self._died

    @property
    def have_respawned(self) -> bool:
        """bool: Whether the enemy has completed a respawn cycle."""
        return self._have_respawned

    @have_respawned.setter
    def have_respawned(self, new_value: bool) -> None:
        self._have_respawned = new_value

    @property
    def angry(self) -> bool:
        """bool: Whether the enemy is in angry mode."""
        return self._angry

    @angry.setter
    def angry(self, new_value: bool) -> None:
        self._angry = new_value

    def update(self, delta_time: float) -> None:
        """Update the enemy: run AI brain, update sprite, apply movement.

        Args:
            delta_time (float): Time elapsed since the last frame in seconds.
        """
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
        """Trigger the enemy death sequence when eaten by the player.

        Switches the enemy to the RESPAWN state and makes it semi-transparent.

        Args:
            delta_time (float): Time elapsed since the last frame in seconds.
        """
        if self._is_edible:
            self._died = True
            self._is_edible = False
            self.sprite.texture = self.sprite_sheet_died[
                self.current_texture_index
            ]
            self.sprite.alpha = 50
            self.mode = EnemyState.RESPAWN

            if game_config.debug_mode:
                print_log(f"Changed state for {self} to RESPAWN")

    def _update_animation(self, _delta_time: float) -> None:
        """Select the correct animation frame based on the current direction.

        Args:
            _delta_time (float): Unused, required by the abstract interface.
        """
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
        """Switch the active sprite sheet based on the current AI state."""
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
    """Static collectible entity placed in the maze.

    Attributes:
        score (int): Points awarded to the player upon collection.
    """

    def __init__(
        self,
        spawn_point: tuple[int, int],
        sprite_data: str | arcade.Texture,
        calculator: SuperCalculator,
        scale: float = 1.0,
        score: int = 0
    ) -> None:
        """Initialize a Collectible.

        Args:
            spawn_point (tuple[int, int]): Pixel position of the collectible.
            sprite_data (str | arcade.Texture): Sprite path or texture.
            calculator (SuperCalculator): Helper for coordinate conversions.
            scale (float, optional): Sprite scale factor. Defaults to 1.0.
            score (int, optional): Points awarded on collection. Defaults to 0.
        """

        super().__init__(spawn_point, sprite_data, calculator, scale)

        self.sprite.parent = self
        self._score: int = score

    @property
    def score(self) -> int:
        """int: Points awarded to the player upon collecting this item."""
        return self._score

    def update(self, delta_time: float) -> None:
        """No-op update for static collectibles.

        Args:
            delta_time (float): Unused.
        """
        pass
