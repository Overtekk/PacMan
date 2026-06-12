# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  player.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 18:40:42 by roandrie        #+#    #+#               #
#  Updated: 2026/06/12 11:28:26 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from .entity import Movable
from src.utils import SuperCalculator
from src import game_config


class Player(Movable):
    """Player-controlled entity with animation and cheat-mode support.

    Attributes:
        base_speed (float): Default speed before any cheat modifiers.
        invincible (bool): True when a super pacgum effect is active.
        cheat_invincible (bool): True when invincibility cheat is enabled.
        cheat_speed (float): Extra speed added by cheat codes.
    """
    def __init__(
        self, spawn_point: tuple[int, int],
        sprite_sheet: list[arcade.Texture],
        calculator: SuperCalculator,
        scale: float = 1.0,
        speed: float = 100.0,
    ) -> None:
        """Initialize the Player.

        Args:
            spawn_point (tuple[int, int]): Starting pixel coordinates (x, y).
            sprite_sheet (list[arcade.Texture]): Ordered animation frames.
            calculator (SuperCalculator): Helper for coordinate conversions.
            scale (float, optional): Sprite scale factor. Defaults to 1.0.
            speed (float, optional): Movement speed in px/s. Defaults to 100.0.
        """

        super().__init__(
            spawn_point=spawn_point,
            sprite_sheet=sprite_sheet,
            calculator=calculator,
            scale=scale,
            speed=speed
        )
        self.base_speed = speed
        self.invincible: bool = False
        self.cheat_invincible: bool = False
        self.cheat_speed: float = 0

    def update(self, delta_time: float) -> None:
        """Update sprite facing direction and apply movement.

        Args:
            delta_time (float): Time elapsed since the last frame in seconds.
        """
        self._update_sprite_facing()

        super().update(delta_time)

    def die(self, _delta_time: float) -> None:
        """Handle player death by teleporting back to spawn point.

        Args:
            _delta_time (float): Unused, required by the abstract interface.
        """
        self.respawn()

    def increase_cheat_speed(self, value: float) -> None:
        """Increase the player speed by a given amount, capped at 400 px/s.

        Args:
            value (float): Amount to add to the current speed.
        """
        self.speed += value

        if self.speed > 400:
            self.speed = 400

    def decrease_cheat_speed(self, value: float) -> None:
        """Decrease the player speed by a given amount, floored at base speed.

        Args:
            value (float): Amount to subtract from the current speed.
        """
        self.speed -= value

        if self.speed < game_config.player_speed:
            self.speed = game_config.player_speed

    def _update_animation(self, delta_time: float) -> None:
        """Cycle through animation frames while the player is moving.

        Args:
            delta_time (float): Time elapsed since the last frame in seconds.
        """
        # Verify that the sprite is moving
        if (self.can_move and
                (self.current_direction[0] != 0 or
                 self.current_direction[1] != 0)):

            # Set the timer and update current texture
            self._animation_timer += delta_time

            if self._animation_timer > 0.02:
                self.current_texture_index = ((self.current_texture_index + 1)
                                              % len(self.textures))

                self.sprite.texture = self.textures[self.current_texture_index]

                self._animation_timer = 0

    def _update_sprite_facing(self) -> None:
        """
        Rotate and flip the sprite to face the current movement direction.
        """
        # Get the base scale of the sprite
        base_scale: float = abs(self.sprite.scale_x)

        # Move the facing in each direction based on the angle
        match self.current_direction:
            case (1.0, 0.0):
                self.sprite.angle = 0
                self.sprite.scale_x = base_scale

            case (-1.0, 0.0):
                self.sprite.angle = 0
                self.sprite.scale_x = -base_scale

            case (0.0, 1.0):
                self.sprite.angle = -90
                self.sprite.scale_x = base_scale

            case (0.0, -1.0):
                self.sprite.angle = 90
                self.sprite.scale_x = base_scale
