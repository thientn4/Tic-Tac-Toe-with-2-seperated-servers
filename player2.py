
"""
1.As the client, Player 2 will ask the user for the host information of Player 1 to join the game:
        1.Ask the user for the host name/IP address of Player 1 they want to play with
        2.Ask the user for the port to use in order to play with Player 1
2.Using that information they will attempt to connect to Player 1
        1.Upon successful connection they will send Player 1 the their username (just alphanumeric username with no special characters)
        2.If the connection cannot be made then the user will be asked if they want to try again:
                1.If the user enters 'y' then you will request the host information from the user again
                2.If the user enters 'n' then you will end the program
3.Once Player 2 receives Player 1's username or if the users decides to play again
        1.Player 2 will ask the user for their move using the current player display area. 
        2.Send the move to player 1.
                1.Player 2 will always be x/X
                2.Player 2 will always send the first move to Player 1
                        1.Each move will correspond to the area on the board they user clicks on. 
                3.Once player 2 sends their move they will wait for Player 1's move.
                4.Repeat steps 3.1 - 3.2.3 until the game is over (A game is over when a winner is found or the board is full)
4.Once a game has finished (win, lose, or tie) the user will indicate if they want to play again using the user interface.
        1.If the user enters 'y' or 'Y' then player 2 will send "Play Again" to player 1
        2.If the user enters 'n' or 'N' then player 2 will send "Fun Times" to player 1 and end the program
                1.Once the user is done, the module will print all the statistics.


A dialog that asks the user if they want to play again
"""

from tkinter import messagebox
import tkinter
import socket
from gameboard import BoardClass

pause=True
def turnPause():
    global pause
    pause=not pause
gameBoard={}
mainBoard=BoardClass()
connectionSocket=''

#############################################   Setup Window    ########################################################
mainWindow=tkinter.Tk()
mainWindow.title("player2")
mainWindow.geometry('470x362')
mainWindow.resizable(0,0)

#############################################   Address and name entry    ########################################################
IPName=tkinter.StringVar()
IPName.set('enter your IP here')
IPEntry=tkinter.Entry(mainWindow, text=IPName,width=39)
IPEntry.grid(row=0,column=0,columnspan=3)
portName=tkinter.StringVar()
portName.set('enter your port here')
portEntry=tkinter.Entry(mainWindow, text=portName,width=39)
portEntry.grid(row=1,column=0,columnspan=3)
playerName=tkinter.StringVar()
playerName.set('enter your username here')
nameEntry=tkinter.Entry(mainWindow, text=playerName,width=39)
nameEntry.grid(row=2,column=0,columnspan=3)
#############################################   whose turn and who won   ########################################################
currentPlayerText=tkinter.StringVar()
currentPlayerText.set('whose turn and who won')
currentPlayer=tkinter.Label(mainWindow, textvariable=currentPlayerText,width=31)
currentPlayer.grid(row=3,column=0,columnspan=3)

