#!/usr/bin/python3
""" automation.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import datetime

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
        try:
            # Ping each device in-turn
            for index, device in enumerate(p_devices):
                logger.debug(
                    'Pinging device [%s] at [%s]',
                    device.name,
                    device.address)
                response = rpihome_v3.ping_device(device.address, logger)
                if response is True:
                    device = rpihome_v3.Pdevice(
                        device.name, device.address,
                        'true', str(datetime.datetime.now()))
                else:
                    device = rpihome_v3.Pdevice(
                        device.name, device.address,
                        'false', device.last_seen)
                p_devices[index] = device


            # Do not loop when status flag is false
            if loop is False:
                logger.debug('Breaking out of update_Pdevice_status loop')
                break
            # Otherwise wait a pre-determined time period, then re-run the task
            logger.debug(
                'Sleeping update_Pdevice_status task for 10 seconds before running again')
            await asyncio.sleep(10)
        except KeyboardInterrupt:
            logging.debug('Stopping update_Pdevice_status process loop')
            break


# Main event loop function ****************************************************
async def update_Adevice_status(a_devices, loop, logger):
    """ test """
    while True:
        try:
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
        except KeyboardInterrupt:
            logging.debug('Stopping update_Adevice_status process loop')
            break


# Main event loop function ****************************************************
async def update_Adevice_state(a_devices, p_devices, schedule, loop, logger):
    """ test """
    while True:
        try:
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
        except KeyboardInterrupt:
            logging.debug('Stopping update_Adevice_state process loop')
            break


def automate(a_devices, p_devices, logger):
    # Cycle through automation devices and execute rules
    logger.info('Called automate function')
    for index, device in enumerate(a_devices):

        # Check motion sensor(s)
        if device.devtype == 'motion_capture':
            if rpihome_v3.check_motion(device.address, logger) is True:
                logger.info('Motion sensed by device [%s]', device.name)

