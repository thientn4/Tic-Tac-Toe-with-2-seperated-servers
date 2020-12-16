
"""
  1.The user will be asked to provide the host information so that it can establish a socket connection as the server
  2.Player 1 will accept incoming requests to start  a new game
  3.When a connection request is received and accepted, Player 1 will wait for Player 2 to send their username
  4.Once Player 1 receives Player 2's user name, then Player 1 will send "player1" as their username to Player 2 and wait for Player 2 to send their move.
        1.Once Player 1 receives Player 2's move they will ask the user for their move and send it to Player 1 using the current player display area.
                1.Each move will correspond to the area on the board they user clicks on. 
        2.Once player 1 sends their move they will wait for Player 2's move.
        3.Repeat steps 4.1 - 4.2 until the game is over (A game is over when a winner is found or the board is full)
  5.Once a game has finished (win or tie) player 1 will wait for player 2 to indicate if they want to play again using the user interface.
        1.If Player 2 wants to play again then Player 1 will wait for player 2's first move.
        2.If Player 2  does not wants to play again then Player 1 will print the statistics
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
serverSocket=''
clientSocket=''

#############################################   Setup Window    ########################################################
mainWindow=tkinter.Tk()
mainWindow.title("player1")
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
mainBoard.UserName2='Player 2'
def sendAndCheck():
    global clientSocket
    global mainBoard
    global serverSocket
    if submitText.get()=='SUBMIT':
        try:
            serverSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serverSocket.bind((IPName.get().strip(),int(portName.get().strip())))
            serverSocket.listen(1)
            clientSocket, clientAddress=serverSocket.accept()
            if playerName.get()=='enter your username here':
                playerName.set('Player 1')
            mainBoard.UserName1=playerName.get()
            clientSocket.send(bytes(playerName.get(),'utf-8'))
            mainBoard.UserName2=clientSocket.recv(1024).decode('ascii')
        except Exception:
            serverSocket=''
            messagebox.showerror("IP and port 1", "Please enter valid IP and port")
            return
        submitText.set('player 2 is ready, click to play')
        IPEntry['state']='disabled'
        portEntry['state']='disabled'
        nameEntry['state']='disabled'
        statDisplay.set(mainBoard.UserName1 +' vs Player 2\nLast move picked by: '+'player'+'\nGames played: '+str(mainBoard.TotalGame)+'\nWin: '+str(mainBoard.TotalWin)+'\nLoss: '+str(mainBoard.TotalLoss)+'\nTie: '+str(mainBoard.TotalTie)+'\n')
    elif submitText.get()=='player 2 is ready, click to play':
        currentPlayerText.set(mainBoard.UserName2+'\'s turn')
        submitText.set('SUBMIT')
        submitButton['state']='disabled'
        statDisplay.set(mainBoard.UserName1+' vs '+mainBoard.UserName2+'\nLast move picked by: '+'player'+'\nGames played: '+str(mainBoard.TotalGame)+'\nWin: '+str(mainBoard.TotalWin)+'\nLoss: '+str(mainBoard.TotalLoss)+'\nTie: '+str(mainBoard.TotalTie)+'\n')
        clientSocket.send(b'let\'s play')
        mainWindow.update()
        coord=clientSocket.recv(1024).decode('ascii')
        if coord=='quit':
                clientSocket=''
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
                statDisplay.set(mainBoard.UserName1 +' vs Player 2\nLast move picked by: '+'player'+'\nGames played: '+str(mainBoard.TotalGame)+'\nWin: '+str(mainBoard.TotalWin)+'\nLoss: '+str(mainBoard.TotalLoss)+'\nTie: '+str(mainBoard.TotalTie)+'\n')
                messagebox.showerror('announce 1', mainBoard.UserName2+" want to stop")
                return
        coord=int(coord)
        gameBoard[coord].buttonChar.set('x')
        turnPause()
        mainBoard.playMoveOnBoard(coord,'x')
        currentPlayerText.set('Your turn')
        
submitButton=tkinter.Button(mainWindow,textvariable=submitText,width=31,height=3,command=sendAndCheck)
submitButton.grid(row=0,column=5,rowspan=3)
#############################################   Statistic board    ########################################################
statDisplay=tkinter.StringVar()
statDisplay.set('Player 1'+' vs '+'Player 2'+'\nLast move picked by: '+'player'+'\nGames played: '+str(mainBoard.TotalGame)+'\nWin: '+str(mainBoard.TotalWin)+'\nLoss: '+str(mainBoard.TotalLoss)+'\nTie: '+str(mainBoard.TotalTie)+'\n')
resultBoard=tkinter.Label(mainWindow, textvariable=statDisplay,width=32,height=20,bg='white')
resultBoard.grid(row=3,column=4,rowspan=12,columnspan=3)
#############################################   quit button   ########################################################
def quitFunc():
    if mainBoard.CountFilled!=0 and mainBoard.CountFilled!=9:
        clientSocket.send(b'quit')
        serverSocket.close()
        mainWindow.destroy()
quitButton=tkinter.Button(mainWindow,text='QUIT',width=33,command=quitFunc)
quitButton.grid(row=7,column=0,columnspan=3)

#############################################   game board   ########################################################
def endGame(winOrLost):
    if messagebox.showerror('End of Game 1',winOrLost+". Let\'s wait to play again with "+mainBoard.UserName2)!=None:
        global clientSocket
        check=clientSocket.recv(1024).decode('ascii')
        mainBoard.resetGameBoard()
        for x in range(0,3):
            for y in range(0,3):
                gameBoard[x*10+y].buttonChar.set('')
        mainWindow.update()
        if check=='Fun Times':
            clientSocket=''
            IPEntry['state']='normal'
            portEntry['state']='normal'
            nameEntry['state']='normal'
            submitButton['state']='normal'
            currentPlayerText.set('whose turn and who won')
            statDisplay.set(mainBoard.UserName1 +' vs Player 2\nLast move picked by: '+'player'+'\nGames played: '+str(mainBoard.TotalGame)+'\nWin: '+str(mainBoard.TotalWin)+'\nLoss: '+str(mainBoard.TotalLoss)+'\nTie: '+str(mainBoard.TotalTie)+'\n')
            turnPause()
            messagebox.showerror(check, mainBoard.UserName2+" want to stop")
        elif check=='Play Again':
            coord=clientSocket.recv(1024).decode('ascii')
            if coord=='quit':
                    clientSocket=''
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
                    statDisplay.set(mainBoard.UserName1 +' vs Player 2\nLast move picked by: '+'player'+'\nGames played: '+str(mainBoard.TotalGame)+'\nWin: '+str(mainBoard.TotalWin)+'\nLoss: '+str(mainBoard.TotalLoss)+'\nTie: '+str(mainBoard.TotalTie)+'\n')
                    messagebox.showerror('announce 1', mainBoard.UserName2+" want to stop")
                    turnPause()
                    return
            coord=int(coord)
            gameBoard[coord].buttonChar.set('x')
            mainBoard.playMoveOnBoard(coord,'x')
            currentPlayerText.set('Your turn')
            messagebox.showerror(check, mainBoard.UserName2+" want to play again")
class square:
    def setO(self):
        global clientSocket
        if mainBoard.CurrentBoard[self.xy//10][self.xy%10]=='' and mainBoard.isGameFinished('o')==False and pause==False:

            currentPlayerText.set(mainBoard.UserName2+'\'s turn')
            mainBoard.playMoveOnBoard(self.xy,'o')
            self.buttonChar.set(mainBoard.CurrentBoard[self.xy//10][self.xy%10])
            mainBoard.LatestUserName=mainBoard.UserName1
            clientSocket.send(bytes(str(self.xy),'utf-8'))
            mainWindow.update()

            check=mainBoard.isGameFinished('o')
            if check=='Tie':
                currentPlayerText.set('that was a tie')
                statDisplay.set(mainBoard.UserName1+' vs '+mainBoard.UserName2+'\nLast move picked by: '+mainBoard.LatestUserName+'\nGames played: '+str(mainBoard.TotalGame)+'\nWin: '+str(mainBoard.TotalWin)+'\nLoss: '+str(mainBoard.TotalLoss)+'\nTie: '+str(mainBoard.TotalTie)+'\n')
                endGame('That was a tie')
            elif check=='PTrue':
                currentPlayerText.set('you won')
                statDisplay.set(mainBoard.UserName1+' vs '+mainBoard.UserName2+'\nLast move picked by: '+mainBoard.LatestUserName+'\nGames played: '+str(mainBoard.TotalGame)+'\nWin: '+str(mainBoard.TotalWin)+'\nLoss: '+str(mainBoard.TotalLoss)+'\nTie: '+str(mainBoard.TotalTie)+'\n')
                endGame('You won')
            elif check==False:
                mainBoard.LatestUserName=mainBoard.UserName2
                coord=clientSocket.recv(1024).decode('ascii')
                if coord=='quit':
                    clientSocket=''
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
                    statDisplay.set(mainBoard.UserName1 +' vs Player 2\nLast move picked by: '+'player'+'\nGames played: '+str(mainBoard.TotalGame)+'\nWin: '+str(mainBoard.TotalWin)+'\nLoss: '+str(mainBoard.TotalLoss)+'\nTie: '+str(mainBoard.TotalTie)+'\n')
                    turnPause()
                    messagebox.showerror('announce 1', mainBoard.UserName2+" want to stop")
                    return
                coord=int(coord)

                gameBoard[coord].buttonChar.set('x')
                mainBoard.playMoveOnBoard(coord,'x')
                currentPlayerText.set('Your turn')
                check=mainBoard.isGameFinished('o')
                if check=='Tie':
                    currentPlayerText.set('that was a tie')
                    statDisplay.set(mainBoard.UserName1+' vs '+mainBoard.UserName2+'\nLast move picked by: '+mainBoard.LatestUserName+'\nGames played: '+str(mainBoard.TotalGame)+'\nWin: '+str(mainBoard.TotalWin)+'\nLoss: '+str(mainBoard.TotalLoss)+'\nTie: '+str(mainBoard.TotalTie)+'\n')
                    endGame('That was a tie')
                elif check=='OTrue':
                    currentPlayerText.set('you lost')
                    statDisplay.set(mainBoard.UserName1+' vs '+mainBoard.UserName2+'\nLast move picked by: '+mainBoard.LatestUserName+'\nGames played: '+str(mainBoard.TotalGame)+'\nWin: '+str(mainBoard.TotalWin)+'\nLoss: '+str(mainBoard.TotalLoss)+'\nTie: '+str(mainBoard.TotalTie)+'\n')
                    endGame('You lost')
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
    if clientSocket!='':
        clientSocket.send(b'quit')
    if serverSocket!='':
        serverSocket.close()
    mainWindow.destroy()
mainWindow.protocol("WM_DELETE_WINDOW", exitAndAnnounce)
mainWindow.mainloop()
