from tkinter import *
from tkinter import ttk
from pynput import mouse
from pynput.mouse import Button, Controller
from pynput import keyboard

#Functions called by buttons
def Test():
    print("Hello")

def validate_cps(input):
    try:
        cps = float(input)
        if cps > 0:
            return True
        else: return False
    except:
        return False

def convertToCps(period):
    return 1/period

def startAutoClicker():
    if validate_cps(cps.get()):
        print("Correct Value for CPS")
    else:
        print("Not a Decimal Greater than Zero.")

class KeyThread:
    keybindThread = False

    def isThreadFree():
        return not KeyThread.keybindThread
    
    def openThread():
        KeyThread.keybindThread = True
        
    def closeThread():
        KeyThread.keybindThread = False

    def on_press(key):
        if key != keyboard.Key.esc:
            print(f"{key} pressed")
            return False
        print("Still listening. Escape cannot be bound")

    def keybind():
        try:
            KeyThread.isThreadFree()
            KeyThread.openThread()
            with keyboard.Listener(on_press=KeyThread.on_press) as listener:
                KeyThread.closeThread()
                listener.join()
        except:
            print("Keybind thread still open. Choose a key to close it.")

#Tkinter Window Elements
root = Tk() #Declares our main window
root.title("Orange Clicker") #and names it

frame = ttk.Frame(root)

nameOfProgram = ttk.Label(root, text="Orange Clicker")
nameOfProgram.pack()

cps = StringVar()
cps.set("0")

testLabel = ttk.Label(root,
                      textvariable=cps,
                      width=40)
testLabel.pack()

keybindButton = ttk.Button(root,
                            text="Choose the Keybind for the Auto Clicker",
                            width=40,
                            command=KeyThread.keybind)
keybindButton.pack()

clickTypeButton = ttk.Button(root,
                            text="Choose What is Being Clicked",
                            width=40,
                            command=KeyThread.keybind)
clickTypeButton.pack()

startButton = ttk.Button(root,
                        text="Start Auto Clicker",
                        width=40,
                        command=startAutoClicker)
startButton.pack()

cpsEntry = ttk.Entry(root,
                    textvariable=cps,
                    width=20)
cpsEntry.pack()

mouse = Controller()
#mouse.move(-1000,-1000)

root.mainloop() #This is actually what updates the window