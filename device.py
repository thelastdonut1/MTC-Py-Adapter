
# device.py

### Purpose:
# Defines the class for the "device" object that has bewtween 1 and 12 outputs, with these outputs changing to a random integer between 1 and 10 every few seconds

#TODO: Work on creating a longer list of attributes with condition and event items. The device should communicate its list of attributes to the Adapter object instead of using a list of the known device attributes as an Adapter attribute

 #TODO while loop that reads the inputs 
import platform
import pyautogui
import psutil
import time

class Device:
    def __init__(self, name):
        self.name = name
        self.version  = self.getVersion()
        self.user = self.getUser()
        self.cursor = self.getCursor()
        self.CPU = self.getCPU()
        self.battery = self.getBattery()
        
        

    def getUser(self):
        UserName = psutil.users()
        self.user = UserName[0].name

    def getCursor(self):
        cursorPOS = pyautogui.position()
        self.cursor = f"({cursorPOS.x},{cursorPOS.y})"

    def getVersion(self):
        verSet = platform.win32_ver()
        self.version = verSet[1]
        
    def getCPU(self):
        varCPU = psutil.cpu_percent()
        self.CPU = varCPU

    def getBattery(self):
        bat = psutil.sensors_battery()
        self.battery = bat[0]

    def run(self):
        while True:
            self.getUser()
            self.getCursor()
            self.getVersion()
            self.getCPU()
            self.getBattery()
            time.sleep(5)
            