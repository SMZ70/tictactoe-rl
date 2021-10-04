import numpy as np
from numpy.typing import ArrayLike
from typing import AnyStr

PLAYER_CHARS = {1: 'X', -1: 'O', 0: '-'}


class Environment():
    def __init__(self, size=3):
        self.grid = np.zeros((size, size), dtype=np.int32)

    @staticmethod
    def grid_to_hash(grid: ArrayLike):
        flat = grid.flatten()
        return ",".join(map(str, flat))

    def hash(self):
        return self.grid_to_hash(self.grid)

    @staticmethod
    def grid_possible_actions(grid: ArrayLike):
        n_rows, n_cols = grid.shape
        return [(i, j) for i in range(n_rows) for j in range(n_cols) if grid[i, j] == 0]

    @property
    def possible_actions(self):
        return self.grid_possible_actions(self.grid)

    @staticmethod
    def grid_to_str(grid):
        to_print = 25 * "-" + "\n"
        grid_body = "\n".join(["\t".join(map(lambda x: PLAYER_CHARS[x], row)) for row in grid])
        to_print += grid_body + "\n" + 25 * "-"
        return to_print

    @property
    def shape(self):
        return self.grid.shape

    @property
    def size(self):
        return self.shape[0]

    @staticmethod
    def get_winner(grid):
        n_rows, n_cols = grid.shape
        assert n_rows == n_cols

        if n_rows in grid.sum(axis=0):
            return 1
        if -n_rows in grid.sum(axis=0):
            return -1
        if n_rows in grid.sum(axis=1):
            return 1
        if -n_rows in grid.sum(axis=1):
            return -1
        if sum(grid.diagonal()) == n_rows:
            return 1
        if sum(grid.diagonal()) == -n_rows:
            return -1
        if sum(np.fliplr(grid).diagonal()) == n_rows:
            return 1
        if sum(np.fliplr(grid).diagonal()) == -n_rows:
            return -1

    @staticmethod
    def get_possible_actions(grid):
        size = grid.shape[0]
        possible_actions = [(i, j) for i in range(size) for j in range(size) if grid[i, j] == 0]
        return possible_actions

    @classmethod
    def is_grid_terminal(cls, grid: ArrayLike):
        if not cls.get_possible_actions(grid) or cls.get_winner(grid=grid):
            return True
        return False

    @property
    def is_terminal(self):
        return self.is_grid_terminal(self.grid)

    @property
    def winner(self):
        return self.get_winner(self.grid)

    @classmethod
    def get_grid_turn(cls, grid):
        if cls.is_grid_terminal(grid):
            return None
        n_plays = {key: 0 for key in [-1, 0, 1]}
        uniques, counts = np.unique(grid, return_counts=True)
        uniques = list(map(int, uniques))
        for i, u in enumerate(uniques):
            n_plays[u] = counts[i]
        if n_plays[-1] < n_plays[1]:
            return -1
        else:
            return 1

    @classmethod
    def calculate_step(cls, grid, pos):
        turn = cls.get_grid_turn(grid)
        resulting_grid = grid.copy()
        if resulting_grid[pos] == 0:
            resulting_grid[pos] = turn
        winner = cls.get_winner(resulting_grid)
        reward = {1: 0, -1: 0}
        if winner:
            reward[winner] = 1
        elif cls.is_grid_terminal(resulting_grid):
            reward[1] = 0.5
            reward[-1] = 0.5
        return resulting_grid, reward, cls.is_grid_terminal(resulting_grid), None

    def step(self, pos, inplace=True):
        resulting_grid, reward, is_terminal, debug_info = self.calculate_step(self.grid, pos)

        if inplace:
            self.grid = resulting_grid

        return resulting_grid, reward, is_terminal, debug_info

    def reset(self):
        self.__init__()
        return self.grid

    def __str__(self):
        return self.grid_to_str(self.grid)


if __name__ == "__main__":
    env = Environment()
    print(env)
    print(env.is_terminal)
