# adapter.py

### Purpose:
# Reads data from the device that it is connected to

### Status:
# Creating a very simple start of the adapter to create a device object and read the output and print in the terminal

import device
import time
import datetime
import socket

class Adapter:
    def __init__(self, deviceName: str):     # Creates the adpater class with a defualt of 8 outputs
        self.device = device.Device(deviceName, 8)  # Creates a device object that the adapter will be linked to
        self.device.status = "running"

        self.adapterData = {}
        self.adapterDataTemplate = {"AO1": "UNAVAILABLE", "AO2": "UNAVAILABLE", "AO3": "UNAVAILABLE",
                                 "AO4": "UNAVAILABLE", "AO5": "UNAVAILABLE", "AO6": "UNAVAILABLE",
                                 "AO7": "UNAVAILABLE", "AO8": "UNAVAILABLE", "AO9": "UNAVAILABLE",
                                 "AO10": "UNAVAILABLE", "AO11": "UNAVAILABLE", "AO12": "UNAVAILABLE"
                                 }

        self.SHDRString = self.format_data()

    def __init__(self, deviceName: str, numOfInputs: int):    # Creates the adapter class with a specified number of outputs (up to 12)
        self.device = device.Device(deviceName, numOfInputs)
        self.device.status = "running"
    
    def __init__(self, device: device):
        self.device = device

    # Reads the data that the device is outputting every 1 second and updates the adapterData dictionary with newest data sample
    def read_device(self):
        while self.device.status == "running":
            # os.system('cls' if os.name == 'nt' else 'clear')  # clear terminal before printing
            for i in range(self.device.num_outputs):
                key = "AO" + str(i) # Assigns output a name according to the adapter data item naming convention
                value = getattr(self.device, "output_" + str(i+1))  # Gets the attribute value corresponding to the output

                # data = Data(key, value)
                data = {key: value}

                self.update_dict()
                self.adapterData.update(data)   # Updates the adapterData dictionary with the new data

                # print("Value of output {} is {}".format(i+1, value))

            time.sleep(1)   # Sets the time period between data sampling
            
    # TODO: Add in the method that the adapter will use to map key value pairs to data items defined in the device file
    def update_dict(self, data: dict):
        if self.has_changed(data):
            if data.keys()[0] in self.adapterDataTemplate:
                self.adapterData.update(data)
                # Needs to be more robust. Currently ignores any data items that do not match keys in the dictionary, without informing the user

    def has_changed(self, data: dict):
        key = data.keys()[0]
        # key = data.items()[0][0]

        # Check to see if key is already in dictionary
        if key not in self.adapterData:
            return True

        # Check to see if the value associated with the key aligns with the exisitng {key: value} in the adapterData dict
        # If the {key: value} pairs do not match the value has changed and the function returns true
        if data.values()[0] != self.adapterData[key]:
            return True
        else:
            return False

    # Formats the data into a list of 'SHDRStrings' and adds the SHDRTime to the beginning of the list. Use the form_SHDR_String method to generate the complete string to send to the agent
    def format_data(self):
        SHDRTime = datetime.datetime().utcnow().isoformat() + "Z"
        SHDRStringsList = [SHDRTime]
        for [key, value] in self.adapterData.items():
            SHDRString = "|" + key + "|" + value
            SHDRStringsList.append(SHDRString)
        SHDRString = ''.join(SHDRStringsList)
        return SHDRString



    # TODO: Add in the method that the adapter will use to send data to agent using SHDR. Will need to use another thread

    # TODO: Find a method for the adapter to send InitialData when the connection to the agent is established

# TODO: Find a way to implement a class to hold new data. Each entry in the dictionary should be a "Data" object with a key value pair as well as a status indicating whether the value has change since the last data sent to the agent. Bypassed for now
# class Data:
#     def __init__(self, key, value):
#         self.key = key
#         self.value = value
#         self.dataItem = ""
#         self.has_changed = False

#     def has_changed(self):
#         if self.value != 