# adapter.py

### Purpose:


### Status:
# Creating a very simple start of the adapter to create a device object and read the output and print in the terminal

import device
import time
import os

class Adapter:
    def __init__(self, deviceName):
        self.device = device.Device(deviceName, 8)
        self.device.status = "running"

    def __init__(self, deviceName, numOfInputs):
        self.device = device.Device(deviceName, numOfInputs)
        self.device.status = "running"


    def read_device(self):
        # os.system('cls' if os.name == 'nt' else 'clear')  # clear terminal before printing
        # while self.device.status == "running":
        os.system('cls' if os.name == 'nt' else 'clear')  # clear terminal before printing
        for i in range(self.device.num_outputs):
            value = getattr(self.device, "output_" + str(i+1))
            print("Value of output {} is {}".format(i+1, value))
        time.sleep(1)