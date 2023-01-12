import threading
import device
import adapter
import time

MTC_Adapter = adapter.Adapter('MyDevice', 8)

# Will need to use threading. One thread to run the continuous shuffle inputs loop and one will perform the read_device method continuously.
# MTC_Adapter.device.shuffle_input()
# MTC_Adapter.read_device()

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