# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  super_pacgum.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/14 19:09:02 by roandrie        #+#    #+#               #
#  Updated: 2026/06/01 11:36:05 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any

from pathlib import Path

from src import game_config
from ..entity import Collectible, Enemy
from ..player import Player
from ..logics.StateMachine import EnemyState
from src.utils import SuperCalculator, print_log


class SuperPacgum(Collectible):
    def __init__(
        self, spawn_point: tuple[int, int],
        sprite: str | Path,
        calculator: SuperCalculator,
        scale: float = 1.0,
        score: int = 0
    ) -> None:

        super().__init__(
            spawn_point=spawn_point,
            sprite_data=sprite,
            calculator=calculator,
            scale=scale,
            score=score
        )

        self._power_up_time: float = 0.0
        self._is_activate: bool = False

    @property
    def is_activate(self) -> bool:
        return self._is_activate

    def update(self, delta_time: float) -> None:
        # Elapsed time
        self._power_up_time += delta_time

        # Blinking logic
        warning: float = game_config.time_power_up - 3.0
        blink_speed: float = 0.30

        if warning <= self._power_up_time < game_config.time_power_up:
            is_blinking: bool = (
                (self._power_up_time % (blink_speed * 2)) < blink_speed
            )
            self._apply_blinking(is_blinking)

        # Disable power up
        if self._power_up_time > game_config.time_power_up:
            self._deactivate_effect()

    def activate_power(
        self, player_reference: Player, enemies_reference: list[str, Any]
    ) -> None:

        # Store the player & enemy object reference
        self._player_ref: Player = player_reference
        self._enemy_ref: Enemy = enemies_reference

        # Activate the player invincibility
        player_reference.invincible = True
        self._is_activate = True

        # Change state of all enemies
        for enemy in enemies_reference.values():
            if enemy.died:
                continue

            enemy.mode = EnemyState.RUNAWAY
            enemy.is_edible = True
            enemy.sprite.color = (64, 99, 193)
            enemy.speed = (
                game_config.enemy_speed - game_config.ennemy_speed_reduction)

            # Turn the enemy
            x: float = enemy.current_direction[0] * -1
            y: float = enemy.current_direction[1] * -1
            enemy.current_direction = (x, y)

            if game_config.debug_mode:
                print_log(f"Changed state for {enemy} to RUNAWAY")

    # :---------------:
    #  PRIVATE METHODS
    # :---------------:

    def _apply_blinking(self, is_blinking: bool) -> None:
        for enemy in self._enemy_ref.values():

            if enemy.died:
                continue

            if is_blinking:
                enemy.sprite.color = (255, 255, 255)
            else:
                enemy.sprite.color = (64, 99, 193)

    def _deactivate_effect(self) -> None:
        self._is_activate = False

        self._player_ref.invincible = False

        for enemy in self._enemy_ref.values():
            if enemy.died:
                continue

            enemy.mode = EnemyState.WANDER
            enemy.is_edible = False
            enemy.sprite.color = (255, 255, 255)
            enemy.speed = game_config.enemy_speed

            if game_config.debug_mode:
                print_log(f"Changed state for {enemy} to WANDER")

        if game_config.debug_mode:
            print_log("DISABLE SUPERPACGUM")
