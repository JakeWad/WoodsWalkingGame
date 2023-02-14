import tkinter as tk
from playsound import *

playerDictionary = {}
activePlayers = 0
turnOrder = 1
newroot = 0
scoreLabel=""
activePlayers = []
counter = 0

class Game:

    def __init__( self,grade, players, width, height):
        self.grade = grade
        self.players = players
        self.width = width
        self.height = height
        global activePlayers
        for x in range(1, int(players) + 1):
            activePlayers.append(x)

        global playerDictionary
        playerDictionary = {
                    "players":[1,2,3,4],
                    "moveHistories" : [[],[],[],[]],
                    "scores" : [0,0,0,0],
                    "startPoints" : [[0, 0], [0, height], [width, height], [width, 0]],
        }

        self.makeBoard(width,height)

    def getScoreSheet(self) :
         scoreString = f"Player {turnOrder}'s turn.\t\t"
         for x in range(int(self.players)):
             scoreString += f"Player {x+1}'s score is {playerDictionary['scores'][x]} \t"
         return scoreString

    def makeBoard(self,width,height) :
        scoreSheet = ""
        scoreSheet +=  self.getScoreSheet();
        global newroot
        newroot = tk.Tk()
        newroot.title("Wandering in the Woods", )
        cHeight = newroot.winfo_screenheight()
        cWidth = newroot.winfo_screenwidth()

        outerCanvas = tk.Canvas(newroot, width=cWidth, height=cHeight)
        outerCanvas.grid(columnspan=3, rowspan=6)
        titleLabel = tk.Label(outerCanvas, text="Wandering in the Woods", fg="black", font=("Helvetica", 32))
        titleLabel.grid(column=1, row=0)
        global scoreLabel
        scoreLabel =    tk.Label(outerCanvas, text = scoreSheet)
        scoreLabel.grid(column=1, row=1)
        newcanvas = tk.Canvas(newroot)
        newcanvas.grid(columnspan=int(width), rowspan=int(height))

        a=0
        b=0
        while a != int(width)    :
            btn = tk.Button(newcanvas, text=f"{a,b}", command=lambda row = a, col = b:  self.amove([row, col]))
            btn.grid(column=a, row=b)

            while b != int(height) :
                btn = tk.Button(newcanvas, text=f"{a,b}", command=lambda row = a, col = b:  self.amove([row, col]))
                btn.grid(column=a, row=b)
                b += 1
            b = 0
            a += 1


    def winCondtion(self) :
        global newroot
        newroot.destroy()
        print("YOU'VE WON")

    def amove(self,  mylist ) :
        global turnOrder
        global activePlayers
        global scoreLabel
        global counter
        if  len(activePlayers) == 1 :
             self.winCondtion()
        else:
            playsound("./sounds/singleStep.wav")
            playerDictionary["scores"][activePlayers.index(turnOrder)] += 1
            playerDictionary["moveHistories"][activePlayers.index(turnOrder)].append([mylist[0], mylist[1]])


            for x in  activePlayers  :
                if x is not  activePlayers[counter] :
                    try:

                        currentPlayer = playerDictionary["moveHistories"][activePlayers.index(turnOrder)][-1]
                        otherPlayers =playerDictionary["moveHistories"][activePlayers.index(x)][-1]
                        if currentPlayer[-1] != False and otherPlayers[-1] != False :
                            if otherPlayers[0] == currentPlayer[0] and  otherPlayers[1] == currentPlayer[1]:
                                activePlayers.remove(x)
                    except:
                        pass

            if  counter + 1 >=  len(activePlayers) :
                     counter = 0
            else :
                      counter += 1
            turnOrder = activePlayers[counter]
            scoreLabel.config(text=f"{self.getScoreSheet()}")