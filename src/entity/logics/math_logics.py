# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  math_logics.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/25 17:22:26 by roandrie        #+#    #+#               #
#  Updated: 2026/05/25 19:28:37 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from math import sqrt


def euclidean_distance(
    point1: tuple[float, float], point2: tuple[float, float]
) -> float:
    distance: float = 0.0

    for i in range(len(point1)):
        distance += (point2[i] - point1[i]) ** 2
    return sqrt(distance)


def check_open_wall(
    x: int, y: int, maze_bitemap: dict[tuple[int, int], str],
) -> dict[tuple[int, int], tuple[int, int]]:
    open_wall: dict[tuple[int, int], tuple[int, int]] = {}

    # West
    if maze_bitemap[(x + 1, y)] == 0:
        open_wall[(1, 0)] = (x + 1, y)

    # East
    if maze_bitemap[(x - 1, y)] == 0:
        open_wall[(-1, 0)] = (x - 1, y)

    # South
    if maze_bitemap[(x, y + 1)] == 0:
        open_wall[(0, -1)] = (x, y + 1)

    # North
    if maze_bitemap[(x, y - 1)] == 0:
        open_wall[(0, 1)] = (x, y - 1)

    return open_wall
