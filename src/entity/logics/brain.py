# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  brain.py                                          :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/29 14:10:28 by roandrie        #+#    #+#               #
#  Updated: 2026/06/10 11:56:30 by anacharp        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any

import random
import math
import heapq

from .StateMachine import EnemyState
from src import game_config
from src.utils import print_log

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.entity.entity import Enemy


class EnemyBrain():
    def __init__(self, enemy_ref: "Enemy") -> None:
        self.enemy: Enemy = enemy_ref

        # - Private attributes -
        self._current_path: list[tuple[int, int]] = []
        self._old_target: tuple[float, float] = (0, 0)

    def update(self, delta_time: float) -> None:
        if self.enemy.mode not in [
            EnemyState.WAIT, EnemyState.CHASE, EnemyState.ANGRY
        ]:
            self._raycasting()

        self._state_machine(delta_time)

    def force_move(self) -> None:
        conv_x, conv_y = (
            self.enemy.calculator.get_pixel_to_grid_entity(self.enemy)
        )

        open_walls: dict[tuple[float, float], tuple[int, int]] = (
            self.enemy.calculator.check_open_wall(
                int(conv_x), int(conv_y), self.enemy.maze_bitmap))

        valid_coords: list[tuple[int, int]] = []
        for coords in open_walls:
            valid_coords.append(coords)

        force_direction = random.choice(valid_coords)
        self.enemy.current_direction = force_direction

    # :---------------:
    #  PRIVATE METHODS
    # :---------------:

    def _state_machine(self, delta_time: float) -> None:
        if self.enemy.mode == EnemyState.WAIT:
            if self.enemy._wait_revive:
                self._revive(delta_time)

        elif self.enemy.mode == EnemyState.WANDER:
            self.enemy.speed = self.enemy.base_speed
            self._move()

        elif self.enemy.mode == EnemyState.SEARCH:
            self.enemy.speed = (
                self.enemy.base_speed + 1
            )
            self._go_to_position(self.enemy.player_ref.x,
                                 self.enemy.player_ref.y)

        elif self.enemy.mode == EnemyState.CHASE:
            self.enemy.speed = (
                self.enemy.base_speed + game_config.enemy_chase_speed
            )
            self._chase_player(delta_time)

        elif self.enemy.mode == EnemyState.ANGRY:
            self.enemy.speed = (
                self.enemy.base_speed + game_config.enemy_angry_speed
            )
            self._go_to_position(self.enemy.player_ref.x,
                                 self.enemy.player_ref.y)

        elif self.enemy.mode == EnemyState.RUNAWAY:
            self.enemy.speed = (
                self.enemy.base_speed - game_config.ennemy_speed_reduction
            )
            self._runaway_from_player()

        elif self.enemy.mode == EnemyState.RESPAWN:
            self.enemy.speed = (
                self.enemy.base_speed + game_config.enemy_speed_respawn
            )
            self._return_to_spawnpoint()

            self.enemy._timer_check_respawn -= delta_time

            if self.enemy._timer_check_respawn < 0.0:
                self.enemy.respawn()
                self.enemy._timer_check_respawn = (
                    game_config.enemy_check_res_timer
                )

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
        open_walls: dict[tuple[float, float], tuple[int, int]] = (
            self.enemy.calculator.check_open_wall(
                int(conv_x), int(conv_y), self.enemy.maze_bitmap))

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

        for i in range(1, game_config.raycasting_max_distance + 1):
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
                    self.enemy.mode = EnemyState.WANDER
                    self.enemy._timer_chase = 0.0

                    if game_config.debug_mode:
                        print_log(f"Changed state for {self.enemy} to WANDER")

        # Chase the player
        self._go_to_position(self.enemy.player_ref.x, self.enemy.player_ref.y)

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

    def _go_to_position(self, pos_x: float, pos_y: float) -> None:
        open_walls = self._get_available_moves()
        if not open_walls:
            return

        # Pop single available move immediately to skip loop
        if len(open_walls) == 1:
            self.enemy._next_direction = list(open_walls.keys()).pop()
            return

        conv_pos: tuple[float, float] = (
            self.enemy.calculator.get_pixel_to_grid_any(pos_x, pos_y)
        )

        best_distance: float = float('inf')
        direction: tuple[float, float] = (0.0, 0.0)
        TURN_PENALTY: float = 0.2

        random_percent: float = 0.6
        if self.enemy.mode == EnemyState.CHASE:
            random_percent == 0.4
        if random.random() < random_percent and self.enemy.enemy_type == "dog":
            direction = random.choice(list(open_walls.keys()))
        else:
            for key, coords in open_walls.items():
                distance: float = self.enemy.calculator.get_euclidean_distance(
                    coords, conv_pos
                )

                # Apply momentum penalty if the path forces a turn
                if (key != self.enemy.current_direction and
                        self.enemy.current_direction != (0.0, 0.0)):
                    distance += TURN_PENALTY

                if distance < best_distance:
                    best_distance = distance
                    direction = key

        self.enemy._next_direction = direction

    def _go_to_position_better(self, target: tuple[int, int]) -> None:
        self_coords = (
                int(self.enemy.calculator.get_pixel_to_grid_entity(self.enemy))
            )

        # Check if targer have moved
        if self._old_target != target:
            self._old_target = target

            self._current_path: list[tuple[int, int]] = a_star_algo(
                self.enemy.maze_bitmap, self_coords, target
            )

            # Pop the start position
            if self._current_path:
                self._current_path.pop(0)

        # Move
        if self._current_path:
            if self_coords == self._current_path[0]:
                self._current_path.pop(0)

            if self._current_path:
                dx = self._current_path[0][0] - self_coords[0]
                dy = self._current_path[0][1] - self_coords[1]

                self.enemy._next_direction = (dx, dy)

