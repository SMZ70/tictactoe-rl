from .environment import Environment
from .player import Player, ComputerPlayer
import numpy as np


class Trainer:
    def __init__(self, player1=None, player2=None):
        self.env = Environment()
        if player1 is None:
            self.p1 = ComputerPlayer("p1")
        if player2 is None:
            self.p2 = ComputerPlayer("p2")
        self.players = [self.p1, self.p2]
        self.game_stats = {1: 0, -1: 0, 0: 0}

    def train(self, n_games=100, print_each_grid=False, print_winner=False, report_freq=1000):
        self.p1.eps_decrease = 2 / n_games
        self.p2.eps_decrease = 2 / n_games
        for game in range(n_games):
            if game % report_freq == 0 and game > 0:
                stat_percents = {key: round((val/game)*100, 2) for key, val in self.game_stats.items()}
                print(f"Game {game:7.0f}/{n_games}\t{self.p1.eps:1.5f}\t{self.p2.eps:1.5f}\tStats: {stat_percents}")
            self.env.reset()
            done = False
            while not done:
                for p in self.players:
                    action = p.take_action(self.env)
                    resulting_grid, reward, done, debug_info = self.env.step(action, inplace=True)
                    if print_each_grid:
                        print(self.env)
                    if done:
                        if self.env.winner == 1:
                            self.p1.feed_reward(1, self.env)
                            self.p2.feed_reward(0, self.env)
                            self.game_stats[1] += 1
                        elif self.env.winner == -1:
                            self.p1.feed_reward(0, self.env)
                            self.p2.feed_reward(1, self.env)
                            self.game_stats[-1] += 1
                        else:
                            self.p1.feed_reward(0.5, self.env)
                            self.p2.feed_reward(0.5, self.env)
                            self.game_stats[0] += 1
                        if print_winner:
                            print(f"The winner is: {self.env.winner}", self.game_stats)
                        self.p1.reset()
                        self.p2.reset()
                        break
            self.p1.pickle_strategy()
            self.p2.pickle_strategy()
