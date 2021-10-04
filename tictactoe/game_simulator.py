from .player import Player, ComputerPlayer, HumanPlayer
from .environment import Environment


class GameSimulator:
    def __init__(self, p1: Player, p2: Player):
        self.env = Environment()
        self.p1 = p1
        self.p2 = p2
        self.players = [self.p1, self.p2]

    def run(self, print_grid=False):
        done = False
        while not done:
            print(self.env)
            for p in self.players:
                action = p.take_action(self.env)
                if print_grid:
                    print(p.name, action)
                resulting_grid, reward, done, debug_info = self.env.step(action, inplace=True)
                if print_grid:
                    print(self.env)
                if done:
                    if print_grid:
                        if self.env.winner:
                            print(f"{p.name} wins!")
                        else:
                            print(f"Draw!")
                    return self.env.winner
