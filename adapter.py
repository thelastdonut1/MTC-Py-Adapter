# adapter.py

### Purpose:
# Reads data from the device that it is connected to

### Status:
# Creating a very simple start of the adapter to create a device object and read the output and print in the terminal

#TODO: Implement an adapter.config (or potentially adapter.json) file that will be used to get some key settings for the adapter such as port, address, numOfInputs, deviceName, etc.

import logging
import logger as lgr

import time
from datetime import datetime
import socket

from device import Device
from data import Data
from server import Server

class Adapter:
    def __init__(self, deviceName: str, numOfInputs: int = 8):     # Creates the adapter class with a defualt of 8 outputs
        self.device = Device(deviceName, numOfInputs)  # Creates a device object that the adapter will be linked to
        self.version = "1.0.0.0"
        self.device.status = "running"

        self.previousDataSample: list[Data] = []   # Stores the data from the last time the device was sampled
        self.currentDataSample: list[Data] = []    # Stores the data from the most recent read of the device

        self.adapterData: list[Data] = []  # Stores the filtered currentDataSample to only include data that has changed. Used to form SHDR string.
        
        self.adapterDataTemplate = {f"AO{i}": "UNAVAILABLE" for i in range(1, numOfInputs + 1)}

        self.SHDRString = self.formSHDRString() # Forms the SHDR String for the data sample that will be sent to the agent

        self.port = 7878    # Port that the adapter will send data from
        self.IPAddress = socket.gethostbyname(socket.gethostname()) # IP Adrress that the adapter will send data from

        self.socket = Server(self.port, self.IPAddress) # Socket at [IPAddress:Port]

        self.connected = False  # Indicates whether there are any active connections to the adapter

        #TODO: Add this attribute to all classes for easy logging
        self.logger = logging.getLogger('adapterLog')

    def updateExecution(self):
        # Update Execution 
        self.device.execution = "Active"  

    def updateControllerMode(self):
        # Update ControllerMode 
        self.device.controller_mode = "Automatic"

    def updateProgram(self):
        #Update pgm
        self.device.mainprogram = "PART-COUNT-MC"

    def updateProgramComment(self):
        #Update pcmt
        self.programComment = "PART COUNTER DEMO PROGRAM"
        
    # Runs the adapter and performs the device reading, filtering, SHDR formation, and sending at a specified interval
    def run(self):
        # Checks if log file has content. If not, creates new log file. Passes self for properties in log file.
        if lgr.logFileExists(self.logger):
            lgr.startNewLog(self)
        
        self.logger.info('Adapter has been started.')

        # Update Availability to AVAILABLE
        self.device.availability = "AVAILABLE"

        while self.device.status == "running":
            self.checkConnection()
            time.sleep(1)
            while self.connected:                
                self.readDevice()
                self.filterData()
                self.formSHDRString()
                self.sendToAgents()
                time.sleep(5)   # Sets the time period between data sampling and sending
                break
    # Reads the data that the device is outputting every 1 second and updates the adapterData dictionary with newest data sample
    def readDevice(self):
        for i in range(self.device.num_outputs):
            key = "AO" + str(i+1) # Assigns output a name according to the adapter data item naming convention
            value = getattr(self.device, "output_" + str(i+1))  # Gets the attribute value corresponding to the output

            if key in self.adapterDataTemplate:
                outputData = Data(key, value)
                self.currentDataSample.append(outputData)   # Updates the currentSampleData list will all of the current data objects from the device

    # Iterates throught the current data sample to find all the updated values and adds them to the adapter data list
    def filterData(self):
        self.hasChanged()  # Calls the method to check the data to see if it has changed
        for data in self.currentDataSample:
            if data.has_changed:
                self.adapterData.append(data)

    # Iterates through the current and previous sample data and records whether a data item's value has changed        
    def hasChanged(self):
        if not self.previousDataSample: # Checks if list is empty. Should happen on first sample. Sets the has_changed property of all data to True
            for data in self.currentDataSample:
                data.has_changed = True
        else:
            for i in range(len(self.currentDataSample)):
                if self.currentDataSample[i].value != self.previousDataSample[i].value: # If the currentDataSample value with index i does not match the previousDataSample value with index i, changed the "has_changed" attr to True
                    self.currentDataSample[i].has_changed = True

   # Forms the SHDRString and data items for sending to the agent.
    def formSHDRString(self) -> str:
        SHDRTime = datetime.utcnow().isoformat() + "Z"
        SHDRStringsList = [SHDRTime] # Initializes a list to store SHDR strings, starting with the timestamp

        # Clear the adapterData list before adding new data items
        self.adapterData.clear()

        # Add Availability data item to the adapter data
        availability_data = Data("avail", self.device.availability)
        self.adapterData.append(availability_data)

        # Add ControllerMode data item to the adapter data
        controller_mode_data = Data("mode", self.device.controller_mode)
        self.adapterData.append(controller_mode_data)

        # Add Execution data item to the adapter data
        execution_data = Data("execution", self.device.execution)
        self.adapterData.append(execution_data)

        # Add Program data item to the adapter data
        program_data = Data("program", self.device.mainprogram)
        self.adapterData.append(program_data)

        # Add programComment data item to the adapter data
        programComment_data = Data("program_cmt", self.device.programComment)
        self.adapterData.append(programComment_data)

        #Add PartCountAct data item to the adapterData
        PartCountAct_data = Data("PartCountAct", self.device.PartCountAct)
        self.adapterData.append(PartCountAct_data)

        # Update "AO" keys in adapterData based on currentDataSample
        # for data in self.currentDataSample:
        #     if data.key.startswith("AO"):
        #         self.adapterData.append(data)

        # Create SHDR strings for all data items in adapterData
        for data in self.adapterData:
            string = data.SHDRFormat()
            SHDRStringsList.append(string)

        # Concatenate all the SHDR strings to form the final SHDRString
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
       # Set the Availability status to "AVAILABLE" when there are active connections.
        if self.socket.active_connections:
            self.connected = True
            self.device.availability = "AVAILABLE"
            # self.logger.info("Connection established. Availability: %s", self.device.availability)
            # print("Connection established. Availability:", self.device.availability)
        else:
            self.connected = False
            self.device.availability = "UNAVAILABLE"
            # self.logger.info("No active connections. Availability: %s", self.device.availability)



