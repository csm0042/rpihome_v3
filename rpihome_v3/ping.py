#!/usr/bin/python3
""" device_ping.py:   
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import collections
import datetime
import logging
import os
import platform
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


# Ping Function ***************************************************************
@asyncio.coroutine
def ping_devices(device_list, logger=None):
    """ Pings every device in a list periodically as defined by sleeptime
    input variable.  Each device is ping'd using an individual coroutine
    so nothing blocks the main thread """

    # Configure local logging
    logger = logger or logging.getLogger(__name__)

    # Ping each device in list in turn and update their record accordingly
    for index, device in enumerate(device_list):
        logger.debug('Pinging device [%s] at [%s]',
                     device.name, device.address)
        result = yield from ping_device(device.address, logger)
        logger.debug('Updating device [%s] status to [%s]',
                     device.name, str(result))
        device = rpihome_v3.Pdevice(
            device.name, device.address,
            str(result), str(datetime.datetime.now())
            )
        logger.debug('Updating record in personal device list')
        device_list[index] = device


def ping_device(address, logger=None):
    """ Pings a device with a given address and returns a True/False based
    upon whether or not the device responded  """
    # Configure local logging
    logger = logger or logging.getLogger(__name__)

    # Set ping command flags based upon operating system used
    if platform.system().lower() == "windows":
        ping_flags = "-n 1"
        logger.debug('Attempting to ping on Windows platform')
    else:
        ping_flags = "-c 1"
        logger.debug('Attempting to ping on Non-Windows platform')

    # Perform ping
    logger.debug('Performing ping to address [%s]', address)
    result = os.system("ping " + ping_flags + " " + address)
    logger.debug('Ping returned result [%s]', str(result))

    # evaluate result
    if result == 0:
        return True
    else:
        return False



