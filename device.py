
# device.py

### Purpose:
# Defines the class for the "device" object that has bewtween 1 and 12 outputs, with these outputs changing to a random integer between 1 and 10 every few seconds

#TODO: Work on creating a longer list of attributes with condition and event items. The device should communicate its list of attributes to the Adapter object instead of using a list of the known device attributes as an Adapter attribute

 #TODO while loop that reads the inputs 
# import platform
import pyautogui
import psutil
import time
import distro 
import random
from blink import SSDisplay, readPotentiometer, blink
import threading

class Device:
    def __init__(self, name):
        self.name = name                              # Set the name attribute to the provided name
        self.version  = self.getVersion()             # Set the version attribute by calling the getVersion() method
        self.user = self.getUser()                     # Set the user attribute by calling the getUser() method
        self.cursor = self.getCursorX()                # Set the cursor attribute by calling the getCursorX() method
        self.cursorY = self.getCursorY()               # Set the cursorY attribute by calling the getCursorY() method
        self.CPU = self.getCPU()                       # Set the CPU attribute by calling the getCPU() method
        self._display = SSDisplay(16, 12, 19, 13, 26, 21, 20, active_high=False)  # Create an instance of SSDisplay with specified pin numbers
        self.digit = self._display.AdapterSend         # Set the digit attribute to the AdapterSend value of _display
        self._reader = readPotentiometer()             # Create an instance of readPotentiometer
        self.analog = self._reader.numRange            # Set the analog attribute to the numRange value of _reader
        self.state = blink()                           # Create an instance of blink and assign it to the state attribute
        self.ON = self.state.LEDstate                  # Set the ON attribute to the LEDstate value of state

    def shuffle_display(self):
        while True:
            self._display.display(self.analog)          # Call the display method of _display with the analog attribute as an argument
            self.digit = self._display.AdapterSend      # Set the digit attribute to the AdapterSend value of _display
            self.analog = self._reader.numRange         # Set the analog attribute to the numRange value of _reader
            time.sleep(0.05)

    def getUser(self):
        UserName = psutil.users()                      # Get the currently logged-in user(s) information
        self.user = UserName[0].name                   # Set the user attribute to the name of the first user

    def getCursorX(self):
        cursorPOS = pyautogui.position()                # Get the current position of the cursor
        self.cursorX = cursorPOS.x                      # Set the cursorX attribute to the x-coordinate of the cursor position

    def getCursorY(self):
        cursorPOS = pyautogui.position()                # Get the current position of the cursor
        self.cursorY = cursorPOS.y                      # Set the cursorY attribute to the y-coordinate of the cursor position

    def getVersion(self):
        verSet = distro.linux_distribution()            # Get the version information of the Linux distribution
        self.version = verSet[1]                        # Set the version attribute to the second element of the version information

    def getCPU(self):
        varCPU = psutil.cpu_percent()                    # Get the current CPU usage percentage
        self.CPU = varCPU                                # Set the CPU attribute to the CPU usage percentage

    def run(self):
        threadSSD = threading.Thread(target=self.shuffle_display, args=())   # Create a thread for shuffle_display method
        threadANA = threading.Thread(target=self._reader.run_analog, args=()) # Create a thread for run_analog method of _reader
        threadBLINK = threading.Thread(target=self.state.go_blink, args=())  # Create a thread for go_blink method of state
        threadSSD.start()                                 # Start the thread for shuffle_display
        threadANA.start()                                 # Start the thread for run_analog
        threadBLINK.start()                               # Start the thread for go_blink
        while True:
            self.getUser()                                # Update the user attribute
            self.getCursorX()                             # Update the cursorX attribute
            self.getCursorY()                             # Update the cursorY attribute
            self.getVersion()                             # Update the version attribute
            self.getCPU()                                 # Update the CPU attribute
            time.sleep(5)      