#!/usr/bin/python3
""" configure.py:
    Configuration helper functions used to set up this service
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import configparser
import datetime
import sys
if __name__ == "__main__":
    sys.path.append("..")
import cal_service as service
import helpers


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
def configure_log(filename):
    # Define connection to configuration file
    config_file = configparser.ConfigParser()
    config_file.read(filename)
    # Set up application logging
    log = wemo_service.setup_log_handlers(
        __file__,
        config_file['LOG FILES']['debug_log_file'],
        config_file['LOG FILES']['info_log_file'])
    # Return configured objects to main program
    return log


# Configure service socket server *********************************************
def configure_server(filename, log):
    # Define connection to configuration file
    config_file = configparser.ConfigParser()
    config_file.read(filename)
    # Read credential info from file
    try:
        address = config_file['CAL SERVICE']['address']
        port = config_file['CAL SERVICE']['port']
        log.debug('Address and port found: %s:%s', address, port)
    except:
        log.error('No address or port configuration found')
        address = '0'
        port = '0'
    # Return configured objects to main program
    return address, port


# Configure service socket server *********************************************
def configure_automation_connection(filename, log):
    # Define connection to configuration file
    config_file = configparser.ConfigParser()
    config_file.read(filename)
    # Read credential info from file
    try:
        address = config_file['AUTOMATION SERVICE']['address']
        port = config_file['AUTOMATION SERVICE']['port']
        log.debug('Address and port found: %s:%s', address, port)
    except:
        log.error('No address or port configuration found')
        address = '0'
        port = '0'
    # Return configured objects to main program
    return address, port
