from tictactoe import GameSimulator, Player, ComputerPlayer, HumanPlayer
import pickle


game_stats = {1: 0, -1: 0, 0: 0}

n_games = 0
while True:
    n_games += 1
    p1 = ComputerPlayer.from_file(file_name="p1.pkl")
    p1.eps = 0

    p2 = ComputerPlayer.from_file(file_name="p2.pkl")
    p2.eps = 0

    p_h = HumanPlayer("Maryam")
    if n_games % 2:
        gs = GameSimulator(p1=p1, p2=p_h)
    else:
        gs = GameSimulator(p1=p_h, p2=p2)

    winner = gs.run(print_grid=True)

    if winner:
        game_stats[winner] += 1
    else:
        game_stats[0] += 1

    print(f"Game {n_games+1:6.0f}:", end='\t')
    for key, val in game_stats.items():
        # print(f"{key:2.0f}: {val / (n_games + 1):0.10f}%", end='\t')
        print(f"{key:2.0f}: {val:10.0f}", end='\t')
    print(end='\r')
    # print(f"Game: {n_games+1:6.0f} - Draw!", end="\r")
