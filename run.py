# run.py

# File for executing the MTC Python Adapter application

from logger import configureLogger
from threading import Thread
from adapter import Adapter

import logging

configureLogger()

# Create the logger
#* Finds the 'adapterLog' logger configured in logger.py (I do not know how) and uses these settings for the logger
#* This means that to create the log, each object should have a self.logger attribute and it should be set to equal the statement below
appLog = logging.getLogger('adapterLog')

# Creates the Adapter object
#* Set to a default number of 8 objects with a device named 'MyDevice'. Need to have this file read adapter.config to extract arguments to pass to this function.
MTC_Adapter = Adapter('MyDevice', 12)

# Using Threading:
#TODO: Refactor code in adapter.py so that each of these threads are created when the Adapter.run() method is called
deviceThread = Thread(target=MTC_Adapter.device.shuffleInput, args=()) 
adapterThread = Thread(target=MTC_Adapter.run, args=()) 
serverThread = Thread(target=MTC_Adapter.socket.start, args=())
deviceThread.start() 
adapterThread.start() 
serverThread.start()

# Joins all the threads back into the main thread when they have completed
deviceThread.join() 
adapterThread.join()
serverThread.join()


