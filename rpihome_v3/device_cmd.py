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
async def update_adevice_cmd(devices, wemo, sun, loop, logger):
    """ test """
    sleep = 5
    while True:
        try:
            # Evaluate each device in turn
            for index, device in enumerate(devices):
                # Wemo devices are querried for the current state
                if device.rule == "dusk to dawn":
                    devices[index], wemo = await rpihome_v3.dusk_to_dawn(
                        devices[index], wemo, sun, logger)

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


# Dusk to dawn function *******************************************************
async def dusk_to_dawn(device, wemo, sun, logger):
    """ test """
    # Turn on light if after sunset or before sunrise and not already on
    if (datetime.datetime.now().time() < sun.sunrise(datetime.datetime.now(), -5) or
            datetime.datetime.now().time() >= sun.sunset(datetime.datetime.now(), -5)) and (
                device.cmd.lower() != 'on'):
        logger.info('Turning on [%s] based on dusk to dawn rule', device.name)
        device, wemo = await rpihome_v3.wemo_set_on(device, wemo, logger)
    # Turn off light if after sunrise and before sunset and currently on
    if (datetime.datetime.now().time() >= sun.sunrise(datetime.datetime.now(), -5) and
            datetime.datetime.now().time() < sun.sunset(datetime.datetime.now(), -5) and
            device.cmd.lower() != 'off'):
        logger.info('Turning off [%s] based on dusk to dawn rule', device.name)
        device, wemo = await rpihome_v3.wemo_set_off(device, wemo, logger)
    # Return updated list to calling routine
    return device, wemo
