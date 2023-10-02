# device.py

### Purpose:
# Defines the class for the "device" object that has bewtween 1 and 12 outputs, with these outputs changing to a random integer between 1 and 10 every few seconds

#TODO: Work on creating a longer list of attributes with condition and event items. The device should communicate its list of attributes to the Adapter object instead of using a list of the known device attributes as an Adapter attribute

import random
import time
import threading  # Import the threading module

class Device:
    def __init__(self, name, outputs: int):
        self.lock = threading.Lock()  # Create a lock to ensure thread safety
        
        self.name = name
        self.outputs_list = []
        self.status = "stopped"
        self.controller_mode = "Automatic"  # Initialize the controller mode
        self.execution = "Active"  # Initialize the execution mode
        self.availability = "UNAVAILABLE"  # Initialize availability as "UNAVAILABLE"
        self.mainprogram = "program" # Initialize the main program
        self.programComment = "program_cmt" # Initialize the program comment
        self.PartCountAct = 0 # Initialize PartCountAct

        #Initialize a dictionary called cycle_counters
        self.cycle_counters = { 
            "controller_mode": 0,
            "execution": 0,
            "mainprogram": 0,
            "programComment": 0
        }
        

        # Validates the number of device output channels specified
        if outputs > 12:
            print("Specified number of outputs is too large. Setting to the maximum number of outputs: 12")
            self.num_outputs = 12
        elif outputs < 1:
            print("Specified number of outputs is too small. Setting to the minimum number of outputs: 1")
            self.num_outputs = 1
        else:
            self.num_outputs = outputs

        # Creates an attribute for the device to represent each of the outputs
        for i in range(self.num_outputs):
            setattr(self,'output_' + str(i+1), 0)

        # Creates a list of string with the created attribute names, used for calling specific attributes later
        for i in range(self.num_outputs):
            self.outputs_list.append('output_' + str(i+1))

    # Picks a random output to change the value of at a random interval between 1 and 5 seconds
    # Continuously loops while the device is running to simulate changes in the device output to be read by the adapter
    def shuffleInput(self):
        while self.status == "running":
            i = random.randint(1, self.num_outputs) - 1
            value = self.outputs_list[i]
            setattr(self, value, random.randint(1,10))

            # Update ControllerMode randomly
            self.controller_mode = random.choice(["AUTOMATIC", "MANUAL", "MANUAL_DATA_INPUT"])

            #Update execution randomly.
            self.execution = random.choice(["ACTIVE", "READY", "FEED_HOLD"])

            #Update program  randomly
            self.mainprogram = random.choice(["PART-COUNT-MC","MTC-SP-OVR"])

            #Update program comment randomly
            self.programComment = random.choice(["PART COUNTER DEMO PROGRAM REV-02D","MTCONNECT TEST. SPINDLE OVERRIDES"])
 
            # Increment PartCountAct based on cycling attributes
            self.update_part_count_act()

            time.sleep(random.randint(1,5))

    # Used to increment PartsCountAct. 
    def update_part_count_act(self):
        # Check if all cycling attributes have cycled twice
        if all(self.cycle_counters[attr] >= 2 for attr in self.cycle_counters):
            self.PartCountAct += 1
            # Reset the cycle counters
            for attr in self.cycle_counters:
                self.cycle_counters[attr] = 0
        else:
            # Increment the cycle counters for attributes that have cycled
            for attr in self.cycle_counters:
                if getattr(self, attr) != "AUTOMATIC": # Check if the current value of the attribute specified by 'attr' is not equal to "AUTOMATIC"
                    self.cycle_counters[attr] += 1

    # Used to turn the device on or off and also as an attribute that can be reported to the adapter
    def changeStatus(self, status):
        valid_status = ["stopped", "paused", "running"]
        if status in valid_status:
            self.status = status
             # Update availability based on status
            if status == "running":
                self.availability = "AVAILABLE"
            else:
                self.availability = "UNAVAILABLE"
            print("Availability changed to:", self.availability)
