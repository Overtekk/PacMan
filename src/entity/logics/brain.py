# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  brain.py                                          :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/29 14:10:28 by roandrie        #+#    #+#               #
#  Updated: 2026/06/04 10:46:25 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import random

from .StateMachine import EnemyState
from src import game_config
from src.utils import print_log

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.entity.entity import Enemy

# CHASE_SPEED: float = game_config.chase_speed


class EnemyBrain():
    def __init__(self, enemy_ref: "Enemy") -> None:
        self.enemy: Enemy = enemy_ref

    def update(self, delta_time: float) -> None:
        if self.enemy.mode not in [EnemyState.WAIT, EnemyState.CHASE]:
            self._raycasting()

        self._state_machine(delta_time)

    def _state_machine(self, delta_time: float) -> None:
        if self.enemy.mode == EnemyState.WAIT:
            if self.enemy._wait_revive:
                self._revive(delta_time)

        elif self.enemy.mode == EnemyState.WANDER:
            self._move()

        elif self.enemy.mode == EnemyState.SEARCH:
            pass

        elif self.enemy.mode == EnemyState.CHASE:
            self.enemy.speed = (
                self.enemy.base_speed + (self.enemy.base_speed//10)
            )
            self._chase_player(delta_time)

        elif self.enemy.mode == EnemyState.RUNAWAY:
            self._runaway_from_player()

        elif self.enemy.mode == EnemyState.RESPAWN:
            self._return_to_spawnpoint()

            self.enemy._timer_check_respawn -= delta_time

            if self.enemy._timer_check_respawn < 0.0:
                self.enemy.respawn()
                self.enemy._timer_check_respawn = (
                    game_config.enemy_check_res_timer
                )

    # :---------------:
    #  PRIVATE METHODS
    # :---------------:

    def _get_available_moves(
        self
    ) -> dict[tuple[float, float], tuple[int, int]]:

        # Convert position from pixels to grid
        conv_x, conv_y = (
            self.enemy.calculator.get_pixel_to_grid_entity(self.enemy)
        )

        # Prevent recalculating on the same tile
        if ((conv_x, conv_y) == self.enemy.last_movement and
                self.enemy.current_direction != (0.0, 0.0)):
            return {}

        self.enemy.last_movement = (conv_x, conv_y)

        # Check all available walls
        open_walls: dict[tuple[int, int], tuple[int, int]] = (
            self.enemy.calculator.check_open_wall(
                conv_x, conv_y, self.enemy.maze_bitmap))

        # Dead end handling: Move to the only wall available
        if len(open_walls) == 1:
            return open_walls

        # Remove the inverted direction from the current one to avoid looping
        if self.enemy.current_direction != (0.0, 0.0):
            curr_dir_x: float = self.enemy.current_direction[0] * -1.0
            curr_dir_y: float = self.enemy.current_direction[1] * -1.0

            if (curr_dir_x, curr_dir_y) in open_walls:
                open_walls.pop((curr_dir_x, curr_dir_y))

        # Anti-stuck fallback: If unexpected collision logic empties the list
        if len(open_walls) == 0:
            fallback_x: float = self.enemy.current_direction[0] * -1.0
            fallback_y: float = self.enemy.current_direction[1] * -1.0
            open_walls[(fallback_x, fallback_y)] = (int(conv_x), int(conv_y))

            if game_config.debug_mode:
                print_log(
                    f"Fallback triggered for {self.enemy}. Forcing 180 turn."
                )

        return open_walls

    def _raycasting(self) -> bool:
        CHECK_DISTANCE: int = 4

        if self.enemy.mode in (
            EnemyState.WAIT, EnemyState.RUNAWAY, EnemyState.RESPAWN
        ):
            return False

        if self.enemy.current_direction == (0.0, 0.0):
            return False

        ext_self = (
            self.enemy.calculator.get_pixel_to_grid_entity(self.enemy)
        )
        ext_player = (
            self.enemy.calculator.get_pixel_to_grid_entity(
                self.enemy.player_ref))

        dir_x: float = self.enemy.current_direction[0]
        dir_y: float = self.enemy.current_direction[1]

        dx: int = int(ext_self[0])
        dy: int = int(ext_self[1])

        player_found: bool = False

        for i in range(1, CHECK_DISTANCE + 1):
            wall_x: int = int(ext_self[0] + dir_x * (2 * i - 1))
            wall_y: int = int(ext_self[1] + dir_y * -1 * (2 * i - 1))

            dx = int(ext_self[0] + dir_x * (2 * i))
            dy = int(ext_self[1] + dir_y * -1 * (2 * i))

            # WALL
            if self.enemy.maze_bitmap.get((wall_x, wall_y), 1) == 1:
                dx = int(ext_self[0] + dir_x * (2 * (i - 1)))
                dy = int(ext_self[1] + dir_y * -1 * (2 * (i - 1)))
                break

            # PLAYER FOUND
            if (dx, dy) == (int(ext_player[0]), int(ext_player[1])):
                if self.enemy.mode != EnemyState.CHASE:
                    self.enemy.mode = EnemyState.CHASE

                    if game_config.debug_mode:
                        print_log(f"Changed state for {self.enemy} to CHASE")

                player_found = True
                break

        # Debug raycast extraction
        normal_x: float = (dx - 1) / 2.0
        normal_y: float = (dy - 1) / 2.0
        self.enemy._debug_raycast = (
            self.enemy.calculator.get_grid_to_pixel(normal_x, normal_y)
        )

        return player_found

    def _chase_player(self, delta_time: float) -> None:
        MAX_TIME_TO_FORGET: float = 7.0
        player_found: bool = self._raycasting()

        if not player_found:
            self.enemy._timer_chase += delta_time

            if self.enemy._timer_chase > MAX_TIME_TO_FORGET:

                if random.random() <= self.enemy._loose_chance:
                    self.enemy.speed = self.enemy.base_speed - (self.enemy.base_speed//10)

                    self.enemy.mode = EnemyState.WANDER
                    self.enemy._timer_chase = 0.0

                    if game_config.debug_mode:
                        print_log(f"Changed state for {self.enemy} to WANDER")

        open_walls = self._get_available_moves()
        if not open_walls:
            return

        # Pop single available move immediately to skip loop
        if len(open_walls) == 1:
            self.enemy._next_direction = list(open_walls.keys()).pop()
            return

        conv_player_pos: tuple[float, float] = (
            self.enemy.calculator.get_pixel_to_grid_any(
                self.enemy.player_ref.x, self.enemy.player_ref.y))

        best_distance: float = float('inf')
        direction: tuple[float, float] = (0.0, 0.0)
        TURN_PENALTY: float = 0.2

        for key, coords in open_walls.items():
            distance: float = self.enemy.calculator.get_euclidean_distance(
                coords, conv_player_pos
            )

            # Apply momentum penalty if the path forces a turn
            if (key != self.enemy.current_direction and
                    self.enemy.current_direction != (0.0, 0.0)):
                distance += TURN_PENALTY

            if distance < best_distance:
                best_distance = distance
                direction = key

        self.enemy._next_direction = direction

    def _runaway_from_player(self) -> None:
        open_walls = self._get_available_moves()
        if not open_walls:
            return

        self.enemy._next_direction = self._apply_momentum_choice(open_walls)

    def _return_to_spawnpoint(self) -> None:
        conv_spawn_point: tuple[float, float] = (
            self.enemy.calculator.get_pixel_to_grid_any(
                self.enemy.spawn_point[0], self.enemy.spawn_point[1]))

        conv_x, conv_y = self.enemy.calculator.get_pixel_to_grid_entity(
            self.enemy
        )

        # Target reached
        if (conv_x, conv_y) == conv_spawn_point:
            self.enemy._wait_revive = True
            self.enemy.mode = EnemyState.WAIT

            if game_config.debug_mode:
                print_log(f"Changed state for {self.enemy} to WAIT")

            return

        open_walls = self._get_available_moves()
        if not open_walls:
            return

        if len(open_walls) == 1:
            self.enemy._next_direction = list(open_walls.keys()).pop()
            return

        best_distance: float = float('inf')
        direction: tuple[float, float] = (0.0, 0.0)
        TURN_PENALTY: float = 0.2

        for key, coords in open_walls.items():
            distance: float = (
                self.enemy.calculator.get_euclidean_distance(
                    coords, conv_spawn_point))

            # Apply momentum penalty if the path forces a turn
            if (key != self.enemy.current_direction and
                    self.enemy.current_direction != (0.0, 0.0)):
                distance += TURN_PENALTY

            if distance < best_distance:
                best_distance = distance
                direction = key

        self.enemy._next_direction = direction

    def _move(self) -> None:
        open_walls = self._get_available_moves()
        if not open_walls:
            return

        self.enemy._next_direction = self._apply_momentum_choice(open_walls)

    def _revive(self, delta_time: float) -> None:
        self.enemy._revive_timer += delta_time

        ratio = self.enemy._revive_timer / game_config.player_revive_time
        ratio = min(ratio, 1.0)
        self.enemy.sprite.alpha = int(255 * ratio)

        if self.enemy._revive_timer > game_config.player_revive_time:
            self.enemy.mode = EnemyState.WANDER
            self.enemy.sprite.color = (255, 255, 255)
            self.enemy._wait_revive = False
            self.enemy._died = False
            self.enemy._revive_timer = 0.0
            self.enemy.sprite.alpha = 255
            self.enemy.have_respawned = True

            if game_config.debug_mode:
                print_log(f"Changed state for {self.enemy} to WANDER")

    def _apply_momentum_choice(
        self, open_walls: dict[tuple[float, float], tuple[int, int]]
    ) -> tuple[float, float]:

        available_directions: list[tuple[float, float]] = (
            list(open_walls.keys())
        )
        current_dir: tuple[float, float] = self.enemy.current_direction

        # If current direction is an option and there are other choices
        if (current_dir in available_directions and
                len(available_directions) > 1):
            KEEP_DIRECTION_CHANCE: float = 0.80

            if random.random() < KEEP_DIRECTION_CHANCE:
                return current_dir
            else:
                # Force a turn by removing the straight path from options
                available_directions.remove(current_dir)

        return random.choice(available_directions)
