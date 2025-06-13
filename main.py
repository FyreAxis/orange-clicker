from tkinter import *
from tkinter import ttk
from pynput import mouse
from pynput.mouse import Button, Controller
from pynput import keyboard
from time import *

#Functions called by buttons
class Autoclicker:

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
        KeyThread.setMode("Default")
        if Autoclicker.validate_cps(cps.get()):
            mouse = Controller()
            
        else:
            print("Not a Decimal Greater than Zero.")

class KeyThread:

    currentMode = "Default"
    pressOrHold = "Press"
    hotkey = keyboard.Key.space
    simKey = 'a'

    def setMode(mode):
        KeyThread.currentMode = mode
        global modeVar
        modeVar.set(f"Mode: {mode}")

    def recordHotkey():
        KeyThread.setMode("Hotkey")

    def updateHotkey(key):
        if key is not keyboard.Key.esc:
            KeyThread.hotkey = key
            print(f"{KeyThread.hotkey} set as HotKey")
            KeyThread.setMode("Default")
        else:
            print("Still listening. Escape cannot be bound.")

    def recordSimKey():
        KeyThread.setMode("SimKey")

    def updateSimKey(key):
        if key is not keyboard.Key.esc:
            KeyThread.simKey = key
            print(f"{KeyThread.simKey} set as SimKey")
            KeyThread.setMode("Default")
        else:
            print("Still listening. Esc cannot be bound.")

    def on_press(key): #Is going to handle flow control
        if KeyThread.currentMode == "Default":
            #Start/Stop autoclicker
            if key is KeyThread.hotkey:
                print(f"{KeyThread.hotkey} was hit")
            else:
                print(f"Not equal. Key: {key}, Hotkey: {KeyThread.hotkey}")

        elif KeyThread.currentMode == "Hotkey":
            KeyThread.updateHotkey(key)

        elif KeyThread.currentMode == "SimKey":
            KeyThread.updateSimKey(key)

    def on_release(key):
        if KeyThread.pressOrHold == "Press":
            print("Press Mode Enabled, Released Anyway")
        elif KeyThread.pressOrHold == "Hold":
            print(f"{key} Released")

#Tkinter Window Elements
root = Tk() #Declares our main window
root.title("Orange Clicker") #and names it

frame = ttk.Frame(root)

nameOfProgram = ttk.Label(root, text="Orange Clicker")
nameOfProgram.pack()

modeVar = StringVar()
modeVar.set("Mode: ")

modeLabel = ttk.Label(root,
                      textvariable=modeVar,
                      width=40)
modeLabel.pack()

keybindButton = ttk.Button(root,
                            text="Choose the Keybind for the Auto Clicker",
                            width=40,
                            command=KeyThread.recordHotkey)
keybindButton.pack()

clickTypeButton = ttk.Button(root,
                            text="Choose What is Being Clicked",
                            width=40,
                            command=KeyThread.recordSimKey)
clickTypeButton.pack()

startButton = ttk.Button(root,
                        text="Start Auto Clicker",
                        width=40,
                        command=Autoclicker.startAutoClicker)
startButton.pack()

cps = StringVar()
cps.set("0")

cpsEntry = ttk.Entry(root,
                    textvariable=cps,
                    width=20)
cpsEntry.pack()

listener = keyboard.Listener(
    on_press=KeyThread.on_press,
    on_release=KeyThread.on_release)
listener.start()

root.mainloop() #This is actually what updates the window