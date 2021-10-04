import pickle
from tictactoe import ComputerPlayer, Environment
from itertools import product
import numpy as np


def get_all_possible_grids():
    possible_grids = dict()
    for raw in product([1, -1, 0], repeat=9):
        this_grid = np.array(raw, dtype=np.int32).reshape(3, 3)
        print(this_grid)
        this_hash = Environment.grid_to_hash(this_grid)
        possible_grids[this_hash] = this_grid
    return possible_grids


all_grids = get_all_possible_grids()

p1 = ComputerPlayer.from_file("p1.pkl")
for i, state in enumerate(p1.state_values):
    if state not in all_grids:
        print(i, state)

