#!/usr/bin/python3
""" device_cmd.py:
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


# Device cmd logic ************************************************************
async def update_adevice_cmd(devices, wemo, loop, logger):
    """ test """
    sleep = 5
    while True:
        try:
            # Evaluate each device in turn
            for index, device in enumerate(devices):
                # Wemo devices are querried for the current state
                if device.devtype == "wemo_switch":
                    devices[index], wemo = await rpihome_v3.wemo_read_status(
                        devices[index], wemo, logger)
                await asyncio.sleep(sleep)

            # Do not loop when status flag is false
            if loop is False:
                logger.debug('Breaking out of update_device_status loop')
                break
            # Otherwise wait a pre-determined time period, then re-run the task
            logger.debug(
                'Sleeping update automation device status task for '
                '%s seconds before running again', str(sleep))
            await asyncio.sleep(sleep)
        except KeyboardInterrupt:
            logging.debug(
                'Stopping update automation device status process loop')
            break
            break