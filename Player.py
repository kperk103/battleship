from Gameboard import Gameboard
from Minimax import Minimax

if __name__ == "__main__":
    game = Gameboard()
    mini = Minimax(1)
    turn_number = -1 # Turns start on turn # 0.

    print("Welcome to Connect 4!")

    #Game continues as long as nobody wins... 
    #is there a case when all discs are used and nobody wins?
    while not game.checkWin():
        turn_number += 1
        invalid_input = True

        while invalid_input:
            game.toString()
            player = (turn_number % 2) + 1 

            col = 0
            if player == 1:
                col = input(f"Player {player} ({'X' if player == 1 else '0'}), Select a column (1-7): ")
            else:
                col = mini.minimax(game.board, 2) + 1
            print("\n\n\n---------------------------------------------------")
            
            try:
                col = int(col)
                if col < 1 or col > 7 or not game.addDisc(player, col):
                    print("Invalid Input")
                else:
                    invalid_input = False
            except ValueError:
                print("Invalid Input")

    print(f"Player {game.checkWin()} wins!")
    game.toString()
            






        
