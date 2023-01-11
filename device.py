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
        self.status = "stopped"

        self.output_1 = 0
        self.output_2 = 0
        self.output_3 = 0
        self.output_4 = 0
        self.output_5 = 0
        self.output_6 = 0
        self.output_7 = 0
        self.output_8 = 0

        self.outputs_list = ['output_1', 'output_2', 'output_3', 'output_4', 'output_5', 'output_6', 'output_7', 'output_8']

    def shuffle_input(self):
            i = random.randint(1, self.num_outputs) - 1
            value = self.outputs_list[i]
            setattr(self, value, random.randint(1,10))
            # time.sleep(random.randint(1,5))

    # def shuffle_inputs(self):
    #     while self.status == "running":
    #         i = random.randint(1, self.num_outputs) - 1
    #         value = self.outputs_list[i]
    #         setattr(self, value, random.randint(1,10))
    #         time.sleep(random.randint(1,5))

    def change_status(self, status):
        valid_status = ["stopped", "paused", "running"]
        if status in valid_status:
            self.status = status
