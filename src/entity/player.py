# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  player.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 18:40:42 by roandrie        #+#    #+#               #
#  Updated: 2026/06/10 13:42:33 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import arcade

from .entity import Movable
from src.utils import SuperCalculator
from src import game_config


class Player(Movable):
    def __init__(
        self, spawn_point: tuple[int, int],
        sprite_sheet: list[arcade.Texture],
        calculator: SuperCalculator,
        scale: float = 1.0,
        speed: float = 100.0,
    ) -> None:

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
        self._update_sprite_facing()

        super().update(delta_time)

    def die(self, _delta_time: float) -> None:
        self.respawn()

    def increase_cheat_speed(self, value: float) -> None:
        self.speed += value

        if self.speed > 400:
            self.speed = 400

    def decrease_cheat_speed(self, value: float) -> None:
        self.speed -= value

        if self.speed < game_config.player_speed:
            self.speed = game_config.player_speed

    def _update_animation(self, delta_time: float) -> None:
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
