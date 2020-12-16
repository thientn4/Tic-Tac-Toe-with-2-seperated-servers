
"""
Note this module is to be imported and used by both player1 and player2 modules
Class Variables:
    The current board of the game that keeps track of all the moves  
    Usernames of both players
    Username of the last player to have a turn
    Total Number of games played
    Total Number of wins
    Total Number of ties
    Total Number of losses
Class Methods:
    recordGamePlayed() #Updates how many total games have been played
    resetGameBoard() #Clear all the moves from game board
    playMoveOnBoard() #Updates the game board with the player's move
    isBoardFull() #Checks if the board is full (I.e. no more moves to make)
    isGameFinished() #Checks if the latest move resulted in a win, loss or tie
                     #Updates the wins, losses and ties count if the game is over
    computeStats() #Gathers and returns the following information: 
                            #Usernames of both players
                            #The username of the last person to make a move
                            #The total number of games
                            #The total number of wins
                            #The total number of losses
                            #The total number of ties
"""
class BoardClass:
    def __init__(self):
        self.CountFilled=0
        self.CurrentBoard=[['','',''],['','',''],['','','']]
        self.UserName1='Player 1'
        self.UserName2='Player 2'
        self.LatestUserName='none'
        self.TotalGame=0
        self.TotalWin=0
        self.TotalTie=0
        self.TotalLoss=0
    def recordGamePlayed(self):
        self.TotalGame+=1
    def resetGameBoard(self):
        self.CurrentBoard=[['','',''],['','',''],['','','']]
        self.CountFilled=0
    def playMoveOnBoard(self, coord, player):
        self.CurrentBoard[coord//10][coord%10]=player
        self.CountFilled+=1
    def isBoardFull(self):
        return self.CountFilled==9
    def isGameFinished(self, player):
        opponent='o'
        if player=='o': 
            opponent='x'
        if self.CurrentBoard[0][0]==self.CurrentBoard[1][1] and self.CurrentBoard[1][1]==self.CurrentBoard[2][2]:
            if self.CurrentBoard[0][0]==player:
                self.TotalWin+=1
                self.TotalGame+=1
                return 'PTrue'
            if self.CurrentBoard[0][0]==opponent:
                self.TotalLoss+=1
                self.TotalGame+=1
                return 'OTrue'
        if self.CurrentBoard[0][2]==self.CurrentBoard[1][1] and self.CurrentBoard[1][1]==self.CurrentBoard[2][0]:
            if self.CurrentBoard[0][2]==player:
                self.TotalWin+=1
                self.TotalGame+=1
                return 'PTrue'
            if self.CurrentBoard[0][2]==opponent:
                self.TotalLoss+=1
                self.TotalGame+=1
                return 'OTrue'
        for x in range(0,3):
            countRowP=0
            countLineP=0
            countRowO=0
            countLineO=0
            for y in range(0,3):
                if self.CurrentBoard[x][y]==player:
                    countLineP+=1
                if self.CurrentBoard[x][y]==opponent:
                    countLineO+=1
                if self.CurrentBoard[y][x]==player:
                    countRowP+=1
                if self.CurrentBoard[y][x]==opponent:
                    countRowO+=1
            if countRowO==3 or countLineO==3:
                self.TotalLoss+=1
                self.TotalGame+=1
                return 'OTrue'
            if countRowP==3 or countLineP==3:
                self.TotalWin+=1
                self.TotalGame+=1
                return 'PTrue'
        if self.isBoardFull():
            self.TotalTie+=1
            self.TotalGame+=1
            return 'Tie'
        return False
    def computeStats(self):
        return self.UserName1, self.UserName2, self.LatestUserName, self.TotalGame, self.TotalWin, self.TotalTie, self.TotalLoss