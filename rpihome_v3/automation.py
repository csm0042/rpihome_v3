#!/usr/bin/python3
""" automation.py:
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


# Main event loop function ****************************************************
async def update_adevice_status(devices, loop, logger):
    """ test """
    while True:
        try:
            # Evaluate each device in turn
            for index, device in enumerate(devices):
                # Wemo devices are querried for the current state
                if device.devtype == "wemo_switch":
                    devices[index] = await wemo_status(devices[index], logger)
                await asyncio.sleep(2)

            # Do not loop when status flag is false
            if loop is False:
                logger.debug('Breaking out of update_device_status loop')
                break
            # Otherwise wait a pre-determined time period, then re-run the task
            logger.debug(
                'Sleeping update_device_status task for 10 seconds before running again')
            await asyncio.sleep(2)
        except KeyboardInterrupt:
            logging.debug('Stopping update_device_status process loop')
            break


async def update_pdevice_status(devices, loop, logger):
    """ test """
    while True:
        try:
            # Evaluate each device in turn
            for index, device in enumerate(devices):
                # Personal devices get ping'd to detect if they are on the network or not
                if device.devtype == 'personal':
                    devices[index] = await ping(devices[index], logger)

            # Do not loop when status flag is false
            if loop is False:
                logger.debug('Breaking out of update_device_status loop')
                break
            # Otherwise wait a pre-determined time period, then re-run the task
            logger.debug(
                'Sleeping update_device_status task for 10 seconds before running again')
            await asyncio.sleep(15)
        except KeyboardInterrupt:
            logging.debug('Stopping update_device_status process loop')
            break


async def ping(device, logger):
    # Personal devices get ping'd to detect if they are on the network or not
    logger.debug(
        'Pinging device [%s] at [%s], original status [%s / %s]',
        device.name,
        device.address,
        device.status,
        device.last_seen)
    response = await rpihome_v3.ping_device(device.address, logger)
    if response is True:
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


async def wemo_status(device, logger):
    # Wemo devices get a status query message sent to detect if they are
    # on the network or not and what their current state is
    logger.debug(
        'Querrying device [%s] at [%s], original status [%s / %s]',
        device.name,
        device.address,
        device.status,
        device.last_seen)
    device = await rpihome_v3.wemo_check_status(device, logger)
    logger.debug(
        'Updating device status to [%s / %s]',
        device.status, device.last_seen)
    return device
