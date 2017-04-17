#!/usr/bin/python3
""" configure.py:
    Configuration process for the RPiHome application.
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import copy
import configparser
import typing
import mysql.connector
import mysql.connector.errorcode as errorcode
from .log_support import setup_log_handlers
import rpihome_v3


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
    try:
        database = mysql.connector.connect(
            host=config_file['DATABASE']['host'],
            port=config_file['DATABASE']['port'],
            database=config_file['DATABASE']['schema'],
            user=config_file['DATABASE']['user'],
            password=config_file['DATABASE']['password'])
        logger.debug("Successfully connected to database")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            database = None
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            database = None
        else:
            database = None
        pass
        logger.debug("Could not connect to database")

    # Return configured objects to main program
    return database


def configure_Pdevice(filename, logger):
    # Define connection to configuration file
    config_file = configparser.ConfigParser()
    config_file.read(filename)

    p_devices = []
    logger.debug('Begining search for persona devices in config file')
    for i in range(1, 10, 1):
        try:
            if len(str(i)) == 1:
                device_id = 'device0' + str(i)
            elif len(str(i)) == 2:
                device_id = 'device' + str(i)
            device_name = config_file['PERSONAL_DEVICES'][device_id]
            pd_temp = rpihome_v3.Pdevice(device_name, '', '', '', '')
            p_devices.append(copy.copy(pd_temp))
            logger.debug(
                'Device %s added to personal device list', device_name)
        except:
            pass
    logger.debug('Completed personal device list: %s', str(p_devices))

    # Obtain addresses for found personal devices
    for index, device in enumerate(p_devices):
        pd_add = config_file['PERSONAL_DEVICE_ADDRESSES'][device.name]
        device = rpihome_v3.Pdevice(
            device.name,
            copy.copy(pd_add),
            device.status,
            device.status_mem,
            device.last_seen)
        p_devices[index] = device
        logger.debug(
            'Updated device [%s] record with address [%s]',
            device.name,
            pd_add
            )
    logger.debug('Updated personal device list: %s', p_devices)
    # Return configured objects to main program
    return p_devices


def configure_Adevice(filename, logger):
    # Define connection to configuration file
    config_file = configparser.ConfigParser()
    config_file.read(filename)

    a_devices = []
    logger.debug('Begining search for automation devices in config file')
    for i in range(1, 50, 1):
        try:
            if len(str(i)) == 1:
                device_id = 'device0' + str(i)
            elif len(str(i)) == 2:
                device_id = 'device' + str(i)
            device_name = config_file['AUTOMATION_DEVICES'][device_id]
            ad_temp = rpihome_v3.Adevice(device_name, '', '', '', '', '')
            a_devices.append(copy.copy(ad_temp))
            logger.debug(
                'Device %s added to automation device list', device_name)
        except:
            pass
    logger.debug('Completed automation device list: %s', str(a_devices))

    # Obtain device type for found automation devices
    for index, device in enumerate(a_devices):
        ty_add = config_file['AUTOMATION_DEVICE_TYPES'][device.name]
        device = rpihome_v3.Adevice(
            device.name,
            copy.copy(ty_add),
            device.address,
            device.status,
            device.status_mem,
            device.last_seen)
        a_devices[index] = device
        logger.debug(
            'Updated device [%s] record with device type [%s]',
            device.name,
            ty_add
            )
    logger.debug('Updated automation device list: %s', a_devices)

    # Obtain addresses for found automation devices
    for index, device in enumerate(a_devices):
        ad_add = config_file['AUTOMATION_DEVICE_ADDRESSES'][device.name]
        device = rpihome_v3.Adevice(
            device.name,
            device.devtype,
            copy.copy(ad_add),
            'false',
            device.status_mem,
            device.last_seen)
        a_devices[index] = device
        logger.debug(
            'Updated device [%s] record with address [%s]',
            device.name,
            ad_add
            )
    logger.debug('Updated automation device list: %s', a_devices)
    # Return configured objects to main program
    return a_devices


def configure_calendar(filename, logger):
    # Define connection to configuration file
    config_file = configparser.ConfigParser()
    config_file.read(filename)
    # Read credential info from file
    credentials = rpihome_v3.Credentials(
        config_file['CALENDAR']['username'],
        config_file['CALENDAR']['password'])
    logger.debug('Credentails obtained from INI file')
    # Return configured objects to main program
    return credentials


def configure_all(filename):
    """ Gather application configuration data from config.ini file """
    logger = configure_logger(filename)
    database = configure_database(filename, logger)
    p_devices = configure_Pdevice(filename, logger)
    a_devices = configure_Adevice(filename, logger)
    credentials = configure_calendar(filename, logger)
    logger.debug('Finished call to configuration function')
    # Return results to main program
    return (logger, database, p_devices, a_devices, credentials)
