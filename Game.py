from Player import Player

class Game():

    def init(self):
        self.player1 = Player() # real
        self.player2 = Player() # ai
        self.playingStatus = True

    def gameOver(self):
        if self.player1.gameboard.checkWin():
            print("Player 1 Wins")
        else:
            print("Player 2 Wins")
        self.playingStatus = False

    def getPlayingStatus(self):
        return self.playingStatus