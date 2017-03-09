#!/usr/bin/python3
""" configure.py:
    Configuration process for the RPiHome application.
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import collections
import copy
import configparser
from log_support import setup_log_handlers
from persistance import MySqlInterface


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
    logger = setup_log_handlers(
        __file__,
        config_file['LOG FILES']['debug_log_file'],
        config_file['LOG FILES']['info_log_file']
        )
    # Return configured objects to main program
    return logger


def configure_database(filename, logger):
    # Define connection to configuration file
    config_file = configparser.ConfigParser()
    config_file.read(filename)
    # Set up database connection
    database = MySqlInterface(
        host=config_file['DATABASE']['host'],
        port=config_file['DATABASE']['port'],
        schema=config_file['DATABASE']['schema'],
        user=config_file['DATABASE']['user'],
        password=config_file['DATABASE']['password']
        )
    logger.info('Database connection established to: %s', str(database))
    # Return configured objects to main program
    return database


def configure_pdevice(filename, logger):
    # Define connection to configuration file
    config_file = configparser.ConfigParser()
    config_file.read(filename)    
    # Create personal device list
    Pdevice = collections.namedtuple(
        'Pdevice', 'name, address, status, last_seen'
        )
    p_devices = []
    logger.info('Begining search for persona devices in config file')
    for i in range(1, 10, 1):
        try:
            if len(str(i)) == 1:
                device_id = 'device0' + str(i)
            elif len(str(i)) == 2:
                device_id = 'device' + str(i)
            device_name = config_file['PERSONAL_DEVICES'][device_id]
            pd_temp = Pdevice(device_name, '', '', '')
            p_devices.append(copy.copy(pd_temp))
            logger.info(
                'Device %s added to personal device list', device_name)
        except:
            pass
    logger.info('Completed personal device list: %s', str(p_devices))

    # Obtain addresses for found personal devices
    for index, device in enumerate(p_devices):
        pd_add = config_file['PERSONAL_DEVICE_ADDRESSES'][device.name]
        device = Pdevice(
            device.name,
            copy.copy(pd_add),
            device.status,
            device.last_seen)
        p_devices[index] = device
        logger.info(
            'Updated device [%s] record with address [%s]',
            device.name,
            pd_add
            )
    logger.info('Updated personal device list: %s', p_devices)
    # Return configured objects to main program
    return p_devices


def configure_adevice(filename, logger):
    # Define connection to configuration file
    config_file = configparser.ConfigParser()
    config_file.read(filename)    
    # Create automation device list
    Adevice = collections.namedtuple(
        'Adevice', 'name, address, status, last_seen'
        )
    a_devices = []
    logger.info('Begining search for automation devices in config file')
    for i in range(1, 50, 1):
        try:
            if len(str(i)) == 1:
                device_id = 'device0' + str(i)
            elif len(str(i)) == 2:
                device_id = 'device' + str(i)
            device_name = config_file['AUTOMATION_DEVICES'][device_id]
            ad_temp = Adevice(device_name, '', '', '')
            a_devices.append(copy.copy(ad_temp))
            logger.info(
                'Device %s added to automation device list', device_name)
        except:
            pass
    logger.info('Completed automation device list: %s', str(a_devices))

    # Obtain addresses for found automation devices
    for index, device in enumerate(a_devices):
        ad_add = config_file['AUTOMATION_DEVICE_ADDRESSES'][device.name]
        device = Adevice(
            device.name,
            copy.copy(ad_add),
            device.status,
            device.last_seen)
        a_devices[index] = device
        logger.info(
            'Updated device [%s] record with address [%s]',
            device.name,
            ad_add
            )
    logger.info('Updated automation device list: %s', a_devices)
    # Return configured objects to main program
    return a_devices
