# playground.py

# File for experimenting with the adapter and device communcication and reading the output in the terminal

import threading
import adapter

MTC_Adapter = adapter.Adapter('MyDevice', 8)

# Using Threading:
t1 = threading.Thread(target=MTC_Adapter.device.shuffle_input, args=()) 
t2 = threading.Thread(target=MTC_Adapter.read_device, args=()) 
t1.start() 
t2.start() 
t1.join() 
t2.join()


# Filter Duplicates:
## Option in agent config file (in the adapter section)
## Also possible to only send updated data items from the adapter by filtering on the adapter side