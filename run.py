# playground.py

# File for experimenting with the adapter and device communcication and reading the output in the terminal

import threading
import adapter
import logging

# Create the logger
logger = logging.getLogger('myLogger')

# Set the logging level
logger.setLevel(logging.DEBUG)

# Specify the path
path = r'C:\Users\momoore\OneDrive - Mazak Corporation\Documents\MTConnect'
fileName = r'\pythonAdapterLog.txt'
fullPath = path + fileName

# Create a file handler
# file_handler = logging.FileHandler('fullPath')

# # Set the log format
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# # Set the file handler's format
# file_handler.setFormatter(formatter)

# # Add the file handler to the logger
# logger.addHandler(file_handler)

# MTC_Adapter = adapter.Adapter('MyDevice', 8)

# MTC_Adapter.logger = logger

# Using Threading:
deviceThread = threading.Thread(target=MTC_Adapter.device.shuffleInput, args=()) 
adapterThread = threading.Thread(target=MTC_Adapter.run, args=()) 
serverThread = threading.Thread(target=MTC_Adapter.socket.start, args=())
deviceThread.start() 
adapterThread.start() 
serverThread.start()


logger.debug('Device has been shuffled')
logger.info('Adapter has been started')
logger.error('Error connecting to server')


deviceThread.join() 
adapterThread.join()
serverThread.join()


