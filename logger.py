# logger.py

### Notes:
# This file must be run in order to work correctly. 
# Once the file has been run, any configuration chnages made to this logger will be saved and anytime the logger is referenced, the configuration details are known.
# If changes are made to this file, altering the logger configuration, the logger will not automatically be updated and any logs created using this logger will not reflect changes.
# Therefore, this logger.py script must be run in the run.py file so the current configuration details will be registered
 
#TODO: Explore more logging settings and find out how to append a specific string to the log when a new log file is created. Find a way to pull the configuration settings for the logger object from a logger.config file that will be placed in the application folder.
import logging
import string
import json
import os

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
def configureLogger():
        
    DEFAULTS = {"level": "debug", 
                "filename": "Adapter_Log.log", 
                "filemode": "a", 
                "format": "%(asctime)s - %(levelname)s - %(message)s", 
                "datefmt": "%m/%d/%Y %H:%M:%S %p"
                }
    
    # Read the settings from the config file
    try:
        with open('logger_config.json','r') as f:
            settings = json.load(f)
    except FileNotFoundError:
        # Logger config file was not found. Create a new config file using the default settings
            with open('logger_config.json', 'w') as f:
                json.dump(DEFAULTS, f, indent=4)
                settings = DEFAULTS
        

    
    # Designate function variables for the settings from the file
    #TODO: Need to add exception handling for invalid inputs
    level = settings.get('level', 'info')
    filename = settings.get('filename', 'adapter_log.log')
    format = settings.get('format','%(asctime)s - [%(levelname)s] - %(message)s')
    datefmt = settings.get('datefmt','%m/%d/%Y %H:%M:%S %p')
    filemode = settings.get('filemode', 'a')

    # Create the logger
    logger = logging.getLogger('adapterLog')

    # Set the logging level
    try:
        logger.setLevel(level.upper())
    except ValueError:
        logger.warn(f'Invalid logging level: {level}. Setting default level to INFO.')
        logger.setLevel('INFO')

    # Create a file handler
    if not validateFileName(filename):
        filename = DEFAULTS['filename']
    try:
        file_handler = logging.FileHandler(filename, filemode)
    except ValueError:
        logger.warn(f'Invalid file mode: {filemode}. Setting default file mode to append.')
        filemode = DEFAULTS['filemode']
        file_handler = logging.FileHandler(filename, filemode)

    # Set the log format
    try:
        formatter = logging.Formatter(format, datefmt)
    except Exception:
        #TODO
        pass

    # Set the file handler's format
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    # Could possibly be condensed to this. Need to test.

    # logger = logging.basicConfig(level= level,
    #                          format= format,
    #                          datefmt= datefmt,
    #                          filename= filename,
    #                          filemode= filemode)

def logFileExists(lgr: logging.Logger) -> bool:
    filename = ""
    for handler in lgr.handlers:
        if isinstance(handler, logging.FileHandler):
            filename = handler.baseFilename

    if os.path.getsize(filename) == 0:
        # Log file has been created by FileHandler but has no content
        return True
    else:
        return False
    
def startNewLog(adapter):
    lgr = adapter.logger
    lgr.info('New log created.')
    lgr.info(f'Adapter Version: {adapter.version}')

def validateLevel(level: str):
    VALID_LOG_LEVELS = {'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}
    if level.upper() not in VALID_LOG_LEVELS:
        raise ValueError

def validateFileName(file_name: str):
    """
    Validates a file name based on the following criteria:
    - The file name must not be empty.
    - The file name must not contain any of the following characters: \ / : * ? " < > |
    - The file name must not start or end with a period.
    """
    if not file_name:
        return False
    if any(c in file_name for c in r'\/:*?"<>|'):
        return False
    if file_name.startswith('.') or file_name.endswith('.'):
        return False
    return True

if __name__ == '__main__':
    # logger.py executed as script
    configureLogger()

