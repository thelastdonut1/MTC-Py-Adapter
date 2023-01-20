# logger.py

#TODO: Explore more logging settings and find out how to append a specific string to the log when a new log file is created. Find a way to pull the configuration settings for the logger object from a logger.config file that will be placed in the application folder.
import logging
'''
LOGGER LEVELS:
-------------------
DEBUG:
Detailed information, typically of interest only when diagnosing problems.

INFO:
Confirmation that things are working as expected.

WARNING:
An indication that something unexpected happened, or indicative of some problem in the near future (e.g. disk space low). The software is still working as expected.

ERROR:
Due to a more serious problem, the software has not been able to perform some function.

CRITICAL:
A serious error, indicating that the program itself may be unable to continue running.
'''
# Create the logger
logger = logging.getLogger('adapterLog')

# Set the logging level
logger.setLevel(logging.INFO)

# Create a file handler
file_handler = logging.FileHandler('Adapter_Log.log')

# Set the log format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Set the file handler's format
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

