# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  math_logics.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/25 17:22:26 by roandrie        #+#    #+#               #
#  Updated: 2026/05/25 18:20:55 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from math import sqrt


def euclidean_distance(point1: float, point2: float) -> float:
    distance: float = 0.0

    for i in range(len(point1)):
        distance += (point2[i] - point1[i]) ** 2
    return sqrt(distance)


def check_open_wall(
    x: int, y: int, maze_bitemap: dict[tuple[int, int], str],
) -> list[tuple[int, int]]:
    open_wall: list[tuple[int, int]] = []

    if maze_bitemap[(x + 1, y)] == 0:
        open_wall.append((x + 1, y))

    if maze_bitemap[(x - 1, y)] == 0:
        open_wall.append((x - 1, y))

    if maze_bitemap[(x, y + 1)] == 0:
        open_wall.append((x, y + 1))

    if maze_bitemap[(x, y - 1)] == 0:
        open_wall.append((x, y - 1))

    return open_wall
