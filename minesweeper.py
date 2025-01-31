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
        self.is_flagged = False

    # Open a cell, and add the number of bombs around it
    def open(self, bombs_around):
        self.is_open = True
        self.bombs_around = str(bombs_around)
        return self.is_open

    def __repr__(self):
        # return the number of bombs around the cell
        if self.is_flagged and not self.is_open:
            return "F"
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

    def list_neigh(self, row_idx: int, col_idx: int) -> list:
        """
        Given a cell coordinate
        Return a list with all the neighbor indexes from this cell
        """
        # all possible neighbor positions
        neigh_positions = []
        pairs = list(product((-1, 0, 1), repeat=2)) # all combinations of of -1,0,1 in doubles (-1,-1), ....

        for pair in pairs:
            if pair[0] == 0 and pair[1] == 0:
                # this is us
                continue

            row = row_idx + pair[0]
            col = col_idx + pair[1]

            if row < 0 or col < 0:
                # we are out of range
                continue
            if row >= self.grid_coordinates.row or col >= self.grid_coordinates.col:
                # out of range
                continue

            neigh_positions.append((row, col))

        return neigh_positions

    def click(self, row_idx, col_idx):
        """
        Once we click a cell, it must be opened and checked to see if it is a bomb.
        If not, assign to its value, the number of bombs around you and return it
        """
        bombs_around = 0

        # Check if user clicked somewere out of bounds
        if (row_idx < 0 or row_idx >= self.grid_coordinates.row) or (col_idx < 0 or col_idx >= self.grid_coordinates.col):
            return "Out of Bound"

        # Hit bomb
        if self.grid[row_idx][col_idx].is_bomb:
            self.game = False
            return "BOOOM!"

        neighbors = self.list_neigh(row_idx, col_idx)

        # number of bombs around us
        for n in neighbors:
            if self.grid[n[0]][n[1]].is_bomb:
                bombs_around += 1

        # assign the bombs_around
        self.grid[row_idx][col_idx].open(bombs_around)

        # return to the user the updated grid
        return self.to_json_serializable_grid()

    def flag(self, row_idx, col_idx):
        self.grid[row_idx][col_idx].is_flagged = 'F'
        return self.to_json_serializable_grid()
    
    def show_grid(self):
        return json.dumps(self.grid, indent=4)

    def start(self):
        self.game = True
        self.build_grid()

    def check_win(self):
        """Parse through the list and check if we have a cell that is not opened and not bombs
        If there is any cell left unopen that is not a bomb, game is still on
        """
        
        for row_idx in range(self.grid_coordinates.row):
            for col_idx in range(self.grid_coordinates.col):
                cell = self.grid[row_idx][col_idx]
                if not cell.is_open and not cell.is_bomb:
                    return False
        return True

    def __repr__(self):
        return str(self.grid)
