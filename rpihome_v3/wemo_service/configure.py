#!/usr/bin/python3
""" configure.py:
    Configuration helper functions used to set up this service
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import configparser
import sys
if __name__ == "__main__":
    sys.path.append("..")
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
    log = helpers.setup_log_handlers(
        __file__,
        config_file['LOG FILES']['debug_log_file'],
        config_file['LOG FILES']['info_log_file'])
    # Return configured objects to main program
    return log


# Configure service addresses and ports ***************************************
def configure_servers(filename, log):
    # Define connection to configuration file
    config_file = configparser.ConfigParser()
    config_file.read(filename)
    # Create dict with all services defined in INI file
    service_addresses = {}
    for option in config_file.options('SERVICES'):
        service_addresses[option] = config_file['SERVICES'][option]
    # Return dict of configured addresses and ports to main program
    return service_addresses


# Configure message types *****************************************************
def configure_message_types(filename, log):
    # Define connection to configuration file
    config_file = configparser.ConfigParser()
    config_file.read(filename)
    # Create dict with all services defined in INI file
    message_types = {}
    for option in config_file.options('MESSAGE TYPES'):
        message_types[option] = config_file['MESSAGE TYPES'][option]
    # Return dict of configured addresses and ports to main program
    return message_types
