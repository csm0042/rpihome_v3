#!/usr/bin/python3
""" automation.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
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


# Main event loop function ****************************************************
async def update_Pdevice_status(p_devices, loop, logger):
    """ test """
    while True:
        for index, device in enumerate(p_devices):
            logger.debug(
                'Starting 2-second sleep to simulate status query for device: [%s]',
                device.name)
            await asyncio.sleep(2)
        if loop is False:
            logger.debug('Breaking out of update_Pdevice_status loop')
            break
        logger.debug(
            'Sleeping update_Pdevice_status task for 10 seconds before running again')
        await asyncio.sleep(10)


# Main event loop function ****************************************************
async def update_Adevice_status(a_devices, loop, logger):
    """ test """
    while True:
        for index, device in enumerate(a_devices):
            logger.debug(
                'Starting 2-second sleep to simulate status query for device: [%s]',
                device.name)
            await asyncio.sleep(2)
        if loop is False:
            logger.debug('Breaking out of update_Adevice_status loop')
            break
        logger.debug(
            'Sleeping update_Adevice_status task for 10 seconds before running again')
        await asyncio.sleep(2)


# Main event loop function ****************************************************
async def update_Adevice_state(a_devices, p_devices, schedule, loop, logger):
    """ test """
    while True:
        for index, device in enumerate(a_devices):
            logger.debug(
                'Starting 1/2-second sleep to simulate state-set for device: [%s]',
                device.name)
            await asyncio.sleep(0.5)
        if loop is False:
            logger.debug('Breaking out of update_Adevice_state loop')
            break
        logger.debug(
            'Sleeping update_Adevice_state task for 1 seconds before running again')
        await asyncio.sleep(1)


def automate(a_devices, p_devices, logger):
    # Cycle through automation devices and execute rules
    logger.info('Called automate function')
    for index, device in enumerate(a_devices):

        # Check motion sensor(s)
        if device.devtype == 'motion_capture':
            if rpihome_v3.check_motion(device.address, logger) is True:
                logger.info('Motion sensed by device [%s]', device.name)