#############################################   Submit button for address and name    ########################################################
submitText=tkinter.StringVar()
submitText.set('SUBMIT')
submitButton=0
mainBoard.UserName1='Player 1'
def sendAndCheck():
    global connectionSocket
    global mainBoard
    try:
        connectionSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connectionSocket.connect((IPName.get().strip(),int(portName.get().strip())))
        mainBoard.UserName1=connectionSocket.recv(1024).decode('ascii')
        if playerName.get()=='enter your username here':
            playerName.set('Player 2')
        mainBoard.UserName2=playerName.get()
        connectionSocket.send(bytes(playerName.get(),'utf-8'))
    except Exception:
        messagebox.showerror("IP and port 2", "Please enter valid IP and port")
        connectionSocket=''
        return
    submitText.set('please wait for player 1')
    IPEntry['state']='disabled'
    portEntry['state']='disabled'
    nameEntry['state']='disabled'
    if playerName.get()!='enter your username here':
        statDisplay.set(mainBoard.UserName1 +' vs '+mainBoard.UserName2+'\nLast move picked by: '+'player'+'\nGames played: '+str(0)+'\nWin: '+str(0)+'\nLoss: '+str(0)+'\nTie: '+str(0)+'\n')

    acceptance=connectionSocket.recv(10).decode('ascii')
    submitText.set('SUBMIT')
    if acceptance=='quit':
                    connectionSocket=''
                    mainBoard.resetGameBoard()
                    for x in range(0,3):
                        for y in range(0,3):
                            gameBoard[x*10+y].buttonChar.set('')
                    IPEntry['state']='normal'
                    portEntry['state']='normal'
                    nameEntry['state']='normal'
                    submitButton['state']='normal'
                    currentPlayerText.set('whose turn and who won')
                    statDisplay.set(mainBoard.UserName1 +' vs Player 2\nLast move picked by: '+'player'+'\nGames played: '+str(mainBoard.TotalGame)+'\nWin: '+str(mainBoard.TotalWin)+'\nLoss: '+str(mainBoard.TotalLoss)+'\nTie: '+str(mainBoard.TotalTie)+'\n')
                    messagebox.showerror('announce 2', mainBoard.UserName1+" cancelled the game")
                    return
    submitButton['state']='disabled'
    turnPause()
    currentPlayerText.set('Your turn')
submitButton=tkinter.Button(mainWindow,textvariable=submitText,width=31,height=3,command=sendAndCheck)
submitButton.grid(row=0,column=5,rowspan=3)

#############################################   Statistic board    ########################################################
statDisplay=tkinter.StringVar()
statDisplay.set('Player 1'+' vs '+'Player 2'+'\nLast move picked by: '+'player'+'\nGames played: '+str(0)+'\nWin: '+str(0)+'\nLoss: '+str(0)+'\nTie: '+str(0)+'\n')
resultBoard=tkinter.Label(mainWindow, textvariable=statDisplay,width=32,height=20,bg='white')
resultBoard.grid(row=3,column=4,rowspan=12,columnspan=3)
#############################################   quit button   ########################################################
def quitFunc():
    if mainBoard.CountFilled!=0 and mainBoard.CountFilled!=9:
        connectionSocket.send(b'quit')
        connectionSocket.close()
        mainWindow.destroy()
quitButton=tkinter.Button(mainWindow,text='QUIT',width=33,command=quitFunc)
quitButton.grid(row=7,column=0,columnspan=3)

#############################################   game board   ########################################################
def endGame(winOrLost):
    againOrNot=tkinter.messagebox.askquestion ('End of Game 2',winOrLost+'. Click to play again')
    if againOrNot=='no':
        connectionSocket.send(b'Fun Times')
        connectionSocket.close()
        messagebox.showerror("Final Result", statDisplay.get())
        mainWindow.destroy()
    if againOrNot=='yes':
        connectionSocket.send(b'Play Again')
        mainBoard.resetGameBoard()
        for x in range(0,3):
            for y in range(0,3):
                gameBoard[x*10+y].buttonChar.set('')
        currentPlayerText.set('Your turn')
