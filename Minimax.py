import Gameboard
import random

#connect 4 minimax

#from gameboard.py
COLUMNS = 7
ROWS = 6
EMPTY = 0  # 0
PLAYER1 = 1  # 1
PLAYER2 = 2  # 2



class Minimax:

    def __init__(self, depth=float('inf'), alphaBeta=False):
        self.depth = depth
        self.alphaBeta = alphaBeta



    #integrate getCols() function, takes a boardstate, and returns a list of the
    #columns in the board
    def getCols(self, currState):
        numColumns = len(currState[0])
        columns = [[row[col] for row in currState] for col in range(numColumns)]
        return columns

    #integrate getRows() function, takes a boardstate, and returns a list of the
    #columns in the board
    def getRows(self, currState):
        rows = [row for row in currState]
        return rows


    #integrate checkWin() function, takes a boardstate, and returns the mark 
    #of whoever won if there is a winner, 0 if the game is still ongoing, 
    #or -1 if the game ended with no winner
    def checkWin(self, currState): 
        winner = 0
        # check if win in column
        for col in range(COLUMNS):
            for row in range(ROWS-3):
                if currState[row][col] != 0 and currState[row][col] == currState[row+1][col] == currState[row+2][col] == currState[row+3][col]:
                    winner = currState[row][col]
                    break
        # check if win in row
        for col in range(COLUMNS - 3):
            for row in range(ROWS):
                if currState[row][col] != 0 and currState[row][col] == currState[row][col+1] == currState[row][col+2] == currState[row][col+3]:
                    winner = currState[row][col]
                    break
        # check if win in positive diagonal
        for col in range(COLUMNS - 3):
            for row in range(ROWS - 3):
                if currState[row][col] != 0 and currState[row][col] == currState[row+1][col+1] == currState[row+2][col+2] == currState[row+3][col+3]:
                    winner = currState[row][col]
                    break
        # check if win in negative diagonal
        for col in range(COLUMNS - 3):
            for row in range(3, ROWS):
                if currState[row][col] != 0 and currState[row][col] == currState[row-1][col+1] == currState[row-2][col+2] == currState[row-3][col+3]:
                    winner = currState[row][col]
                    break
        if winner != 0:
            return winner
        else: 
            chips_left = 0
            for row in currState:
                for element in row:
                    if element != PLAYER1 and element != PLAYER2:
                        chips_left += 1
    
            return 0 if chips_left > 0 else -1

    
    #integrate getValid() function, takes a boardstate, and returns a 1d array 
    #of size 7 of all the valid columns a piece can be dropped on. 
    #1 at the column index if a piece can be dropped, 0 if it cannot.
    def getValid(self, currState):
        transposedArray = [[row[col] for row in currState] for col in range(len(currState[0]))]

        validArray = []

        # Iterate through columns
        for column in transposedArray:
            row = 5
            while (column[row] != 0 or column[row] != 0) and row >= 0:
                row -= 1

            if row < 0:
                validArray.append(0)
            else:
                validArray.append(1)

        return validArray

        


    #takes a boardstate array, and returns the boardstate array with the specified 
    #piece dropped into the specified column, in place
    def dropPiece(self, currState, piece, column):
        row = 5

        while currState[row][column] != 0:
            row -= 1
            if row == 0: 
                break

        currState[row][column] = piece

        return currState
    
    #takes a boardstate array, and removes the topmost piece in a specified column,
    #in place
    #takes a boardstate array, and removes the topmost piece in a specified column,
    #in place
    def removePiece(self, currState, column):
        row = 5

        while currState[row][column] != 0:
            row -= 1
            if row == -1: 
                break
            
        row += 1
        
        if row == 6: 
            return currState

        currState[row][column] = 0 #0 is empty
        return currState




    #evaluates a score for a window array of 4 pieces. 
    def evaluateWindow(self, window, piece):
        score = 0

        #its better to just win than to block
        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(EMPTY) == 1:
            score += 10
        elif window.count(piece) == 2 and window.count(EMPTY) == 2:
            score += 5
        elif window.count(piece) == 1 and window.count(EMPTY) == 3:
            score += 2
        elif window.count(piece) == 0 and window.count(EMPTY) == 3:
            score -= 1
        elif window.count(piece) == 0 and window.count(EMPTY) == 2:
            score -= 4
        elif window.count(piece) == 0 and window.count(EMPTY) == 1:
            score -= 9
        
        return score



    #returns an integer score based on the currState of the game, 
    #and a given piece. (the piece's score will contribute to positive score
    #opponents piece contributing to negative score)
    def scorePos(self, currState, piece):
        score = 0

        #score columns
        for column in self.getCols(currState):
            for i in range(ROWS - 3):
                window = column[i:i+4]
                score += self.evaluateWindow(window, piece)

        #score rows
        for row in self.getRows(currState):
            for i in range(COLUMNS - 3):
                window = row[i:i+4]
                score += self.evaluateWindow(window, piece)

        #score positive sloped diagonal
        for row in range(ROWS - 3):
            for col in range(COLUMNS - 3):
                window = [currState[row + i][col + i] for i in range(4)]
                score += self.evaluateWindow(window, piece)

        #score negative sloped diagonal
        for row in range(ROWS - 3):
            for col in range(COLUMNS - 3):
                window = [currState[row + 3 - i][col + i] for i in range(4)]
                score += self.evaluateWindow(window, piece)

        return score



    #parameters: currState, a two dimensional array with 6 rows, 7 cols,  
    # containing the current state of the game
    #currPlayer, the player who's turn it is currently.
    #returns a tuple with the column to drop the piece, and the heuristic value
    def minimax(self, currState, currPlayer):
        return self.miniHelper(currState, currPlayer, currPlayer, 0, float('-inf'), float('inf'))[0]
    
    def miniHelper(self, currState, currPlayer, maximizer, depth, alpha, beta):
        #check for game over or tie, assign points accordingly
        didWin = self.checkWin(currState)
        if didWin != 0: 
            if didWin == PLAYER1: 
                return (None, float('inf')) if maximizer == PLAYER1 else (None, float('-inf'))
            elif didWin == PLAYER2: 
                return (None, float('inf')) if maximizer == PLAYER2 else (None, float('-inf'))
            else: 
                return (None, 0) #game ended in a tie
            
        #check if we have reached past the max depth
        if depth > self.depth:
            return (None, self.scorePos(currState, maximizer))

        #one dimensional array of length 7 filled with 1 if a disc can be placed 
        #on that column, 0 if not integrate getValid() method
        validDrop = self.getValid(currState)
        nextPlayer = PLAYER1 if currPlayer == PLAYER2 else PLAYER2

        #maximize or minimize
        val = float('-inf') if currPlayer == maximizer else float('inf')
        col = -1
        for i in range(len(validDrop)):
            if validDrop[i] == 1:
                updated = self.dropPiece(currState, currPlayer, i)
                score = self.miniHelper(updated, nextPlayer, maximizer, depth + 1, alpha, beta)[1]
                #undo drop
                self.removePiece(currState, i)

                if currPlayer == maximizer:
                    if score > val: 
                        val = score
                        col = i
                    alpha = max(alpha, val)
                else: 
                    if score < val: 
                        val = score
                        col = i
                    beta = min(beta, val)

                # if using alpha beta pruning
                if (self.alphaBeta):
                    if alpha >= beta:
                        break
        
        if col == -1: 
            #the bot knows they will lose no matter what next turn, 
            #just place the disc in the first column that is valid
            #to prevent it from giving up.
            indices = [i for i, x in enumerate(validDrop) if x == 1]
            col = random.choice(indices)

        return col, val
    



'''
example usage: 

ai = Minimax()
mini1 = Minimax(3)  #<--- creates a minimax class object, with maximum search depth of length 3
mini2 = Minimax() #<--- creates a minimax class object with no maximum search depth

mini1.minimax(currState, currPlayer) #<-- returns an optimal column to drop, as well as the heuristic val
'''
