from tkinter import *
from tkinter import ttk
from pynput import mouse
from pynput.mouse import Button, Controller
from pynput import keyboard

#Functions called by buttons
def Test():
    print("Hello")

#def validate_cps(input):
    #for character in input:
        #if integer
            #cps.set("Invalid Input")
            #else return false
        #return true

def startAutoClicker():
    #if validate_cps(cps): indent
    mouse.move(100,100)

#Tkinter Window Elements
root = Tk() #Declares our main window
root.title("Orange Clicker") #and names it

frame = ttk.Frame(root)

nameOfProgram = ttk.Label(root, text = "Orange Clicker")
nameOfProgram.pack()

testVariable = StringVar()
testLabel = ttk.Label(root,
                      text = testVariable,
                      width=40)

keybindButton = ttk.Button(root,
                            text="Choose the Keybind for the Auto Clicker",
                            width=40,
                            command=Test)
keybindButton.pack()

clickTypeButton = ttk.Button(root,
                            text="Choose What is Being Clicked",
                            width=40,
                            command=Test)
clickTypeButton.pack()

startButton = ttk.Button(root,
                        text="Start Auto Clicker",
                        width=40,
                        command=Test)
startButton.pack()

cps = StringVar()
cpsEntry = ttk.Entry(root,
                    textvariable=cps,
                    width=20)
cpsEntry.pack()

mouse = Controller()
#mouse.move(-1000,-1000)

root.mainloop() #This is actually what updates the window