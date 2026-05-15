# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  maze_factory.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/15 14:30:14 by roandrie        #+#    #+#               #
#  Updated: 2026/05/15 14:52:14 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.maze.load_mazegenerator import load_mazegenerator


class MazeFactory:
    def __init__(self) -> None:

        self._maze_class = load_mazegenerator()
        self.generate_maze(10, 10, "c")

    def generate_maze(self, width: int, height: int) -> list[list[int]]:

        test = self._maze_class()
        print(test._maze)
