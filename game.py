BOARD_SIZE = 10
EMPTY = '--' # 0
SHIP = '*' #1
HIT = 'X' # 2
MISS = 'O' # 3

class Game:
    def __init__(self):
        self.board = [[0]*10]*10
        self.ships = [None]*5

    def isTaken(self, row, col):
        if self.board[row][col] == 1 or self.board[row][col] == 2:
            return True
        return False

    def hasBeenGuessed(self, row, col):
        if self.board[row][col] == 2 or self.board[row][col] == 3:
            return True
        return False
    
    def addShip(self, ship):        
        # check that the ship hasn't already been added
        if self.ships[ship.s_type - 1] != None:
            return False
        
        if ship.ship_orientation == 'H':
            # horizontal
            start = ship.starting.row
            end = ship.starting.row + ship.ship_size
            col = ship.starting.col
            
            for row in range(start, end):
                if self.board[row][col] == 1:
                    return False
                else:
                    self.board[row][col] = 1
        else:
            # vertical
            start = ship.starting.col
            end = ship.starting.col + ship.ship_size
            row = ship.starting.row
            
            for col in range(start, end):
                if self.board[row][col] == 1:
                    return False
                else:
                    self.board[row][col] = 1
                    
        # add ship object to class so we know that ship exists
        self.ships[ship.s_type - 1] = ship
        
    def isHit(self, row, col):
        if self.board[row][col] == 1:
            return True
        return False
    
    def checkWin(self):
        if self.carrier.hit and self.battleship.hit and self.destroyer.hit and self.submarine.hit and self.cruiser.hit:
            return True
        return False
    
    def toString(self):
        gameboard = ""
        for row in self.board:
            gameboard += "| "
            for col in row:
                if col == 0:
                    gameboard += EMPTY + " | "
                elif col == 1:
                    gameboard += SHIP + " | "
                elif col == 2:
                    gameboard += HIT + " | "
                elif col == 3:
                    gameboard += MISS + " | "
            gameboard += "\n"
        print(gameboard)

gameboard = Game()
gameboard.toString()