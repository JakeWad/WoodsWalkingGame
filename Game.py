import tkinter as tk
import random
import math
import gtts as gt
import os

class Game:
    def __init__(self, grade, players, width, height, stats):
        self.grade = grade
        self.players = players
        self.width = int(width)
        self.height = int(height)
        self.grid = (int(width), int(height))
        self.playerDictionary = {
            "players": list(range(1, int(players) + 1)),
            "moveHistories": [[] for _ in range(int(players))],
            "scores": [0 for _ in range(int(players))],
            "longestRun": 0,
            "shortestRun": float('inf'),
            "totalRunDistance": 0,
            "runCount": 0
        }
        self.totalStats = stats if stats else [0 for _ in range(int(players))]
        self.turnOrder = 1
        self.activePlayers = list(range(1, int(players) + 1))
        self.counter = 0
        self.spriteArray = []
        self.scoreLabel = ""
        self.newcanvas = None
        self.treeImagePath = None
        self.player3Char = None
        self.player4Char = None
        self.player2Char = None
        self.player1Char = None
        self.btnDictionary = dict()

        # Create the board
        self.makeBoard()

    def makeBoard(self):
        instructions = "You are lost in the woods. Click on the squares, and navigate your way back to your friends."
        self.text2speech(instructions, "instructionsMain")
        playsound('./sounds/gameMusic.mp3', block=False)

        scoreSheet = self.getScoreSheet()

        self.newroot = tk.Tk()
        self.newroot.title("Wandering in the Woods")
        cHeight = self.newroot.winfo_screenheight()
        cWidth = self.newroot.winfo_screenwidth()
        self.newroot.geometry(f"{cWidth}x{cHeight}")

        bg = tk.PhotoImage(file="./sprites/bg.gif")
        self.newcanvas = tk.Canvas(self.newroot, width=self.width*100, height=self.height*100, bg="white")
        self.newcanvas.pack(expand=True, fill="both")
        for y in range(self.height):
            for x in range(self.width):
                btn = tk.Button(self.newcanvas, image=bg, height=100, width=100, bd=0,
                                command=lambda x=x, y=y: self.onClick(x, y))
                btn.image = bg
                btn.place(x=x*100, y=y*100)
                self.btnDictionary[(x, y)] = btn

        for player in self.playerDictionary["players"]:
            self.addSprite(player)

        self.newroot.after(5000, lambda: self.text2speech("The game has started", "gameStarted"))
        self.newroot.mainloop()

    def addSprite(self, player):
        imgPath = f"./sprites/player{player}.gif"
        photo = tk.PhotoImage(file=imgPath)
        sprite = self.newcanvas.create_image(50, 50, image=photo, anchor="c")
        self.spriteArray.append(sprite)
        self.newcanvas.tag_bind(sprite, "<Button-1>", lambda event, player=player: self.onClickSprite(event, player))

    def removeSprite(self, player):
        spriteIndex = player - 1
        sprite = self.spriteArray[spriteIndex]
        self.newcanvas.delete(sprite)
        del self.spriteArray[spriteIndex]

    def onClick(self, x, y):
