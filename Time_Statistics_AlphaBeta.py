import random
import time
from Gameboard import Gameboard
from Minimax import Minimax

# Constants
COLUMNS = 7
NUM_GAMES = 10

def play_random_move(game, player):
    valid_moves = [c for c in range(1, COLUMNS + 1) if game.col_idx[c - 1] > 0]
    if valid_moves:
        move = random.choice(valid_moves)
        game.addDisc(player, move)
    else:
        return False
    return True

def main():
    pruning_win_count = 0
    pruning_total_time = 0
    no_pruning_win_count = 0
    no_pruning_total_time = 0

    # with alpha pruning
    for _ in range(NUM_GAMES):
        game = Gameboard()
        minimax = Minimax(depth=3, alphaBeta=True)  # Adjust depth as needed, it affects the runtime though..
        game_over = False
        start_time = time.time()

        while not game_over:
            # Player 1 (Random moves)
            if not play_random_move(game, 1):
                game_over = True
                break

            # Check if game is over
            state = game.checkWin()
            if state[0] != 0:
                game_over = True
                break

            # Player 2 (AI - Minimax) with pruning
            if game.col_idx[minimax.minimax(game.board, 2)] > 0:
                game.addDisc(2, minimax.minimax(game.board, 2) + 1)

            # Check if game is over
            state = game.checkWin()
            if state[0] != 0:
                game_over = True
                break

        end_time = time.time()
        game_duration = end_time - start_time
        pruning_total_time += game_duration

        if game.checkWin()[0] == 2:
            pruning_win_count += 1

    # without alpha beta pruning
    for _ in range(NUM_GAMES):
        game = Gameboard()
        minimax = Minimax(depth=3, alphaBeta=False)  # Adjust depth as needed, it affects the runtime though..
        game_over = False
        start_time = time.time()

        while not game_over:
            # Player 1 (Random moves)
            if not play_random_move(game, 1):
                game_over = True
                break

            # Check if game is over
            state = game.checkWin()
            if state[0] != 0:
                game_over = True
                break

            # Player 2 (AI - Minimax) with pruning
            if game.col_idx[minimax.minimax(game.board, 2)] > 0:
                game.addDisc(2, minimax.minimax(game.board, 2) + 1)

            # Check if game is over
            state = game.checkWin()
            if state[0] != 0:
                game_over = True
                break

        end_time = time.time()
        game_duration = end_time - start_time
        no_pruning_total_time += game_duration

        if game.checkWin()[0] == 2:
            no_pruning_win_count += 1

    pruning_average_time = pruning_total_time / NUM_GAMES
    print(f"Player 2 (AI) won {pruning_win_count}/{NUM_GAMES} games.")
    print(f"Average game duration: {pruning_average_time:.2f} seconds.")

    no_pruning_average_time = no_pruning_total_time / NUM_GAMES
    print(f"Player 2 (AI) won {no_pruning_win_count}/{NUM_GAMES} games.")
    print(f"Average game duration: {no_pruning_average_time:.2f} seconds.")

if __name__ == "__main__":
    main()
