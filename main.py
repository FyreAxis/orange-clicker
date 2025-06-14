from tkinter import *
from tkinter import ttk
from pynput import mouse
from pynput.mouse import Button, Controller
from pynput import keyboard
from time import *
import threading

#Classes
class Autoclicker(threading.Thread): #Inherit the threading.Thread class

    #Object functions
    #Lets us create an autoclicker object with its own thread
    def __init__(self, period, hotkey, click): 
        #Basic details
        super().__init__() #This ensures the Thread is initialized before this object is
        self.active = False #Is it currently clicking?
        self.enabled = True #Is the Thread active? We'll just keep it quiet for now
        #Mouse details
        self.clickPeriod = period #How often it clicks (in seconds)
        self.clickType = click #What is being clicked
        #Keyboard details
        self.currentMode = "Default"
        self.activateMode = "Press"
        self.hotkey = hotkey #What key needs to be pressed to activate it
        self.simKey = 'a'

    #Turn on or off
    def toggle(self):
        self.setMode("Default")
        global desiredCps
        newCps = desiredCps.get() #Go ahead and get the cps so we can avoid errors if the user changes the cps mid-function call
        if self.active == True:
            self.active = False
        elif Autoclicker.validate_cps(newCps):
            self.active = True
            self.clickPeriod = Autoclicker.convertToPeriod(newCps)
        else:
            print(f"{newCps} is Not a Decimal Greater than Zero.")

    def setMode(self, mode):
        self.currentMode = mode
        global modeVar
        modeVar.set(f"Mode: {mode}")

    def setActivateMode(self, mode):
        self.activateMode = mode

    def recordHotkey(self):
        self.setMode("Hotkey")

    def updateHotkey(self, key):
        if key is not keyboard.Key.esc:
            self.hotkey = key
            print(f"{key} set as HotKey")
            self.setMode("Default")
        else:
            print("Still listening. Escape cannot be bound.")

    def recordSimKey(self):
        self.setMode("SimKey")

    def updateSimKey(self, key):
        if key is not keyboard.Key.esc:
            self.simKey = key
            print(f"{self.simKey} set as SimKey")
            self.setMode("Default")
        else:
            print("Still listening. Esc cannot be bound.")

    #This going to handle flow control
    def on_press(self, key):
        #Default means we do on/off
        if self.currentMode == "Default":
            if key is self.hotkey:
                self.toggle()
                print(f"{self.hotkey} was hit")
        
        #This means we are listening to assign for a new hotkey
        elif self.currentMode == "Hotkey":
            self.updateHotkey(key)

        #This means we are listening to assign a new SimKey
        elif self.currentMode == "SimKey":
            self.updateSimKey(key)

    #This also has some flow control
    def on_release(self, key):
        #If we are pressing, we won't do anything of note
        if self.activateMode == "Press":
            print("Press Mode Enabled, Released Anyway")
        #TODO: We'll need to toggle or something
        elif self.activateMode == "Hold":
            print(f"{key} Released")

    #Where the magic happens
    def autoclick(self):
        while self.enabled:
            while self.active:
                mouse.click(self.clickType)
                sleep(self.clickPeriod)

    #Non-object functions
    def validate_cps(input): #Input validation
        try:
            cps = float(input)
            if cps > 0: return True
            else: return False
        except: return False

    #Only called when input is validated
    def convertToPeriod(cps):
        return 1/float(cps)

#Creates our mouse controller
mouse = Controller()

#Object declaration
autoclicker = Autoclicker(1, keyboard.Key.end, Button.left)

#Start the thread (given by inheritance)
autoclicker.start()

#Outline what the keyboard listener does
listener = keyboard.Listener(
    on_press=autoclicker.on_press,
    on_release=autoclicker.on_release)

#Start the thread
listener.start()

#Tkinter Window Elements
root = Tk() #Declares our main window
root.title("Orange Clicker") #and names it

frame = ttk.Frame(root) #TODO: Implement the frame to make things look nice

nameOfProgram = ttk.Label(root, text="Orange Clicker") #This'll be the top label
nameOfProgram.pack() #All pack functions just actually show the thing, in this case, our label

modeVar = StringVar()
modeVar.set("Mode: ")

modeLabel = ttk.Label(root,
                      textvariable=modeVar,
                      width=40)
modeLabel.pack()

keybindButton = ttk.Button(root,
                            text="Choose the Keybind for the Auto Clicker",
                            width=40,
                            command=autoclicker.recordHotkey)
keybindButton.pack()

clickTypeButton = ttk.Button(root,
                            text="Choose What is Being Clicked",
                            width=40,
                            command=autoclicker.recordSimKey)
clickTypeButton.pack()

startButton = ttk.Button(root,
                        text="Start Auto Clicker",
                        width=40,
                        command=autoclicker.toggle)
startButton.pack()

desiredCps = StringVar()
desiredCps.set("1")

desiredCpsEntry = ttk.Entry(root,
                    textvariable=desiredCps,
                    width=20)
desiredCpsEntry.pack()

numClicks = IntVar()
numClicks.set(0)

def clicked(): #Updates numClicks
    clickSoFar = numClicks.get()
    clickSoFar += 1
    numClicks.set(clickSoFar)

clickTracker = ttk.Label(root,
                        textvariable=numClicks,
                        width=40)
clickTracker.pack()

testButton = ttk.Button(root,
                        text="Test Button",
                        width=40,
                        command=clicked)
testButton.pack()

#This is actually what updates the window
root.mainloop()

#If mainloop ever stops, let's go ahead and close these threads

autoclicker.join()
listener.stop()
listener.join()