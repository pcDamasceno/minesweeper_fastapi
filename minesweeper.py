import random
import json
from itertools import product
from typing import NamedTuple


class GridSize(NamedTuple):
    row: int
    col: int


class Cell:
    def __init__(self, is_bomb=False, is_open=False):
        self.is_bomb = is_bomb
        self.is_open = is_open
        self.bombs_around = False

    # Open a cell, and add the number of bombs around it
    def open(self, bombs_around):
        self.is_open = True
        self.bombs_around = str(bombs_around)
        return self.is_open

    def __repr__(self):
        return str(self.bombs_around) if self.is_open else "X"



class Minesweeper:
    def __init__(self, row=10, col=10):
        # Updated grid dimensions to a named tuple
        self.grid_coordinates = GridSize(row, col)

        self.n_of_bombs = 0
        self.bombs_positions = set()
        
        # create the grid with 'blank' cells
        self.grid = [[Cell() for c in range(col)] for r in range(row)]
        # game status
        self.game = True

    def to_json_serializable_grid(self):
        return [[str(cell) for cell in row] for row in self.grid]

    # random generation for number of bombs
    def _gen_num_bombs(self):
        # Limit the amount of bombs to half of the grid
        self.n_of_bombs = random.randint(1, (self.grid_coordinates.row * self.grid_coordinates.col) // 2)
        return self.n_of_bombs

    def _gen_pos_bombs(self):
        """
        Gen 2 random numbers to be used as coordinates to the bombs location
        """
        while len(self.bombs_positions) < self.n_of_bombs:
            rand_row = random.randrange(0, self.grid_coordinates.row)
            rand_col = random.randrange(0, self.grid_coordinates.col)
            self.bombs_positions.add((rand_row, rand_col))
            # Assign as bomb
            self.grid[rand_row][rand_col].is_bomb = True

    # Gen random number of bombs and assign the cells
    def build_grid(self):
        self._gen_num_bombs()
        self._gen_pos_bombs()

    def list_neigh(self, x: int, y: int) -> list:
        # all possible neighbor positions
        neigh_positions = []
        pairs = list(product((-1, 0, 1), repeat=2))

        for pair in pairs:
            if pair[0] == 0 and pair[1] == 0:
                # this is us
                continue

            row = x + pair[0]
            col = y + pair[1]

            if row < 0 or col < 0:
                # we are out of range
                continue

            if row >= self.grid_coordinates.col or col >= self.grid_coordinates.row:
                continue

            neigh_positions.append((row, col))

        return neigh_positions

    def click(self, x, y):
        bombs_around = 0

        # Check if user clicked somewere impossible
        if (x < 0 or x >= self.grid_coordinates.row) or (y < 0 or y >= self.grid_coordinates.col):
            return "Out of Bound"

        if self.grid[x][y].is_bomb:
            self.game = False
            return "BOOOM!"

        neighbors = self.list_neigh(x, y)
        # number of bombs around us
        for n in neighbors:
            if self.grid[n[0]][n[1]].is_bomb:
                bombs_around += 1

        # save that
        self.grid[x][y].open(bombs_around)

        return self.to_json_serializable_grid()

    def show_grid(self):
        return json.dumps(self.grid, indent=4)

    def start(self):
        self.game = True
        self.build_grid()

    def check_win(self):
        # Look for a cell that is not opened and is not bomb
        for r in range(self.grid_coordinates[0]):
            for c in range(self.grid_coordinates[1]):
                if not (self.grid[r][c].is_open) and not (self.grid[r][c].is_bomb):
                    return False
        return True

    def __repr__(self):
        return str(self.grid)
