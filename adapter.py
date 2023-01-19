# adapter.py

### Purpose:
# Reads data from the device that it is connected to

### Status:
# Creating a very simple start of the adapter to create a device object and read the output and print in the terminal

import time
from datetime import datetime
import socket

from device import Device
from data import Data
from server import Server

class Adapter:
    def __init__(self, deviceName: str, numOfInputs = int(8)):     # Creates the adpater class with a defualt of 8 outputs
        self.device = Device(deviceName, numOfInputs)  # Creates a device object that the adapter will be linked to
        self.device.status = "running"

        self.previousDataSample: list[Data] = []   # Stores the data from the last time the device was sampled
        self.currentDataSample: list[Data] = []    # Stores the data from the most recent read of the device

        self.adapterData: list[Data] = []  # Stores the filtered currentDataSample to only include data that has changed. Used to form SHDR string.

        self.adapterDataTemplate = {"AO1": "UNAVAILABLE", "AO2": "UNAVAILABLE", "AO3": "UNAVAILABLE",
                                 "AO4": "UNAVAILABLE", "AO5": "UNAVAILABLE", "AO6": "UNAVAILABLE",
                                 "AO7": "UNAVAILABLE", "AO8": "UNAVAILABLE", "AO9": "UNAVAILABLE",
                                 "AO10": "UNAVAILABLE", "AO11": "UNAVAILABLE", "AO12": "UNAVAILABLE"
                                 }

        self.SHDRString = self.formSHDRString() # Forms the SHDR String for the data sample that will be sent to the agent

        self.port = 7878    # Port that the adapter will send data from
        self.IPAddress = socket.gethostbyname(socket.gethostname()) # IP Adrress that the adapter will send data from
        # self.IPAddress = 'localhost'
        # self.IPAddress = '172.26.83.77'

        self.socket = Server(self.port, self.IPAddress) # Socket at [IPAddress:Port]

        self.connected = False  # Indicates whether there are any active connections to the adapter

    # TODO: Work on constructor for connecting an adapter to an existing device
    # def __init__(self, device: device):
    #     self.device = device

    # Reads the data that the device is outputting every 1 second and updates the adapterData dictionary with newest data sample
    def readDevice(self):
        for i in range(self.device.num_outputs):
            key = "AO" + str(i+1) # Assigns output a name according to the adapter data item naming convention
            value = getattr(self.device, "output_" + str(i+1))  # Gets the attribute value corresponding to the output

            if key in self.adapterDataTemplate:
                outputData = Data(key, value)
                self.currentDataSample.append(outputData)   # Updates the currentSampleData list will all of the current data objects from the device

    # Iterates through the current and previous sample data and records whether a data item's value has changed        
    def hasChanged(self):
        if not self.previousDataSample: # Checks if list is empty. Should happen on first sample. Sets the has_changed property of all data to True
            for data in self.currentDataSample:
                data.has_changed = True
        else:
            for i in range(len(self.currentDataSample)):
                if self.currentDataSample[i].value != self.previousDataSample[i].value: # If the currentDataSample value with index i does not match the previousDataSample value with index i, changed the "has_changed" attr to True
                    self.currentDataSample[i].has_changed = True

    # Iterates throught the current data sample to find all the updated values and adds them to the adapter data list
    def filterData(self):
        self.hasChanged()  # Calls the method to check the data to see if it has changed
        for data in self.currentDataSample:
            if data.has_changed:
                self.adapterData.append(data)

    # Formats the data into a list of 'SHDRStrings' and adds the SHDRTime to the beginning of the list. Use the form_SHDR_String method to generate the complete string to send to the agent
    def formSHDRString(self) -> str:
        SHDRTime = datetime.utcnow().isoformat() + "Z"
        SHDRStringsList = [SHDRTime]
        for data in self.adapterData:
            string = data.SHDRFormat()
            SHDRStringsList.append(string)
        SHDRString = ''.join(SHDRStringsList)
        self.SHDRString = SHDRString + '\n'

    # Sets the variables back to their default states
    def clean(self):
        self.SHDRString = ''
        self.adapterData.clear()
        self.previousDataSample.clear()
        self.previousDataSample.extend(self.currentDataSample)
        self.currentDataSample.clear()

    # Sends the data to the agent
    def sendToAgents(self):
        if self.socket.active_connections:
            data = self.SHDRString
            self.socket.send(data)
            self.clean()

    # Checks for any connections to the adapter. Changes connection status
    def checkConnection(self):
        if self.socket.active_connections:
            self.connected = True
        else:
            self.connected = False

    # Runs the adapter and performs the device reading, filtering, SHDR formation, and sending at a specified interval
    def run(self):
        while self.device.status == "running":
            self.checkConnection()
            while self.connected:
                self.readDevice()
                self.filterData()
                self.formSHDRString()
                self.sendToAgents()
                time.sleep(5)   # Sets the time period between data sampling and sending
                break

