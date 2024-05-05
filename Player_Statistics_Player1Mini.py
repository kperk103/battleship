import random
import time
from Gameboard import Gameboard
from Minimax import Minimax

# Constants
COLUMNS = 7
NUM_GAMES = 10

def main():
    win_count = 0
    total_time = 0

    # Initialize Minimax for both players
    minimax_player1 = Minimax(depth = 2)
    minimax_player2 = Minimax(depth = 3)

    for _ in range(NUM_GAMES):
        game = Gameboard()
        game_over = False
        start_time = time.time()

        while not game_over:
            # Player 1 (AI - Minimax depth 2)
            col1 = minimax_player1.minimax(game.board, 1)
            if col1 is not None and col1 >= 0 and game.col_idx[col1] > 0:
                game.addDisc(1, col1 + 1)

            # Check if game is over
            state = game.checkWin()
            if state[0] != 0:
                game_over = True
                break

            # Player 2 (AI - Minimax depth 3)
            col2 = minimax_player2.minimax(game.board, 2)
            if col2 is not None and col2 >= 0 and game.col_idx[col2] > 0:
                game.addDisc(2, col2 + 1)

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

        print(f"Game completed in {game_duration:.2f} seconds.")

    average_time = total_time / NUM_GAMES
    print(f"Player 2 (AI) won {win_count}/{NUM_GAMES} games.")
    print(f"Average game duration: {average_time:.2f} seconds.")

if __name__ == "__main__":
    main()
