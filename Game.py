import tkinter as tk
import playsound as playsound
from playsound import *
import math
import gtts as gt
import os

class Game:

    def __init__( self, grade, players, width, height,stats ):
        self.playerDictionary = {}
        self.activePlayers = 0
        self.turnOrder = 1
        self.activePlayers = []
        self.counter = 0
        self.spriteArray = []
        self.scoreLabel = ""
        print(f"stats is {stats}")
        try:
            if(stats is not False and self.totalStats is False):
                self.totalStats = stats
            elif(stats is not False and self.totalStats is not False):
                counter = 0
                for x in stats:
                    self.totalStats[counter] += x
                    counter +=1
            else:
                self.totalStats = stats
        except:
            pass
        self.newcanvas = None
        self.treeImagePath = None
        self.player3Char = None
        self.player4Char = None
        self.player2Char = None
        self.player1Char = None
        self.grade = grade
        self.width = int(width)
        self.height = int(height)
        self.players = players
        self.grid = (int(width), int(height))
        self.btnDictionary = dict()
	self.grid_size = grid_size
        self.grid_shape = grid_shape
        self.meet_time = meet_time

        for x in range(1, int(players) + 1):
            self.activePlayers.append(x)


        if self.grade == 0:
            self.playerDictionary = {
                "players":[1,2],
                "moveHistories" : [[(0, 0)],[( int(width)-1, int(height)-1)]],
                "scores" : [0,0,0,0],
                "longestRun": 0,
                "shortestRun": float('inf'),
                "totalRunDistance": 0,
                "runCount": 0
            }
	if self.grade == 3:
	    self.playerDictionary["longestRunWithoutMeeting"] = 0
	    self.playerDictionary["shortestRunWithoutMeeting"] = float('inf')
	    self.playerDictionary["averageRunWithoutMeeting"] = 0
	if self.grade == 4 or self.grade == 5:
	    self.playerDictionary["longestRunWithoutMeeting"] = 0
	    self.playerDictionary["shortestRunWithoutMeeting"] = float('inf')
	    self.playerDictionary["averageRunWithoutMeeting"] = 0
	
	else:
            self.playerDictionary["players"] = []
            self.playerDictionary["moveHistories"] = []
            self.playerDictionary["scores"] = []
            for x in range(1,int(self.players)+1):
                self.playerDictionary['players'].append(x)
                self.playerDictionary['moveHistories'].append([])
                self.playerDictionary['scores'].append(0)

            self.playerDictionary["longestRun"] = 0
            self.playerDictionary["shortestRun"] = float('inf')
            self.playerDictionary["totalRunDistance"] = 0
            self.playerDictionary["runCount"] = 0


        self.makeBoard()

    @staticmethod
    def text2speech( text,filename):

        txt = gt.gTTS(text)
        txt.save(f"sounds/output/{filename}.mp3")
        playsound(f"sounds/output/{filename}.mp3", block=False)


    def getScoreSheet(self) :
         scoreString = f"Player {self.turnOrder}'s turn.\t\t"
         for x in range(int(self.players)):
             scoreString += f"Player {x+1}'s score is {self.playerDictionary['scores'][x]} \t"
         return scoreString

    def makeBoard(self ):

        instructions="You are lost in the woods. Click on the squares, and navigate your way back to your friends."
        self.text2speech(instructions,"instructionsMain")
        playsound('./sounds/gameMusic.mp3',block=False )
        scoreSheet = ""
        scoreSheet += self.getScoreSheet();


        self.newroot = tk.Tk()
        self.newroot.title("Wandering in the Woods")
        cHeight = self.newroot.winfo_screenheight()
        cWidth = self.newroot.winfo_screenwidth()
        self.newroot.geometry(f"{cWidth}x{cHeight}")


        bgImage = tk.PhotoImage(file="images/mainBG.png",master=self.newroot )
        bgLabel = tk.Label(self.newroot, image=bgImage)
        bgLabel.place(x=0, y=0,anchor='nw')

        lbl=tk.Label(self.newroot)
        lbl.grid(column=1,row=0)

        titleLabel = tk.Label(self.newroot,  text="Wandering in the Woods", fg="black", font=("Helvetica", 32))
        titleLabel.grid(column=2 , row=2  )
	
	if self.grade == 0:  # simple grid for K-2
		self.newcanvas = tk.Canvas(self.newroot, width=cWidth / 3, height=cHeight / 2)
		self.newcanvas.grid(column=2, row=4)
		self.makeGrid()

    	elif self.grade == 3:  # visual maze for grades 3-5
		self.treeImagePath = "images/obstacle.png"
		self.player1Char = tk.PhotoImage(file='images/charSprites/Boy.png', master=self.newroot)
		self.player2Char = tk.PhotoImage(file='images/charSprites/Girl.png', master=self.newroot)
		self.player3Char = tk.PhotoImage(file='images/charSprites/Dog.png', master=self.newroot)
		self.player4Char = tk.PhotoImage(file='images/charSprites/Cat.png', master=self.newroot)
		self.grid = self.generate_maze(self.grid_shape)
		self.newcanvas = tk.Canvas(self.newroot, width=self.grid_size * self.grid_shape[0], height=self.grid_size * self.grid_shape[1])
		self.newcanvas.grid(column=2, row=4)
		self.draw_maze()

    	elif self.grade >= 4:  # complex maze for grades 6-8
		self.treeImagePath = "images/tree.png"
		self.waterImagePath = "images/water.png"
		self.player1Char = tk.PhotoImage(file='images/charSprites/Boy.png', master=self.newroot)
		self.player2Char = tk.PhotoImage(file='images/charSprites/Girl.png', master=self.newroot)
		self.player3Char = tk.PhotoImage(file='images/charSprites/Dog.png', master=self.newroot)
		self.player4Char = tk.PhotoImage(file='images/charSprites/Cat.png', master=self.newroot)



        self.scoreLabel = tk.Label(self.newroot, text=scoreSheet)
        self.scoreLabel.grid(column=2, row=3)
        self.newcanvas = tk.Canvas(self.newroot,width=cWidth/3,height=cHeight/2 )
        self.newcanvas.grid(column=2,row=4)
        self.makeGrid( )

    def makeGrid(self):
       for x in self.newcanvas.winfo_children() :
            x.grid_forget()

       self.player1Char = tk.PhotoImage(file='images/charSprites/Boy.png', master=self.newcanvas)
       self.player2Char = tk.PhotoImage(file='images/charSprites/Girl.png', master=self.newcanvas)
       self.player3Char = tk.PhotoImage(file='images/charSprites/Man.png', master=self.newcanvas)
       self.player4Char = tk.PhotoImage(file='images/charSprites/Woman.png', master=self.newcanvas)
       self.treeImagePath = tk.PhotoImage(file='images/trees/fir_tree_4.png', master=self.newcanvas)


       self.spriteArray = [self.player1Char, self.player2Char, self.player3Char, self.player4Char]

       if self.grade == 0 :
           for a in range(self.width) :
               for b in range(self.height) :
                   btn = tk.Button(self.newcanvas, text=f"{a, b}", bg="green", image=self.treeImagePath,
                                   width="100", height="100", command=lambda row=a, col=b : self.amove((row, col)))
                   btn.image = self.treeImagePath
                   btn.grid(column=a, row=b)
                   self.btnDictionary[(a, b)] = btn
           playerLocation = tuple(self.playerDictionary['moveHistories'][0][0])
           updateBtn = self.btnDictionary[playerLocation]
           updateBtn.config(image=self.spriteArray[0])
           updateBtn.image = self.spriteArray[0]

           playerLocation = tuple(self.playerDictionary['moveHistories'][1][0])
           updateBtn = self.btnDictionary[playerLocation]
           updateBtn.config(image=self.spriteArray[1])
           updateBtn.image = self.spriteArray[1]
       else :
           for a in range(self.width) :
               for b in range(self.height) :
                   btn = tk.Button(self.newcanvas, text=f"{a, b}", bg="green", image=self.treeImagePath,
                                   width="100", height="100", command=lambda row=a, col=b : self.amove((row, col)))
                   btn.image = self.treeImagePath
                   btn.grid(column=a, row=b)
                   self.btnDictionary[(a, b)] = btn

    def newGamePlus(self,):
        self.stats = [self.playerDictionary["longestRun"],self.playerDictionary["shortestRun"],
                      self.playerDictionary["totalRunDistance"],self.playerDictionary["runCount"]]
        Game(self.grade, self.players, self.width, self.height, self.stats)

        self.newroot.destroy()
    def winCondition(self):
        fileList = os.listdir("sounds/output")
        for x in fileList:
            os.remove(f"sounds/output/{x}")
        trophy = tk.PhotoImage(file="images/winAssets/winner.png",master=self.newcanvas)
        for x in self.newcanvas.winfo_children() :
            x.grid_forget()
        average = self.playerDictionary['totalRunDistance'] / self.playerDictionary['runCount']
        statsLabel = tk.Label(self.newcanvas,text=f"\nLongest run: {self.playerDictionary['longestRun']:.2f}\nShortest run:{self.playerDictionary['shortestRun']}\nAverage run distance: {average:.2f}")
        statsLabel.grid(column=1,row=0)
        trophyLabel = tk.Label(self.newcanvas,image=trophy)
        trophyLabel.image=trophy
        trophyLabel.grid(column=1,row=1)
        try:
            btn = tk.Button(self.newcanvas,text="Play again", command=lambda: self.newGamePlus())
            btn.grid(column=1,row=2)
            playsound("./sounds/fanfare.mp3", block=False)

            winSpeech = f"You've Won! Here is how you did."
            player = 1
            for x in self.playerDictionary["scores"] :
                winSpeech += f"player {player} moved {x} times"
            winSpeech += f" the longest run was {self.playerDictionary['longestRun']:.0f}"
            winSpeech += f" the shortest run was {self.playerDictionary['shortestRun']}"
            winSpeech += f" the total distance that was ran was {self.playerDictionary['totalRunDistance']:.0f}"
            winSpeech += f" and the run count was {self.playerDictionary['runCount']:.0f}"
            self.text2speech(winSpeech, "winSpeech")


        except :
           pass
    def removeSprite(self,mylist,spriteId):
        removedSprites = ""
        currBtn = self.btnDictionary[mylist]
        currBtn.config(image=removedSprites)
        currBtn.image = spriteId


        removedSprites = self.spriteArray[spriteId]
        currBtn = self.btnDictionary[mylist]
        currBtn.config(image=removedSprites)
        currBtn.image = removedSprites

    def moveSprites(self, mylist,playerIndex):

        myImageVar = self.spriteArray[playerIndex]
        currBtn = self.btnDictionary[mylist]
        currBtn.config(image=myImageVar)
        currBtn.image = myImageVar

        returnTree = self.treeImagePath
        try:
            if self.playerDictionary['moveHistories'][playerIndex][-1] != mylist :
                a = self.playerDictionary['moveHistories'][playerIndex][-1]
                gridList = (a[0], a[1])
                passBtn = self.btnDictionary[gridList]
                passBtn.config(image=returnTree)
                passBtn.image = returnTree
        except:
            pass
    def amove(self, mylist):

        if len(self.activePlayers) == 1:
            self.winCondition()
        else:

            playsound("./sounds/singleStep.wav",block=False)

            playerIndex = self.activePlayers.index(self.turnOrder)
            self.moveSprites(mylist, playerIndex)
            self.playerDictionary["scores"][playerIndex] += 1
            self.playerDictionary["moveHistories"][playerIndex].append((mylist[0], mylist[1]))


            # Check if players have met
            for x in self.activePlayers:
                if x != self.activePlayers[self.counter]:
                    try:
                        currentPlayer = self.playerDictionary["moveHistories"][playerIndex][-1]
                        otherPlayers = self.playerDictionary["moveHistories"][self.activePlayers.index(x)][-1]
                        if currentPlayer[-1] is not False and otherPlayers[-1] is not False:
                            if otherPlayers[0] == currentPlayer[0] and otherPlayers[1] == currentPlayer[1]:
                                self.removeSprite(mylist, playerIndex)
                                self.activePlayers.remove(x)

                                if len(self.activePlayers) == 1:
                                    self.winCondition()
                    except:
                        pass

            # Update turn order
            if self.counter + 1 >= len(self.activePlayers):
                self.counter = 0
            else:
                self.counter += 1
            self.turnOrder = self.activePlayers[self.counter]

            # Update statistics

            runDistance = 0
            for history in self.playerDictionary["moveHistories"]:
                if len(history) > 1:
                    runDistance += math.sqrt((history[-1][0]-history[-2][0])**2 + (history[-1][1]-history[-2][1])**2)

            if runDistance > self.playerDictionary["longestRun"]:
                self.playerDictionary["longestRun"] = runDistance

            if runDistance < self.playerDictionary["shortestRun"]:
                self.playerDictionary["shortestRun"] = runDistance


            self.playerDictionary["totalRunDistance"] += runDistance
            self.playerDictionary["runCount"] += 1


            labelTxt = self.getScoreSheet()
		self.scoreLabel.configure(text=f"{labelTxt}")
