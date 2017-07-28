#!/usr/bin/python3
""" configure.py:
    Configuration process for the RPiHome application.
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import configparser
import datetime
import sys
if __name__ == "__main__":
    sys.path.append("..")
import automation_service as service
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


# Configure service socket server *********************************************
def configure_server(filename, log):
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


# Configure service socket server *********************************************
def configure_db_connection(filename, log):
    # Define connection to configuration file
    config_file = configparser.ConfigParser()
    config_file.read(filename)
    # Read credential info from file
    try:
        address = config_file['PERSISTANCE SERVICE']['address']
        port = config_file['PERSISTANCE SERVICE']['port']
        log.debug('Address and port found: %s:%s', address, port)
    except:
        log.error('No address or port configuration found')
        address = '0'
        port = '0'
    # Return configured objects to main program
    return address, port


# Configure service socket server *********************************************
def configure_wemo_connection(filename, log):
    # Define connection to configuration file
    config_file = configparser.ConfigParser()
    config_file.read(filename)
    # Read credential info from file
    try:
        address = config_file['WEMO SERVICE']['address']
        port = config_file['WEMO SERVICE']['port']
        log.debug('Address and port found: %s:%s', address, port)
    except:
        log.error('No address or port configuration found')
        address = '0'
        port = '0'
    # Return configured objects to main program
    return address, port


# Configure service socket server *********************************************
def configure_cal_connection(filename, log):
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


# Config Location *************************************************************
def configure_location(filename, log):
    # Define connection to configuration file
    config_file = configparser.ConfigParser()
    config_file.read(filename)
    latitude = float(config_file['LOCATION']['latitude'])
    longitude = float(config_file['LOCATION']['longitude'])
    # Return configured objects to main program
    return latitude, longitude


# Config Automation Device List Function **************************************
def configure_devices(filename, log):
    # Define connection to configuration file
    config_file = configparser.ConfigParser()
    config_file.read(filename)
    # Create list of automation devices defined in config.ini file
    devices = []
    log.debug('Begining search for device configuration in config file')
    device_num = int(config_file['DEVICES']['device_num']) + 1
    log.debug('Importing configuration for %s devices', str(device_num))
    for i in range(1, device_num, 1):
        try:
            if len(str(i)) == 1:
                log.debug('Single digit device ID number')
                device_id = 'device0' + str(i)
            elif len(str(i)) == 2:
                log.debug('Double digit device ID number')
                device_id = 'device' + str(i)
            devices.append(
                helpers.Device(
                    name=config_file['DEVICES'][device_id + '_name'],
                    devtype=config_file['DEVICES'][device_id + '_devtype'],
                    address=config_file['DEVICES'][device_id + '_address'],
                    last_seen=datetime.datetime.now(),
                    rule=config_file['DEVICES'][device_id + '_rule']))
            log.debug('Device %s added to automation device list',
                      config_file['DEVICES'][device_id + '_name'])
        except:
            pass
    log.debug('Completed automation device list:')
    for device in devices:
        log.debug(
            '%s, %s, %s, %s, %s, %s, %s',
            device.name, device.devtype, device.address,
            device.status, device.last_seen, device.cmd, device.rule)
    # Return configured objects to main program
    return devices
