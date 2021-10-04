import numpy as np
from .environment import Environment
import pickle


class Player:
    def __init__(self, player_name):
        self.name = player_name
        pass

    def feed_reward(self, reward, env):
        pass

    def best_action(self, grid):
        pass

    def reset(self):
        pass

    def pickle_strategy(self):
        pass

    def take_action(self, env: Environment):
        pass

    @staticmethod
    def random_action(env: Environment):
        action_ix = np.random.choice(range(len(env.possible_actions)))
        action = env.possible_actions[action_ix]
        return action

    @classmethod
    def from_file(cls, file_name, player_name=None):
        if player_name is None:
            player_name = file_name.split(".pkl")[0]
        player = cls(player_name=player_name)
        with open(file_name, "rb") as infile:
            state_values = pickle.load(infile)
            player.state_values = state_values
        return player


class ComputerPlayer(Player):
    def __init__(self, player_name="computer", initial_eps=1, alpha=0.1, gamma=1.0, eps_decrease=0.01):
        super(ComputerPlayer, self).__init__(player_name=player_name)
        self.visited_states = []
        self.state_values = dict()
        self.eps = initial_eps
        self.learning_rate = alpha
        self.decay_rate = gamma
        self.eps_decrease = eps_decrease
        self.games_completed = 0

    def best_action(self, env):
        best_value = -np.inf

        best_action = None
        for action in env.possible_actions:
            resulting_grid, reward, is_terminal, debug_info = env.step(action, inplace=False)
            grid_value = self.state_values.get(Environment.grid_to_hash(resulting_grid))
            if grid_value is not None:
                if grid_value > best_value:
                    best_value = grid_value
                    best_action = action
        # Take a random action as best action if the future states are not visited so far
        if best_action is None:
            print("Returning random as best!")
            best_action = self.random_action(env)

        return best_action

    def take_action(self, env: Environment):
        rand = np.random.rand()
        if rand < self.eps:
            action = self.random_action(env)
        else:
            action = self.best_action(env)
        self.visited_states.append(env.hash())
        resulting_grid, reward, is_terminal, debug_info = env.step(action, inplace=False)
        self.visited_states.append(Environment.grid_to_hash(resulting_grid))
        return action

    def feed_reward(self, reward, env):
        feature_val = reward
        for state in self.visited_states[-1::-1]:
            if state not in self.state_values.keys():
                self.state_values[state] = 0
            self.state_values[state] += self.learning_rate * (self.decay_rate * feature_val - self.state_values[state])
            feature_val = self.state_values[state]

        self.games_completed += 1
        self.update_eps()

    def update_eps(self):
        if callable(self.eps_decrease):
            eps_dec_rate = self.eps_decrease(self.games_completed)
        else:
            eps_dec_rate = self.eps_decrease
        if self.eps - eps_dec_rate >= 0:
            self.eps -= eps_dec_rate
        else:
            self.eps = 0

    def reset(self):
        self.visited_states = []

    def pickle_strategy(self):
        with open(f"{self.name}.pkl", "wb") as outfile:
            pickle.dump(self.state_values, outfile)

class HumanPlayer(Player):
    def __init__(self, player_name):
        super(HumanPlayer, self).__init__(player_name=player_name)

    def take_action(self, env):
        while True:
            raw_pos = input(f"{self.name}; please play <row,col>: ")
            pos = tuple(map(int, raw_pos.strip(" ()").split(",")))
            if pos in env.possible_actions:
                return pos
            print(f"{pos} is not allowed")


