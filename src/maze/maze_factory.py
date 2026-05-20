# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  maze_factory.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: anacharp, roandrie                        +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/05/15 14:30:14 by roandrie        #+#    #+#               #
#  Updated: 2026/05/20 10:58:44 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.maze.load_mazegenerator import load_mazegenerator


WALL_SPRITES: dict[int, tuple[str, float]] = {
    "wall":  ("maze_wall", 0),
    "wall_90":  ("maze_wall", 90),
    "wall_180":  ("maze_wall", 180),
    "wall_270":  ("maze_wall", -90),

    "corner":  ("maze_wall_corner", 0),
    "corner_90":  ("maze_wall_corner", 90),
    "corner_180": ("maze_wall_corner", 180),
    "corner_270":  ("maze_wall_corner", -90),

    "triple_wall": ("maze_triple_wall", 0),
    "triple_wall_90":  ("maze_triple_wall", 90),
    "triple_wall_180": ("maze_triple_wall", 180),
    "triple_wall_270": ("maze_triple_wall", -90),

    "inside_wall": ("maze_inside_wall", 0),
    "inside_wall_90":  ("maze_inside_wall", 90),
    "inside_wall_180": ("maze_inside_wall", 180),
    "inside_wall_270": ("maze_inside_wall", -90),

    "four_wall": ("maze_four_wall", 0),
}

N = [1, 3, 5, 7, 9, 11, 13, 15]
S = [4, 5, 6, 7, 12, 13, 14, 15]
E = [2, 3, 6, 7, 10, 11, 14, 15]
W = [8, 9, 10, 11, 12, 13, 14, 15]


class MazeFactory:
    def __init__(self) -> None:
        self._maze_class = load_mazegenerator()

    def generate_maze(
        self, width: int, height: int, textures: dict,
        screen_width: int, screen_height: int
    ) -> list[list[int]]:
        self.height = height

        self.tile_size = min(
            screen_width // width,
            screen_height // self.height
        ) - 5

        maze_generator = self._maze_class((width, self.height))
        self.grid_data = maze_generator._maze

        wall_data: list[tuple[str, float, float, float]] = []
        self.offset_x = (screen_width - width * self.tile_size) // 2
        self.offset_y = (screen_height - self.height * self.tile_size) // 2
        self.wall_sprites_list: list[str] = []

        for row_index, row in enumerate(self.grid_data):
            for col_index, cell_value in enumerate(row):

                x, y = self.get_pixel_coordinates(col_index, row_index)

                n = cell_value in N
                s = cell_value in S
                e = cell_value in E
                w = cell_value in W

                keys = []

                if not n and not e:
                    keys.append("inside_wall_180")
                if not w and not n:
                    keys.append("inside_wall_90")
                if not s and not w:
                    keys.append("inside_wall")
                if not e and not s:
                    keys.append("inside_wall_270")
                if n and e:
                    keys.append("corner")
                if s and e:
                    keys.append("corner_90")
                if n and w:
                    keys.append("corner_270")
                if s and w:
                    keys.append("corner_180")
                if n and not e and not w:
                    keys.append("wall")
                if n and e and w:
                    keys.append("triple_wall")
                if w and n and s:
                    keys.append("triple_wall_270")
                if s and e and w:
                    keys.append("triple_wall_180")
                if e and n and s:
                    keys.append("triple_wall_90")
                if s and not e and not w:
                    keys.append("wall_180")
                if w and not n and not s:
                    keys.append("wall_270")
                if e and not n and not s:
                    keys.append("wall_90")
                if n and s and e and w:
                    keys.append("four_wall")

                for key in keys:
                    sprite_name, angle = WALL_SPRITES[key]

                    sprite_path = str(textures[sprite_name])
                    self.wall_sprites_list.append(str(textures[sprite_name]))

                    wall_data.append((sprite_path, angle, x, y, self.tile_size))

        return wall_data


    def get_pixel_coordinates(self, col: int, row: int) -> tuple[int, int]:

        x = col * self.tile_size + self.tile_size / 2 + self.offset_x
        y = (self.height - 1 - row) * self.tile_size + self.tile_size / 2 + self.offset_y

        return (x, y)


def generate_bytes_maze(
    grid: list[list[int]], width: int, height: int
) -> dict[tuple[int, int], str]:
    # Calculation of grid dimensions
    rows: int = 2 * height + 1
    cols: int = 2 * width + 1

    # Initialization: fill all walls with byte '1'
    byte_grid: list[list[int]] = [[1] * cols for _ in range(rows)]

    # Init dictionnary containing walls bytes
    close_or_open: dict[tuple[int, int], str] = {}

    for row_index, row in enumerate(grid):
        for col_index, cell_value in enumerate(row):
            # Bytes verifications: global define
            n: bool = cell_value in N
            s: bool = cell_value in S
            e: bool = cell_value in E
            w: bool = cell_value in W

            # Coordinates of the center of the cell in the new grid
            ay: int = row_index * 2 + 1
            ax: int = col_index * 2 + 1

            # Center will be byte '0' (open)
            byte_grid[ay][ax] = 0

            # Create the corridors if walls do not exist
            if not n and row_index > 0:
                byte_grid[ay - 1][ax] = 0
            if not s and row_index < height - 1:
                byte_grid[ay + 1][ax] = 0
            if not e and col_index < width - 1:
                byte_grid[ay][ax + 1] = 0
            if not w and col_index > 0:
                byte_grid[ay][ax - 1] = 0

    # Convert in dictionnary of strings
    for r_idx, r_content in enumerate(byte_grid):
        for c_idx, val in enumerate(r_content):
            # '0' open / '1' = close
            close_or_open[(r_idx, c_idx)] = val

    # Block open cells inside the 42
    bytes_maze: dict[tuple[int, int], str] = close_or_open.copy()

    for coords, byte in close_or_open.items():
        row, col = coords
        new_byte: int = 1

        # Check if the cell is open
        if byte == 0:
            # Check if inside the 42
            if (close_or_open[(row - 1, col)] == 1 and
                    close_or_open[(row + 1, col)] == 1 and
                    close_or_open[(row, col - 1)] == 1 and
                    close_or_open[(row, col + 1)] == 1
                ):

                # Replace the byte
                bytes_maze[(row, col)] = new_byte

    return bytes_maze
