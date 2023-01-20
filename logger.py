
import logging

# Create the logger
logger = logging.getLogger('myLogger')

# Set the logging level
logger.setLevel(logging.DEBUG)

# Specify the path

# Create a file handler
file_handler = logging.FileHandler('myLogFile.log')

# Set the log format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Set the file handler's format
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

