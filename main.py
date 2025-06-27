from tkinter import *
from tkinter import ttk
from pynput import mouse
from pynput.mouse import Button
from pynput import keyboard
from pynput.keyboard import Listener, Key, KeyCode
from time import *
import threading

#The Autoclicker class encompasses the strict autoclicker and the GUI
class Autoclicker(threading.Thread): #Inherit the threading.Thread class

    #Object functions
    #__init__ Lets us construct an Autoclicker object with its own thread
    def __init__(self, root, hotkey, click): 
        #Object Properties
        super().__init__() #This ensures the Thread is initialized before this object is
        #Autoclicker-management-specific properties
        self.active = False #Is it currently clicking?
        self.enabled = True #Is the Thread active? We'll just keep it quiet for now
        #Mouse-management-details
        self.clickPeriod = 1 #How often it clicks (in seconds)
        self.clickType = click #What mousebutton is being clicked
        #Keyboard-management-details
        self.currentMode = "Default" #This is a little redundant, but this is our actual mode
        self.pressOrHold = "Press" #This is whether we press or hold to enable the autoclicker
        self.hotkey = hotkey #What key needs to be pressed to activate it
        self.simKey = 'a' #This is what key is being clicked (when not a mouse click)
        #Tkinter-specific properties
        self.root = root #root is our root window which we will be passed later on
        self.mode = StringVar(value="Mode: Default") #By default, our object will be in default mode
        self.desiredCps = StringVar(value="1") #By default, our autoclicker will be 1 CPS
        self.numClicks = IntVar(value=0) #This is for tracking clicks in a test, by default it is 0

        #Tkinter GUI elements
        ttk.Frame(root).pack() #TODO: Implement the frame to make things look nice
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
            command=self.recordHotkey).pack()
        #This lets you switch to the simulated key recording mode
        ttk.Button(root,
            text="Choose What is Being Clicked",
            width=40,
            command=self.recordSimKey).pack()
        #This starts/stops the autoclicker
        ttk.Button(root,
            text="Start Auto Clicker",
            width=40,
            command=self.toggleClicking).pack()
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
        #This just cleanly (hopefully) closes the program
        ttk.Button(root,
                   text="Exit Program",
                   width=20,
                   command=self.close).pack()

    #Turns autoclicker clicking on or off
    def toggleClicking(self):
        self.setMode("Default")
        newCps = self.getDesiredCps() #Go ahead and get the cps so we can avoid errors if the user changes the cps mid-function call
        if self.active == True: #If it's clicking, we'll stop clicking
            self.active = False
        elif Autoclicker.validate_cps(newCps): #If it has a valid cps, then we'll start clicking
            self.active = True
            self.clickPeriod = Autoclicker.convertToPeriod(newCps) #with whatever CPS the user input
        else: #This is the case for an invalid number, so we don't start clicking
            print(f"{newCps} is Not a Decimal Greater than Zero.")

    #Just a shorthand for setting the current mode
    def setMode(self, mode):
        self.currentMode = mode
        self.mode.set(value=f"Mode: {mode}") #This may be redundant eventually

    def setPressOrHold(self, pressOrHold):
        self.pressOrHold = pressOrHold

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
                self.toggleClicking()
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
        if self.pressOrHold == "Press":
            print(f"Press: {key} Released.")
        #TODO: We'll need to toggleClicking or something
        elif self.pressOrHold == "Hold":
            print(f"Hold: {key} Released.")

    #Where the magic happens
    def run(self):
        while self.enabled:
            while self.active and self.currentMode == "Default":
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
    
    def getDesiredCps(self):
        return self.desiredCps.get()

    def clicked(self): #Updates numClicks
        clicksSoFar = self.numClicks.get()
        clicksSoFar += 1
        self.numClicks.set(clicksSoFar)

    def close(self):
        self.enabled = False
        autoclicker.join()
        listener.join()
        listener.stop()
        root.quit()
        
root = Tk() #Declares our main window
root.title("Orange Clicker") #and names it

#Creates our mouse controller
mouse = mouse.Controller()

#Object declaration
autoclicker = Autoclicker(root, Key.end, Button.left)

#Start the thread (given by inheritance)
autoclicker.start()

#Outline what the keyboard listener does
listener = Listener(
    on_press=autoclicker.on_press,
    on_release=autoclicker.on_release)

#Start the thread
listener.start()

root.mainloop()