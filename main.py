import tkinter as tk
from tkinter import *
import Game
import Audio as Audio

from gtts import gTTS
game = Game.Game
Audio = Audio.Audio
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
    txt =  gTTS(text)
    txt.save(f"sounds/output/{filename}.mp3")
    Audio(filename).play()

def addFeatures(grade):
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

    if grade == '2':
        instLvl = tk.Label(frame, text="Choose your movement constraints", fg='red', font=("Helvetica", 16))
        instLvl.pack(side=TOP)

        entryWidth = tk.Entry(frame, textvariable=xCon)
        entryWidth.pack(side=TOP)
        xLbl = tk.Label(frame, text="X", fg='red', font=("Helvetica", 16))
        xLbl.pack(side=TOP)
        entryHeight = tk.Entry(frame, textvariable=yCon)
        entryHeight.pack(side=TOP)
        text2speech(
            "Please provide the dimensions for your level. You can make either a square or a rectangle. Then choose"
            "how many players you have. You can also specify how your characters will move", "INST_36")

    else:
        text2speech(
            "Please provide the dimensions for your level. You can make either a square or a rectangle. Then choose"
            "how many players you have.", "INST_36")
    subBtn = tk.Button(frame, text="Play", command=lambda : forgetRoot())
    subBtn.pack(side=TOP)


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
    hide(passFrame)
    flag = False


    if grade == "1" or grade == "2" and flag is not True:
        flag = True

        addFeatures(usrGrade.get())
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
    stats = None
    constraint = []
    if usrGrade.get() == "0":
        game(0, 2, usrWidth.get(), usrWidth.get(),constraint,stats)
        root.destroy()
    elif usrGrade.get() == "1" or usrGrade.get() == "2":
        game(usrGrade.get(), usrPlayerNum.get(), usrWidth.get(), usrHeight.get(),[xCon,yCon],stats)
        root.destroy()



usrPlayerNum = StringVar()
usrWidth = StringVar()
usrHeight = StringVar()
usrGrade = StringVar(value="0")
xCon = StringVar(value="1")
yCon = StringVar(value="1")

firstQuestion()
root.mainloop()
