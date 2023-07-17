
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
        self.name = name
        self.version  = self.getVersion()
        self.user = self.getUser()
        self.cursor = self.getCursorX()
        self.cursorY = self.getCursorY()
        self.CPU = self.getCPU()
        self._display = SSDisplay( 16, 12, 19, 13, 26, 21, 20, active_high=False)
        self.digit = self._display.AdapterSend
        self._reader = readPotentiometer()
        self.analog = self._reader.numRange
        self.state = blink()
        self.ON = self.state.LEDstate
        # self.battery = self.getBattery()
        

    def shuffle_display(self):
        while True:
            self._display.display(self.analog)
            self.digit = self._display.AdapterSend
            self.analog = self._reader.numRange
            time.sleep(0.05)


    def getUser(self):
        UserName = psutil.users()
        self.user = UserName[0].name

    def getCursorX(self):
        cursorPOS = pyautogui.position()
        self.cursorX = cursorPOS.x

    def getCursorY(self):
        cursorPOS = pyautogui.position()
        self.cursorY = cursorPOS.y

    def getVersion(self):
        verSet = distro.linux_distribution()
        self.version = verSet[1]
        
    def getCPU(self):
        varCPU = psutil.cpu_percent()
        self.CPU = varCPU

    # def getBattery(self):
    #     bat = psutil.sensors_battery()
    #     self.battery = bat[0]


    def run(self):
        threadSSD = threading.Thread(target=self.shuffle_display, args=()) 
        threadANA = threading.Thread(target=self._reader.run_analog, args=())
        threadBLINK = threading.Thread(target=self.state.go_blink, args=())
        threadSSD.start()
        threadANA.start()
        threadBLINK.start()
        while True:
            self.getUser()
            self.getCursorX()
            self.getCursorY()
            self.getVersion()
            self.getCPU()
            # self.getBattery()
            time.sleep(5)
       
            