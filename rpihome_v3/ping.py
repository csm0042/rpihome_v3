#!/usr/bin/python3
""" ping.py:  Async ping function for a device at a given address
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
async def ping_device(device, logger):
    # Personal devices get ping'd to detect if they are on the network or not
    logger.debug(
        'Pinging device [%s] at [%s], original status [%s / %s]',
        device.name,
        device.address,
        device.status,
        device.last_seen)

    # Set ping command flags based upon operating system used
    if platform.system().lower() == "windows":
        ping_flags = "-n 1"
        logger.debug('Attempting to ping on Windows platform')
    else:
        ping_flags = "-c 1"
        logger.debug('Attempting to ping on Non-Windows platform')

    # Perform ping
    logger.debug('Performing ping to address [%s]', device.address)
    result = os.system("ping " + ping_flags + " " + device.address)
    logger.debug('Ping returned result [%s]', str(result))

    # evaluate result
    if result == 0:
        device = rpihome_v3.Device(
            device.name,
            device.devtype,
            device.address,
            'true',
            device.status_mem,
            str(datetime.datetime.now()),
            device.cmd,
            device.cmd_mem,
            device.rule
            )
    else:
        device = rpihome_v3.Device(
            device.name,
            device.devtype,
            device.address,
            'false',
            device.status_mem,
            device.last_seen,
            device.cmd,
            device.cmd_mem,
            device.rule
            )
    logger.debug(
        'Updating device status to [%s / %s]',
        device.status, device.last_seen)
    return device