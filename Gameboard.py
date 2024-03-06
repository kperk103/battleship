COLUMNS = 7
ROWS = 6
EMPTY = '-'  # 0
PLAYER1 = 'X'  # 1
PLAYER2 = '0'  # 2


class Gameboard:
    def __init__(self):
        self.board = [[0] * COLUMNS for i in range(ROWS)]
        self.col_idx = {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5}

    def addDisc(self, player, column):
        if self.col_idx[column - 1] < 0:
            # column is already full
            print("Invalid: Column is full")
            return False
        else:
            if player == 1:
                self.board[self.col_idx[column -1]][column - 1] = 1
            else:
                self.board[self.col_idx[column - 1]][column - 1] = 2
            self.col_idx[column - 1] -= 1
        self.checkWin()
        return True

    def checkWin(self):
        winner = 0
        # check if win in column
        for col in range(COLUMNS):
            for row in range(ROWS-3):
                if self.board[row][col] != 0 and self.board[row][col] == self.board[row+1][col] == self.board[row+2][col] == self.board[row+3][col]:
                    winner = self.board[row][col]
                    break
        # check if win in row
        for col in range(COLUMNS - 3):
            for row in range(ROWS):
                if self.board[row][col] != 0 and self.board[row][col] == self.board[row][col+1] == self.board[row][col+2] == self.board[row][col+3]:
                    winner = self.board[row][col]
                    break
        # check if win in positive diagonal
        for col in range(COLUMNS - 3):
            for row in range(ROWS - 3):
                if self.board[row][col] != 0 and self.board[row][col] == self.board[row+1][col+1] == self.board[row+2][col+2] == self.board[row+3][col+3]:
                    winner = self.board[row][col]
                    break
        # check if win in negative diagonal
        for col in range(COLUMNS - 3):
            for row in range(3, ROWS):
                if self.board[row][col] != 0 and self.board[row][col] == self.board[row-1][col+1] == self.board[row-2][col+2] == self.board[row-3][col+3]:
                    winner = self.board[row][col]
                    break
        if winner == 1:
            print("Player 1 wins!")
        elif winner == 2:
            print("Player 2 wins!")
        else:
            return False
        return True

    def toString(self):
        gameboard = ""
        for row in self.board:
            gameboard += "| "
            for col in row:
                if col == 0:
                    gameboard += EMPTY + " | "
                elif col == 1:
                    gameboard += PLAYER1 + " | "
                elif col == 2:
                    gameboard += PLAYER2 + " | "
            gameboard += "\n"
        print(gameboard)