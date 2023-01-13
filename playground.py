# playground.py

# File for experimenting with the adapter and device communcication and reading the output in the terminal

import threading
import adapter

MTC_Adapter = adapter.Adapter('MyDevice', 8)

# Using Threading:
deviceThread = threading.Thread(target=MTC_Adapter.device.shuffle_input, args=()) 
adapterThread = threading.Thread(target=MTC_Adapter.read_device, args=()) 
deviceThread.start() 
adapterThread.start() 
deviceThread.join() 
adapterThread.join()

# TODO: Create a branch from this project, one that uses multi-threading and one that uses multi-processing to determine which is the better option. Will need to have 3 threads or processes