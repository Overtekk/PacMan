# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  print_maze_bytes.py                               :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/19 16:31:56 by roandrie        #+#    #+#               #
#  Updated: 2026/05/19 16:53:12 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.maze import MazeFactory, generate_bytes_maze
from src.renderer import ScreenSettings, SpritesLoader

if __name__ == "__main__":

    maze_width = 20
    maze_height = 10

    maze = MazeFactory()
    sprite = SpritesLoader()
    maze.generate_maze(maze_width, maze_height, sprite.textures,
                       ScreenSettings.WIDTH,ScreenSettings.HEIGHT)

    byte_maze = generate_bytes_maze(maze.grid_data, maze_width, maze_height)

    total_rows: int = (maze_height * 2) + 1
    total_cols: int = (maze_width * 2) + 1

    # Get the logical maze center
    col_center: int = maze_width // 2
    row_center: int = maze_height // 2

    if byte_maze[(row_center * 2 + 1, col_center * 2 + 1)] == 0:
        player_x, player_y = maze.get_pixel_coordinates(
            col_center, row_center
        )

    player_grid_y: int = row_center * 2 + 1
    player_grid_x: int = col_center * 2 + 1

    # Print the maze in the terminal
    for y in range(total_rows):
        for x in range(total_cols):
            if y == player_grid_y and x == player_grid_x:
                print("X", end="")
            else:
                print(byte_maze[(y, x)], end="")

        # Jump to the next row
        print()