# :------------:
#  A* algorithm
# :------------:


def a_star_algo(
        grid: dict[tuple[int, int], int], start_pos: tuple[int, int],
        goal_pos: tuple[int, int]
        ) -> list[tuple[int, int]]:

    # Initialize start node
    start: dict[str, Any] = create_node(
        start_pos, 0, calculate_heuristic(start_pos, goal_pos)
    )

    # Initialize open and closed sets
    open_list = [(start['sum'], start_pos)]  # Priority queue
    open_dict = {start_pos: start}           # For quick node lookup
    closed_set = set()                       # Explored nodes

    while open_list:
        # Find the lowest pos value
        _, current_pos = heapq.heappop(open_list)
        current_node = open_dict[current_pos]

        # Check if we've reached the goal
        if current_pos == goal_pos:
            return reconstruct_path(current_node)

        closed_set.add(current_pos)

        # Explore neighbors
        for neighbor_pos in get_valid_neighbors(grid, current_pos):
            # Skip if already explored
            if neighbor_pos in closed_set:
                continue

            # Calculate new path cost
            tentative_cost = (
                current_node['cost'] + calculate_heuristic(
                    current_pos, neighbor_pos)
            )

            # Create or update neighbor
            if neighbor_pos not in open_dict:
                neighbor = create_node(
                    neighbor_pos, tentative_cost,
                    calculate_heuristic(neighbor_pos, goal_pos),
                    current_node
                )
                heapq.heappush(open_list, (neighbor['sum'], neighbor_pos))
                open_dict[neighbor_pos] = neighbor

            elif tentative_cost < open_dict[neighbor_pos]['cost']:
                # Found a better path to the neighbor
                neighbor = open_dict[neighbor_pos]
                neighbor['cost'] = tentative_cost
                neighbor['sum'] = tentative_cost + neighbor['estim_cost']
                neighbor['parent'] = current_node
                heapq.heappush(open_list, (neighbor['sum'], neighbor_pos))

    return []

# :-----------------------------:
#  HELPERS FUNCTIONS FOR A* ALGO
# :-----------------------------:


def create_node(
        position: tuple[int, int], cost: float = float('inf'),
        estimate_cost: float = 0.0, parent: dict = None) -> dict[str, Any]:

    return {
        'position': position,
        'cost': cost,
        'estim_cost': estimate_cost,
        'sum': cost + estimate_cost,
        'parent': parent
    }


def calculate_heuristic(pos1: tuple[int, int], pos2: tuple[int, int]) -> float:
    x1, y1 = pos1
    x2, y2 = pos2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def get_valid_neighbors(
        grid: dict[tuple[int, int], int], position: tuple[int, int]
        ) -> list[tuple[int, int]]:
    valid_list: list[tuple[int, int]] = []

    x, y = position

    possible_moves: list[tuple[int, int]] = [
        (x+1, y), (x-1, y), (x, y+1), (x, y-1)
    ]

    for nx, ny in possible_moves:
        if grid.get((nx, ny), 1) == 0:
            valid_list.append((nx, ny))

    return valid_list


def reconstruct_path(goal: dict[str, Any]) -> list[tuple[int, int]]:
    path = []
    current = goal

    while current is not None:
        path.append(current['position'])
        current = current['parent']

    return path[::-1]
