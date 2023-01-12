# device.py

### Purpose:
# Defines the class for the "device" object that has bewtween 1 and 10 outputs, with these outputs changing to a random integer between 1 and 10 every few seconds

import random
import time
import tkinter as tk

class Device:
    def __init__(self, name, outputs):
        self.name = name
        self.num_outputs = outputs
        self.outputs_list = []
        self.status = "stopped"

        for i in range(self.num_outputs):
            setattr(self,'output_' + str(i+1), 0)

        for i in range(self.num_outputs):
            self.outputs_list.append('output_' + str(i+1))

    def shuffle_input(self):
        while self.status == "running":
            i = random.randint(1, self.num_outputs) - 1
            value = self.outputs_list[i]
            setattr(self, value, random.randint(1,10))
            time.sleep(random.randint(1,5))

    def change_status(self, status):
        valid_status = ["stopped", "paused", "running"]
        if status in valid_status:
            self.status = status
