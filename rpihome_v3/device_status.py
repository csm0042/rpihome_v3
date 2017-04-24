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
async def update_adevice_status(devices, wemo, loop, logger):
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


# Update motion sensor status *************************************************
async def update_mdevice_status(devices, loop, logger):
    """ test """
    sleep = 2
    while True:
        try:
            # Evaluate each device in turn
            for index, device in enumerate(devices):
                # Personal devices get ping'd to detect if they are on
                # the network or not
                if device.devtype == 'motion_capture':
                    devices[index] = await rpihome_v3.check_motion(
                        devices[index], logger)

            # Do not loop when status flag is false
            if loop is False:
                logger.debug('Breaking out of update_motion_status loop')
                break
            # Otherwise wait a pre-determined time period, then re-run the task
            logger.debug(
                'Sleeping update motion device status task for '
                '%s seconds before running again', str(sleep))
            await asyncio.sleep(sleep)
        except KeyboardInterrupt:
            logging.debug(
                'Stopping update motion device status process loop')
            break
            break


# Update personal device status ***********************************************
async def update_pdevice_status(devices, loop, logger):
    """ test """
    sleep = 15
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
                'Sleeping update personal device status task for '
                '%s seconds before running again', str(sleep))
            await asyncio.sleep(sleep)
        except KeyboardInterrupt:
            logging.debug(
                'Stopping update personal device status process loop')
            break
            break


# Update enviro device status *************************************************
async def update_enviro_status(devices, nest, credentials, loop, logger):
    """ test """
    sleep = 300
    while True:
        try:
            # Evaluate each device in turn
            for index, device in enumerate(devices):
                # Personal devices get ping'd to detect if they are on
                # the network or not
                if device.devtype == 'nest':
                    devices[index], nest = await rpihome_v3.current_conditions(
                        devices[index], nest, credentials, logger)

            # Do not loop when status flag is false
            if loop is False:
                logger.debug('Breaking out of update_enviro_status loop')
                break
            # Otherwise wait a pre-determined time period, then re-run the task
            logger.debug(
                'Sleeping update enviro status task for '
                '%s seconds before running again', str(sleep))
            await asyncio.sleep(sleep)
        except KeyboardInterrupt:
            logging.debug(
                'Stopping update enviro status process loop')
            break
            break
