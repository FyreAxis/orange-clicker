from tkinter import *
from tkinter import ttk
from pynput import mouse
from pynput.mouse import Button
from pynput import keyboard
from pynput.keyboard import Listener, Key, KeyCode
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
        newCps = root.getDesiredCps() #Go ahead and get the cps so we can avoid errors if the user changes the cps mid-function call
        if self.active == True:
            self.active = False
        elif Autoclicker.validate_cps(newCps):
            self.active = True
            self.clickPeriod = Autoclicker.convertToPeriod(newCps)
        else:
            print(f"{newCps} is Not a Decimal Greater than Zero.")

    def setMode(self, mode):
        self.currentMode = mode
        #updateMode(mode)

    def setActivateMode(self, mode):
        self.activateMode = mode

    def recordHotkey(self):
        self.setMode("Hotkey")

    def updateHotkey(self, key):
        if key is not Key.esc:
            self.hotkey = key
            print(f"{key} set as HotKey")
            self.setMode("Default")
        else:
            print("Still listening. Escape cannot be bound.")

    def recordSimKey(self):
        self.setMode("SimKey")

    def updateSimKey(self, key):
        if key is not Key.esc:
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
    def run(self):
        while self.enabled and self.currentMode == "Default":
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
mouse = mouse.Controller()

#Object declaration
autoclicker = Autoclicker(1, Key.end, Button.left)

#Start the thread (given by inheritance)
autoclicker.start()

#Outline what the keyboard listener does
listener = Listener(
    on_press=autoclicker.on_press,
    on_release=autoclicker.on_release)

#Start the thread
listener.start()

#Tkinter Window Elements

class GUI:
    def __init__(self, root):
        #Some basic variables
        self.root = root
        self.mode = StringVar(value="Mode: Default")
        self.desiredCps = StringVar(value="1")
        self.numClicks = IntVar(value=0)
        
        #The GUI elements
        ttk.Frame(root) #TODO: Implement the frame to make things look nice
        #This'll be the title label
        ttk.Label(root, text="Orange Clicker").pack()
        #This displays the current mode
        ttk.Label(root,
            textvariable=self.mode,
            width=40).pack()
        #This lets you switch to the hotkey recording mode
        ttk.Button(root,
            text="Choose the Keybind for the Auto Clicker",
            width=40,
            command=autoclicker.recordHotkey).pack()
        #This lets you switch to the simulated key recording mode
        ttk.Button(root,
            text="Choose What is Being Clicked",
            width=40,
            command=autoclicker.recordSimKey).pack()
        #This starts/stops the autoclicker
        ttk.Button(root,
            text="Start Auto Clicker",
            width=40,
            command=autoclicker.toggle).pack()
        #This lets you input the desired clicks per second
        ttk.Entry(root,
            textvariable=self.desiredCps,
            width=20).pack()
        #This displays the test button's click count
        ttk.Label(root,
            textvariable=self.numClicks,
            width=40).pack()
        #This is a test button to test clicks/cps
        ttk.Button(root,
            text="Test Button",
            width=40,
            command=self.clicked).pack()
    
    def getDesiredCps(self):
        return self.desiredCps.get()

    def clicked(self): #Updates numClicks
        clicksSoFar = self.numClicks.get()
        clicksSoFar += 1
        self.numClicks.set(clicksSoFar)
        
root = Tk() #Declares our main window
root.title("Orange Clicker") #and names it
GUI(root)
root.mainloop()