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
    win_count = 0
    total_time = 0

    for _ in range(NUM_GAMES):
        game = Gameboard()
        minimax = Minimax(depth=2, alphaBeta=True)  # Adjust depth as needed, it affects the runtime though..
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

            # Player 2 (AI - Minimax)
            if game.col_idx[minimax.minimax(game.board, 2)] > 0:
                game.addDisc(2, minimax.minimax(game.board, 2) + 1)

            # Check if game is over
            state = game.checkWin()
            if state[0] != 0:
                game_over = True
                break

        end_time = time.time()
        game_duration = end_time - start_time
        total_time += game_duration

        if game.checkWin()[0] == 2:
            win_count += 1

        # print(f"Game completed in {game_duration:.2f} seconds.")

    average_time = total_time / NUM_GAMES
    print(f"Player 2 (AI) won {win_count}/{NUM_GAMES} games.")
    print(f"Average game duration: {average_time:.2f} seconds.")

if __name__ == "__main__":
    main()
