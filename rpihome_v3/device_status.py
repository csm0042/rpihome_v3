#!/usr/bin/python3
""" status_updates.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import copy
import datetime
import pywemo
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


# Update automation device status *********************************************
async def update_adevice_status(devices, loop, logger):
    """ test """
    while True:
        try:
            # Evaluate each device in turn
            for index, device in enumerate(devices):
                # Wemo devices are querried for the current state
                if device.devtype == "wemo_switch":
                    devices[index] = await rpihome_v3.wemo_status(
                        devices[index], logger)
                await asyncio.sleep(2)

            # Do not loop when status flag is false
            if loop is False:
                logger.debug('Breaking out of update_device_status loop')
                break
            # Otherwise wait a pre-determined time period, then re-run the task
            logger.debug(
                'Sleeping update_device_status task for '
                '10 seconds before running again')
            await asyncio.sleep(2)
        except KeyboardInterrupt:
            logging.debug('Stopping update_device_status process loop')
            break
            break


# Update personal device status ***********************************************
async def update_pdevice_status(devices, loop, logger):
    """ test """
    while True:
        try:
            # Evaluate each device in turn
            for index, device in enumerate(devices):
                # Personal devices get ping'd to detect if they are on
                # the network or not
                if device.devtype == 'personal':
                    devices[index] = await rpihome_v3.ping_device(
                        devices[index], logger)

            # Do not loop when status flag is false
            if loop is False:
                logger.debug('Breaking out of update_device_status loop')
                break
            # Otherwise wait a pre-determined time period, then re-run the task
            logger.debug(
                'Sleeping update_device_status task for '
                '10 seconds before running again')
            await asyncio.sleep(15)
        except KeyboardInterrupt:
            logging.debug('Stopping update_device_status process loop')
            break
            break
