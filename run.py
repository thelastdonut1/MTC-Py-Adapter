# run.py

# File for executing the MTC Python Adapter application

import threading
import adapter
import logging

# Create the logger
#* Finds the 'adapterLog' logger configured in logger.py (I do not know how) and uses these settings for the logger
#* This means that to create the log, each object should have a self.logger attribute and it should be set to equal the statement below
logger = logging.getLogger('adapterLog')

# Creates the Adapter object
#* Set to a default number of 8 objects with a device named 'MyDevice'. Need to have this file read adapter.config to extract arguments to pass to this function.
MTC_Adapter = adapter.Adapter('MyDevice', 12)

# Using Threading:
#TODO: Refactor code in adapter.py so that each of these threads are created when the Adapter.run() method is called
deviceThread = threading.Thread(target=MTC_Adapter.device.shuffleInput, args=()) 
adapterThread = threading.Thread(target=MTC_Adapter.run, args=()) 
serverThread = threading.Thread(target=MTC_Adapter.socket.start, args=())
deviceThread.start() 
adapterThread.start() 
serverThread.start()

# Tests for the logger object
#TODO: Begin implementing logging statements in the code
logger.debug('Device has been shuffled')
logger.info('Adapter has been started')
logger.error('Error connecting to server')

# Joins all the threads back into the main thread when they have completed
deviceThread.join() 
adapterThread.join()
serverThread.join()


