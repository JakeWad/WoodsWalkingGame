import tkinter as tk
from playsound import *

from main import game

playerDictionary = {}
activePlayers = 0
turnOrder = 1
newroot = 0
scoreLabel = ""
activePlayers = []
counter = 0

import tkinter as tk
from playsound import *
from itertools import combinations


class Game:
    def __init__(self, grade, players, width, height):
        self.newroot = None
        self.scoreSheet = None
        self.newcanvas = None
        self.scoreLabel = None
        self.titleLabel = None
        self.outerCanvas = None
        self.grade = grade
        self.players = players
        self.width = width
        self.height = height
        self.activePlayers = []
        self.turnOrder = 1
        self.playerDictionary = {}
        self.counter = 0
        self.makeBoard(width, height)

    def makeBoard(self, width, height):
        for x in range(1, int(self.players) + 1):
            self.activePlayers.append(x)

        self.playerDictionary = {
            "players": [1, 2, 3, 4],
            "moveHistories": [[], [], [], []],
            "scores": [0, 0, 0, 0],
            "startPoints": [[0, 0], [0, height], [width, height], [width, 0]],
        }

        self.scoreSheet = tk.StringVar()
        self.scoreSheet.set(self.getScoreSheet())

        self.newroot = tk.Tk()
        self.newroot.title("Wandering in the Woods", )
        cHeight = self.newroot.winfo_screenheight()
        cWidth = self.newroot.winfo_screenwidth()

        self.outerCanvas = tk.Canvas(self.newroot, width=cWidth, height=cHeight)
        self.outerCanvas.grid(columnspan=3, rowspan=6)

        self.titleLabel = tk.Label(self.outerCanvas, text="Wandering in the Woods", fg="black", font=("Helvetica", 32))
        self.titleLabel.grid(column=1, row=0)

        self.scoreLabel = tk.Label(self.outerCanvas, textvariable=self.scoreSheet)
        self.scoreLabel.grid(column=1, row=1)

        self.newcanvas = tk.Canvas(self.newroot)
        self.newcanvas.grid(columnspan=int(width), rowspan=int(height))

        for a in range(int(width)):
            for b in range(int(height)):
                btn = tk.Button(self.newcanvas, text=f"{a, b}", command=lambda row=a, col=b: self.amove([row, col]))
                btn.grid(column=a, row=b)

    def getScoreSheet(self):
        scoreString = f"Player {self.turnOrder}'s turn.\t\t"
        for x in range(int(self.players)):
            scoreString += f"Player {x + 1}'s score is {self.playerDictionary['scores'][x]} \t"
        return scoreString

    def winCondtion(self):
        self.newroot.destroy()
        print("YOU'VE WON")

    def amove(self, mylist):
        if len(self.activePlayers) == 1:
            self.winCondtion()
        else:
            playsound("./sounds/singleStep.wav")

            # Update score and move history of the current player
            self.playerDictionary["scores"][self.activePlayers.index(self.turnOrder)] += 1
            self.playerDictionary["moveHistories"][self.activePlayers.index(self.turnOrder)].append(
                [mylist[0], mylist[1]])

            # Check if any players have found each other
            player_combinations = combinations(self.activePlayers, 2)
            for player_pair in player_combinations:
                player1, player2 = player_pair
                player1_history = self.playerDictionary["moveHistories"][self.activePlayers.index(player1)]
                player2_history = self.playerDictionary["moveHistories"][self.activePlayers.index(player2)]
                if player1_history and player2_history and player1_history[-1] == player2_history[-1]:
                    # If there are 3
                    if self.players in ['3', '4']:
                        # Find the remaining player and add them to the group
                        remaining_player = list(set(self.activePlayers) - set(player_pair))[0]
                        self.activePlayers.remove(remaining_player)
                        playsound("./sounds/groupStep.wav")
                        self.scoreSheet.set(self.getScoreSheet())
                        self.playerDictionary["moveHistories"][self.activePlayers.index(player1)].append(False)
                        self.playerDictionary["moveHistories"][self.activePlayers.index(player2)].append(False)
                        self.playerDictionary["moveHistories"][self.activePlayers.index(remaining_player)].append(False)
                        self.playerDictionary["scores"][self.activePlayers.index(player1)] += 1
                        self.playerDictionary["scores"][self.activePlayers.index(player2)] += 1
                        self.playerDictionary["scores"][self.activePlayers.index(remaining_player)] += 1
                    else:
                        playsound("./sounds/denyStep.wav")
                        self.scoreSheet.set(self.getScoreSheet())
                        self.playerDictionary["moveHistories"][self.activePlayers.index(player1)][-1] = False
                        self.playerDictionary["moveHistories"][self.activePlayers.index(player2)][-1] = False

                    # Update turn order
                if self.counter + 1 >= len(self.activePlayers):
                    self.counter = 0
                else:
                    self.counter += 1
                self.turnOrder = self.activePlayers[self.counter]

                # Update score label
                self.scoreSheet.set(self.getScoreSheet())


