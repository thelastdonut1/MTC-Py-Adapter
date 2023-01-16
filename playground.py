# playground.py

# File for experimenting with the adapter and device communcication and reading the output in the terminal

import threading
import adapter

MTC_Adapter = adapter.Adapter('MyDevice', 8)

# Using Threading:
deviceThread = threading.Thread(target=MTC_Adapter.device.shuffleInput, args=()) 
adapterThread = threading.Thread(target=MTC_Adapter.run, args=()) 
deviceThread.start() 
adapterThread.start() 
deviceThread.join() 
adapterThread.join()

