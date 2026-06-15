# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  brain.py                                          :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/29 14:10:28 by roandrie        #+#    #+#               #
#  Updated: 2026/06/15 08:48:36 by roandrie        ###   ########.fr        #
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
    """Base brain class managing enemy AI state machine, navigation, and
    raycasting.

    Handles common behaviors such as wandering, chasing, returning to spawn,
    and fallback anti-stuck mechanics
    """
    def __init__(self, enemy_ref: "Enemy") -> None:
        """Initialize the enemy brain.

        Args:
            enemy_ref (Enemy): Reference to the enemy entity controlling this
            brain.
        """
        self.enemy: Enemy = enemy_ref

        # - Private attributes -
        self._current_path: list[tuple[int, int]] = []
        self._old_target: tuple[float, float] = (0, 0)

    def update(self, delta_time: float) -> None:
        """Update the AI state machine logic and vision sensing.

        Args:
            delta_time (float): Time elapsed since the last frame update.
        """
        if self.enemy.mode not in [
            EnemyState.WAIT, EnemyState.CHASE, EnemyState.ANGRY
        ]:
            self._raycasting()

        self._state_machine(delta_time)

    def force_move(self) -> None:
        """Force the enemy to immediately pick a random valid direction."""
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
        """Execute movement logic corresponding to the current state mode.

        Args:
            delta_time (float): Time elapsed since the last frame update.
        """
        if self.enemy.mode == EnemyState.WAIT:
            if self.enemy._wait_revive:
                self._revive(delta_time)

        elif self.enemy.mode == EnemyState.WANDER:
            self.enemy.speed = self.enemy.base_speed
            self._move()

        elif self.enemy.mode == EnemyState.SEARCH:
            self.enemy.speed = self.enemy.base_speed + 1
            self._execute_search_state()

        elif self.enemy.mode == EnemyState.CHASE:
            self.enemy.speed = (
                self.enemy.player_ref.base_speed + 1.2
            )
            self._chase_player(delta_time)

        elif self.enemy.mode == EnemyState.ANGRY:
            self.enemy.speed = (
                self.enemy.player_ref.base_speed + 1
            )
            self._go_to_position(self.enemy.player_ref.x,
                                 self.enemy.player_ref.y)

        elif self.enemy.mode == EnemyState.RUNAWAY:
            self.enemy.speed = (
                self.enemy.base_speed - 40
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

    def _execute_search_state(self) -> None:
        self._go_to_position(self.enemy.player_ref.x, self.enemy.player_ref.y)

    def _get_available_moves(
        self
    ) -> dict[tuple[float, float], tuple[int, int]]:
        """Filter and retrieve unblocked neighboring tiles.

        Prevents 180-degree turns unless trapped in a dead end, and triggers
        anti-stuck fallbacks.

        Returns:
            dict[tuple[float, float], tuple[int, int]]: Maps valid direction
            vectors
                to their corresponding grid target coordinates.
        """

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
        """Cast a straight sensory ray along the moving direction to detect
        the player.

        Returns:
            bool: True if the player is in direct line of sight without wall
            obstructions.
        """
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
        """Pursue the player actively and handle state forgetting when losing
        line of sight.

        Args:
            delta_time (float): Time elapsed since the last frame update.
        """
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
        """Select a safe direction to flee from the player."""
        open_walls = self._get_available_moves()
        if not open_walls:
            return

        self.enemy._next_direction = self._apply_momentum_choice(open_walls)

    def _return_to_spawnpoint(self) -> None:
        """Route the defeated entity back to its starting spawn point."""
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
        """Calculate and submit the next direction during wandering."""
        open_walls = self._get_available_moves()
        if not open_walls:
            return

        self.enemy._next_direction = self._apply_momentum_choice(open_walls)

    def _revive(self, delta_time: float) -> None:
        """Handle alpha restoration and reset states during revival countdown.

        Args:
            delta_time (float): Time elapsed since the last frame update.
        """
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
        """Apply a probability modifier to keep going straight instead of
        turning.

        Args:
            open_walls (dict[tuple[float, float], tuple[int, int]]): Available
            directions.

        Returns:
            tuple[float, float]: Chosen direction vector.
        """

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
        """Route towards a raw pixel coordinate using distance heuristics per
        tile.

        Args:
            pos_x (float): Target X pixel coordinate.
            pos_y (float): Target Y pixel coordinate.
        """
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
        """Call the A* algorithm to calculate the pathfinding of the target.

        Check if the current path have been modified. If so, call the algorithm
        to calculate a new path. Then, apply the current path to the enemy. If
        path can't be accessed, take a random position.
        If debug mode is active, save the path positions to draw it after.

        Args:
            target (tuple[int, int]): the position of the targetted place.
        """
        open_walls = self._get_available_moves()
        if not open_walls:
            return

        self_coords_raw = (
                self.enemy.calculator.get_pixel_to_grid_entity(self.enemy)
            )
        self_coords_x, self_coords_y = self_coords_raw
        self_coords: tuple[int, int] = int(self_coords_x), int(self_coords_y)

        # First step if path exist
        if self._current_path and self_coords == self._current_path[0]:
            self._current_path.pop(0)
            if hasattr(self.enemy, '_debug_pathfinding'):
                self.enemy._debug_pathfinding.pop(0)

        # Stop if destation is reached
        if self_coords == target:
            return

        # Check if we need to recalculate the path
        needs_recalc = False

        # Check if target have moved or path is empty
        if self._old_target != target or not self._current_path:
            needs_recalc = True
        elif self._current_path:
            if self._current_path[0] not in open_walls.values():
                needs_recalc = True

        # Recalculate the path
        if needs_recalc:
            self._old_target = target

            self._current_path: list[tuple[int, int]] = a_star_algo(
                self.enemy.maze_bitmap, self_coords, target,
                self.enemy.current_direction
            )

            # - DEBUG ONLY -
            if hasattr(self.enemy, '_debug_pathfinding'):
                self.enemy._debug_pathfinding.clear()
                self._debug_store_pathfinding()

            # Pop the start position
            if self._current_path:
                self._current_path.pop(0)

        # Find the next direction
        if self._current_path:
            for dir, available_move in open_walls.items():
                if available_move == self._current_path[0]:
                    self.enemy._next_direction = dir
                    return

        # Fallback, take a random path and clear the old pathfinding
        self._current_path.clear()
        if hasattr(self.enemy, '_debug_pathfinding'):
            self.enemy._debug_pathfinding.clear()
        self.enemy._next_direction = self._apply_momentum_choice(open_walls)

    def _debug_store_pathfinding(self) -> None:
        """
        Store the pathfinding path used only in debug mode.
        """
        for coords in self._current_path:
            # Normalize the coords
            raw_x, raw_y = coords
            normal_x: float = (raw_x - 1) / 2.0
            normal_y: float = (raw_y - 1) / 2.0

            x, y = self.enemy.calculator.get_grid_to_pixel(
                normal_x, normal_y)
            self.enemy._debug_pathfinding.append((x, y))

# :------------:
#  A* algorithm
# :------------:


def a_star_algo(
        grid: dict[tuple[int, int], int], start_pos: tuple[int, int],
        goal_pos: tuple[int, int], current_dir: tuple[float, float]
        ) -> list[tuple[int, int]]:
    """Execute the A* pathfinding algorithm over the maze grid layout.

    Args:
        grid (dict[tuple[int, int], int]): The maze bitmap dictionary.
        start_pos (tuple[int, int]): Initial grid coordinates.
        goal_pos (tuple[int, int]): Destination grid coordinates.

    Returns:
        list[tuple[int, int]]: Chronological sequence of nodes from start to
        goal.
    """

    # Initialize start node
    start: dict[str, Any] = create_node(
        start_pos, 0, calculate_heuristic(start_pos, goal_pos)
    )

    # Initialize open and closed sets
    open_list = [(start['sum'], start_pos)]  # Priority queue
    open_dict = {start_pos: start}           # For quick node lookup
    closed_set = set()                       # Explored nodes

    forbidden_pos: tuple[int, int] = None
    while open_list:
        # Find the lowest pos value
        _, current_pos = heapq.heappop(open_list)
        current_node = open_dict[current_pos]

        # Check if we've reached the goal
        if current_pos == goal_pos:
            return reconstruct_path(current_node)

        closed_set.add(current_pos)

        # Avoid turn back
        if current_pos == start_pos:
            inverted_dir_x = current_pos[0] - int(current_dir[0])
            inverted_dir_y = current_pos[1] - int(current_dir[1])
            forbidden_pos = (inverted_dir_x, inverted_dir_y)

        # Explore neighbors
        for neighbor_pos in get_valid_neighbors(grid, current_pos):
            # Skip if already explored
            if neighbor_pos in closed_set:
                continue
            # Skip if it's forbidden
            if neighbor_pos == forbidden_pos:
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
        estimate_cost: float = 0.0,
        parent: dict[str, Any] | None = None) -> dict[str, Any]:
    """Helper formatting dictionary structures representing nodes in A*.

    Args:
        position (tuple[int, int]): Spatial coordinates.
        cost (float): $g(n)$ cost accumulated to reach this node. Defaults to
        infinity.
        estimate_cost (float): $h(n)$ heuristic cost to destination. Defaults
        to 0.0.
        parent (dict[str, Any] | None): Node leading directly to this one.
        Defaults to None.

    Returns:
        dict[str, Any]: Generated node model.
    """

    return {
        'position': position,
        'cost': cost,
        'estim_cost': estimate_cost,
        'sum': cost + estimate_cost,
        'parent': parent
    }


def calculate_heuristic(pos1: tuple[int, int], pos2: tuple[int, int]) -> float:
    """Calculate Euclidean distance metric serving as the A* heuristic.

    Args:
        pos1 (tuple[int, int]): Point A coordinates.
        pos2 (tuple[int, int]): Point B coordinates.

    Returns:
        float: Calculated distance.
    """
    x1, y1 = pos1
    x2, y2 = pos2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def get_valid_neighbors(
        grid: dict[tuple[int, int], int], position: tuple[int, int]
        ) -> list[tuple[int, int]]:
    """Scan cardinally adjacent spaces to find passable tiles.

    Args:
        grid (dict[tuple[int, int], int]): The maze bitmap structure.
        position (tuple[int, int]): Evaluated tile grid origin.

    Returns:
        list[tuple[int, int]]: Collection of valid adjacent tile paths.
    """
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
    """Unroll tracking relationships from a goal node backwards to create a
    path.

    Args:
        goal (dict[str, Any]): Solved target node containing parent lineage.

    Returns:
        list[tuple[int, int]]: Sequential tracking path from start to target.
    """
    path = []
    current = goal

    while current is not None:
        path.append(current['position'])
        current = current['parent']

    return path[::-1]
