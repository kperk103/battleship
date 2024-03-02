# battleship

some reference links:
- minimax algorithm: https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-1-introduction/
- battleship minimax reference code: https://github.com/topics/battleship-game?l=c%23
- gpt design:
- import random

# Constants
BOARD_SIZE = 10
SHIP_SIZE = 3
EMPTY = "~"
SHIP = "S"
HIT = "X"
MISS = "O"

# Initialize boards
player_board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
ai_board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# Utility functions
def print_board(board):
    print("  " + " ".join([chr(c) for c in range(ord('A'), ord('A') + BOARD_SIZE)]))
    for i, row in enumerate(board):
        print(str(i+1).rjust(2) + " " + " ".join(row))

def place_ship(board):
    orientation = random.choice(["horizontal", "vertical"])
    if orientation == "horizontal":
        row = random.randint(0, BOARD_SIZE - 1)
        col = random.randint(0, BOARD_SIZE - SHIP_SIZE)
        for i in range(SHIP_SIZE):
            board[row][col + i] = SHIP
    else:
        row = random.randint(0, BOARD_SIZE - SHIP_SIZE)
        col = random.randint(0, BOARD_SIZE - 1)
        for i in range(SHIP_SIZE):
            board[row + i][col] = SHIP

def is_valid_move(board, row, col):
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and board[row][col] in [EMPTY, SHIP]

def make_move(board, row, col):
    if board[row][col] == SHIP:
        board[row][col] = HIT
        return True
    elif board[row][col] == EMPTY:
        board[row][col] = MISS
        return False

def check_win(board):
    for row in board:
        if SHIP in row:
            return False
    return True

# Minimax algorithm placeholder (to be implemented)
def minimax_move(board):
    # This function will be implemented to make an AI move based on a heuristic.
    # For simplicity, we'll use a random move for now.
    while True:
        row = random.randint(0, BOARD_SIZE - 1)
        col = random.randint(0, BOARD_SIZE - 1)
        if is_valid_move(board, row, col):
            return row, col

# Game setup
place_ship(player_board)
place_ship(ai_board)

# Main game loop
player_turn = True
while True:
    if player_turn:
        print_board(player_board)
        move = input("Enter your move (e.g., A5): ").upper()
        row = int(move[1:]) - 1
        col = ord(move[0]) - ord('A')
        
        if is_valid_move(ai_board, row, col):
            hit = make_move(ai_board, row, col)
            print("Hit!" if hit else "Miss!")
            if check_win(ai_board):
                print("Player 1 wins!")
                break
        else:
            print("Invalid move, try again.")
    else:
        row, col = minimax_move(player_board)
        hit = make_move(player_board, row, col)
        print(f"AI guessed {chr(col + ord('A'))}{row + 1} - {'Hit!' if hit else 'Miss!'}")
        if check_win(player_board):
            print("Player 2 wins!")
            break
    
    player_turn = not player_turn



- structure;
- game: 2 separate boards - 10x10 array which labels indices as either empty, taken or not by a ship (0 or 1), tostring method
- player: current number of ships that are hit, its points, locations its already targeted
- ship: need to know if its been hit and its size (Once the guessing begins, the players may not move the ships. The 5 ships are: Carrier (occupies 5 spaces), Battleship (4), Cruiser (3), Submarine (3), and Destroyer (2))
