import tkinter as tk
from playsound import *
import math

MoreStudentPlayers = {}
playerDictionary = {}
activePlayers = 0
turnOrder = 1
newroot = 0
scoreLabel=""
activePlayers = []
counter = 0

class Game:

    def __init__( self, grade, players, width, height):
        self.grade = grade
        self.players = players
        self.grid = (int(width), int(height))
        global activePlayers
        for x in range(1, int(players) + 1):
            activePlayers.append(x)

        global playerDictionary
        playerDictionary = {
            "players":[1,2,3,4],
            "moveHistories" : [[],[],[],[]],
            "scores" : [0,0,0,0],
            "startPoints" : [[0, 0], [0, int(height)-1], [int(width)-1, int(height)-1], [int(width)-1, 0]],
            "longestRun": 0,
            "shortestRun": float('inf'),
            "totalRunDistance": 0,
            "runCount": 0
        }
        
        global MoreStudentPlayers
    MoreStudentPlayers = {
        "MiddleSchoolers":[1,2,3,4,5,6,7,8],
        print("Enter a number to see which grid you endup on":)
        "DifferentMoves":[[],[],[],[],[],[],[],[]]
        "DifferentScores" :[0,0,0,0,0,0,0,0]
        "StartingPoints": [0,0], [0, int(height)-1,[int(width)-1, int(height)-1, int(width)-1, int(height)-1, int(width)-1, int(height)-1, int(width)-1, 0]],
        "LongestRunTime": 0,
        "ShortestRunTime": float('inf'),
        "TotalDistance": 0, " TotalRunCount": 0
    }

        self.makeBoard(int(width), int(height))

    def getScoreSheet(self) :
         scoreString = f"Player {turnOrder}'s turn.\t\t"
         for x in range(int(self.players)):
             scoreString += f"Player {x+1}'s score is {playerDictionary['scores'][x]} \t"
         return scoreString

    def makeBoard(self, width, height) :
        scoreSheet = ""
        scoreSheet += self.getScoreSheet();
        global newroot
        newroot = tk.Tk()
        newroot.title("Wandering in the Woods")
        cHeight = newroot.winfo_screenheight()
        cWidth = newroot.winfo_screenwidth()

        outerCanvas = tk.Canvas(newroot, width=cWidth, height=cHeight)
        outerCanvas.grid(columnspan=3, rowspan=6)
        titleLabel = tk.Label(outerCanvas, text="Wandering in the Woods", fg="black", font=("Helvetica", 32))
        titleLabel.grid(column=1, row=0)
        global scoreLabel
        scoreLabel = tk.Label(outerCanvas, text=scoreSheet)
        scoreLabel.grid(column=1, row=1)
        newcanvas = tk.Canvas(newroot)
        newcanvas.grid(columnspan=width, rowspan=height)

        for a in range(width):
            for b in range(height):
                btn = tk.Button(newcanvas, text=f"{a,b}", command=lambda row=a, col=b: self.amove([row, col]))
                btn.grid(column=a, row=b)

    def winCondition(self):
        global newroot
        newroot.destroy()
        print("YOU'VE WON")

    def amove(self, mylist):
        global turnOrder
        global activePlayers
        global scoreLabel
        global counter
        if len(activePlayers) == 1:
            self.winCondition()
        else:
            playsound("./sounds/singleStep.wav")
            playerIndex = activePlayers
            playerIndex = activePlayers.index(turnOrder)
            playerDictionary["scores"][playerIndex] += 1
            playerDictionary["moveHistories"][playerIndex].append([mylist[0], mylist[1]])

            # Check if players have met
            for x in activePlayers:
                if x != activePlayers[counter]:
                    try:
                        currentPlayer = playerDictionary["moveHistories"][playerIndex][-1]
                        otherPlayers = playerDictionary["moveHistories"][activePlayers.index(x)][-1]
                        if currentPlayer[-1] is not False and otherPlayers[-1] is not False:
                            if otherPlayers[0] == currentPlayer[0] and otherPlayers[1] == currentPlayer[1]:
                                activePlayers.remove(x)
                                if len(activePlayers) == 1:
                                    self.winCondition()
                    except:
                        pass

            # Update turn order
            if counter + 1 >= len(activePlayers):
                counter = 0
            else:
                counter += 1
            turnOrder = activePlayers[counter]

            # Update statistics
            runDistance = 0
            for history in playerDictionary["moveHistories"]:
                if len(history) > 1:
                    runDistance += math.sqrt((history[-1][0]-history[-2][0])**2 + (history[-1][1]-history[-2][1])**2)

            if runDistance > playerDictionary["longestRun"]:
                playerDictionary["longestRun"] = runDistance

            if runDistance < playerDictionary["shortestRun"]:
                playerDictionary["shortestRun"] = runDistance

            playerDictionary["totalRunDistance"] += runDistance
            playerDictionary["runCount"] += 1

            scoreLabel.config(text=f"{self.getScoreSheet()}\nLongest run: {playerDictionary['longestRun']}\nShortest run: {playerDictionary['shortestRun']}\nAverage run distance: {playerDictionary['totalRunDistance']/playerDictionary['runCount']:.2f}")