class square:
    def setO(self):
        global connectionSocket
        if mainBoard.CurrentBoard[self.xy//10][self.xy%10]=='' and mainBoard.isGameFinished('x')==False and pause==False:
            currentPlayerText.set(mainBoard.UserName1+'\'s turn')
            mainBoard.playMoveOnBoard(self.xy,'x')
            self.buttonChar.set(mainBoard.CurrentBoard[self.xy//10][self.xy%10])
            mainBoard.LatestUserName=mainBoard.UserName2
            connectionSocket.send(bytes(str(self.xy),'utf-8'))
            mainWindow.update()
            
            check=mainBoard.isGameFinished('x')
            if check=='PTrue':
                currentPlayerText.set('you won')
                statDisplay.set(mainBoard.UserName1+' vs '+mainBoard.UserName2+'\nLast move picked by: '+mainBoard.LatestUserName+'\nGames played: '+str(mainBoard.TotalGame)+'\nWin: '+str(mainBoard.TotalWin)+'\nLoss: '+str(mainBoard.TotalLoss)+'\nTie: '+str(mainBoard.TotalTie)+'\n')
                endGame('You won')
            elif check=='Tie':
                currentPlayerText.set('that was a tie')
                statDisplay.set(mainBoard.UserName1+' vs '+mainBoard.UserName2+'\nLast move picked by: '+mainBoard.LatestUserName+'\nGames played: '+str(mainBoard.TotalGame)+'\nWin: '+str(mainBoard.TotalWin)+'\nLoss: '+str(mainBoard.TotalLoss)+'\nTie: '+str(mainBoard.TotalTie)+'\n')
                endGame('That was a tie')
            elif check==False:
                mainBoard.LatestUserName=mainBoard.UserName1
                coord=connectionSocket.recv(1024).decode('ascii')

                if coord=='quit':
                    connectionSocket=''
                    mainBoard.TotalGame+=1
                    mainBoard.TotalWin+=1
                    mainBoard.resetGameBoard()
                    for x in range(0,3):
                        for y in range(0,3):
                            gameBoard[x*10+y].buttonChar.set('')
                    IPEntry['state']='normal'
                    portEntry['state']='normal'
                    nameEntry['state']='normal'
                    submitButton['state']='normal'
                    currentPlayerText.set('whose turn and who won')
                    statDisplay.set('Player 1 vs '+mainBoard.UserName2+'\nLast move picked by: '+'player'+'\nGames played: '+str(mainBoard.TotalGame)+'\nWin: '+str(mainBoard.TotalWin)+'\nLoss: '+str(mainBoard.TotalLoss)+'\nTie: '+str(mainBoard.TotalTie)+'\n')
                    turnPause()
                    messagebox.showerror('announce 2', mainBoard.UserName1+" want to stop")
                    return
                coord=int(coord)
                
                gameBoard[coord].buttonChar.set('o')
                mainBoard.playMoveOnBoard(coord,'o')
                currentPlayerText.set('Your turn')
                check=mainBoard.isGameFinished('x')
                if check=='OTrue':
                    currentPlayerText.set('you lost')
                    statDisplay.set(mainBoard.UserName1+' vs '+mainBoard.UserName2+'\nLast move picked by: '+mainBoard.LatestUserName+'\nGames played: '+str(mainBoard.TotalGame)+'\nWin: '+str(mainBoard.TotalWin)+'\nLoss: '+str(mainBoard.TotalLoss)+'\nTie: '+str(mainBoard.TotalTie)+'\n')
                    endGame('You lost')
                elif check=='Tie':
                    currentPlayerText.set('that was a tie')
                    statDisplay.set(mainBoard.UserName1+' vs '+mainBoard.UserName2+'\nLast move picked by: '+mainBoard.LatestUserName+'\nGames played: '+str(mainBoard.TotalGame)+'\nWin: '+str(mainBoard.TotalWin)+'\nLoss: '+str(mainBoard.TotalLoss)+'\nTie: '+str(mainBoard.TotalTie)+'\n')
                    endGame('That was a tie')
    def __init__(self,xy):
        self.xy=xy
        self.buttonChar=tkinter.StringVar()
        self.button=tkinter.Button(mainWindow,width=10,height=5,textvariable=self.buttonChar,command=self.setO)
for x in range(0,3):
    for y in range(0,3):
        boardButton=square(x*10+y)
        boardButton.button.grid(row=x+4,column=y)
        gameBoard[x*10+y]=boardButton

def exitAndAnnounce():
    if connectionSocket!='':
        connectionSocket.send(b'quit')
        connectionSocket.close()
    mainWindow.destroy()
mainWindow.protocol("WM_DELETE_WINDOW", exitAndAnnounce)
mainWindow.mainloop()
