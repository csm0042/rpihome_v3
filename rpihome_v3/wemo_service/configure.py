#!/usr/bin/python3
""" configure.py:
    Configuration helper functions used to set up this service
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import configparser
if __name__ == "__main__":
    import sys
    sys.path.append("..")
import wemo_service


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Config Function Def *********************************************************
def configure_logger(filename):
    # Define connection to configuration file
    config_file = configparser.ConfigParser()
    config_file.read(filename)
    # Set up application logging
    logger = wemo_service.setup_log_handlers(
        __file__,
        config_file['LOG FILES']['debug_log_file'],
        config_file['LOG FILES']['info_log_file'])
    # Return configured objects to main program
    return logger


# Obtain Credentials **********************************************************
def configure_server(filename, logger):
    # Define connection to configuration file
    config_file = configparser.ConfigParser()
    config_file.read(filename)
    # Read credential info from file
    try:
        address = config_file['SOCKET SERVER']['address']
        port = int(config_file['SOCKET SERVER']['port'])
        logger.debug('Address and port found: %s:%s', address, port)
    except:
        logger.error('No address or port configuration found')
        address = None
        port = 0
    # Return configured objects to main program
    return address, port


# Simple function test ********************************************************
if __name__ == "__main__":
    logger = configure_logger('config.ini')
    address, port = configure_server('config.ini', logger)
    print(address, ":", port)
