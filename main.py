
import tkinter as tk
from tkinter import *
import Game
import playsound as playsound
from playsound import *

import gtts as gt
game = Game.Game
playerOptions = [
    "2",
    "3",
    "4"
]

root = tk.Tk()
root.title("Wandering in the Woods", )
cHeight = root.winfo_screenheight()
cWidth = root.winfo_screenwidth()

canvas = tk.Canvas(root, width=cWidth, height=cHeight)
canvas.grid(columnspan=3, rowspan=3)

bgImage = tk.PhotoImage(file="images/mainBG.png")
bgLabel = tk.Label(root,image=bgImage)
bgLabel.place(x=0,y=0)

var = tk.StringVar()
titleLabel = tk.Label(text="Wandering in the Woods", fg="black", font=("Helvetica", 32))

titleLabel.grid(column=1, row=0)

frame = tk.Frame(root)

frame.grid(column=1, row=1)



def text2speech(text, filename) :
    txt = gt.gTTS(text)
    txt.save(f"sounds/output/{filename}.mp3")
    playsound(f"sounds/output/{filename}.mp3", block=False)

def addFeatures():
    instLvl = tk.Label(frame, text="Choose your level design", fg='red', font=("Helvetica", 16))
    instLvl.pack(side=TOP)

    entryWidth = tk.Entry(frame, textvariable=usrWidth)
    entryWidth.pack(side=TOP)
    xLbl = tk.Label(frame, text="X", fg='red', font=("Helvetica", 16))
    xLbl.pack(side=TOP)
    entryHeight = tk.Entry(frame, textvariable=usrHeight)
    entryHeight.pack(side=TOP)

    instPlayers = tk.Label(frame, text="Choose the number of players", fg='red', font=("Helvetica", 16))
    instPlayers.pack(side=TOP)
    playerList = tk.OptionMenu(frame, usrPlayerNum, *playerOptions)
    playerList.pack(side=TOP)
    subBtn = tk.Button(frame, text="Play", command=lambda : forgetRoot())
    subBtn.pack(side=TOP)
    text2speech("Please provide the dimensions for your level. You can make either a square or a rectangle. Then choose"
                     "how many players you have.","INST_36")

def firstQuestion():

    instGrade = tk.Label(frame, text="Choose your Grade", fg='red', font=("Helvetica", 16))
    instGrade.pack(side=TOP)

    radioK2 = tk.Radiobutton(frame, text="K-2", variable=usrGrade, value="0", )
    radioK2.pack(side=TOP)
    radio35 = tk.Radiobutton(frame, text="3-5", variable=usrGrade, value="1", )
    radio35.pack(side=TOP)
    radio68 = tk.Radiobutton(frame, text="6-8", variable=usrGrade, value="2", )
    radio68.pack(side=TOP)
    text2speech(text= "Select your current grade",filename="firstQuestion")
    subBtn = tk.Button(frame, text="Continue", command=lambda: checkGrade(usrGrade.get(),frame) )
    subBtn.pack(side=TOP)

def hide(hideItem):
    for x in hideItem.winfo_children():
         x.pack_forget()
    hideItem.forget()


def checkGrade(grade,passFrame ):
    print(" in check grade and the usrGrade " + grade)
    hide(passFrame)
    flag = False


    if grade == "1" or grade == "2" and flag is not True:
        flag = True

        addFeatures()
    elif grade == "0":
        flag = False
        instLvl = tk.Label(frame, text="Choose your square's dimensions", fg='red', font=("Helvetica", 16))
        instLvl.pack(side=TOP)

        entryWidth = tk.Entry(frame, textvariable=usrWidth)
        entryWidth.pack(side=TOP)
        subBtn = tk.Button(frame, text="Play", command=lambda :  forgetRoot())
        subBtn.pack(side=TOP)

        text2speech("Please choose what dimension your square will have","INST_k2Square")


def forgetRoot():
    stats = []
    if usrGrade.get() == "0":
        game(0, 2, usrWidth.get(), usrWidth.get(),stats)
        root.destroy()
    elif usrGrade.get() == "1" or usrGrade.get() == "2":
        game(usrGrade.get(), usrPlayerNum.get(), usrWidth.get(), usrHeight.get(),stats)
        root.destroy()



usrPlayerNum = StringVar()
usrWidth = StringVar()
usrHeight = StringVar()
usrGrade = StringVar(value="0")


firstQuestion()
root.mainloop()
