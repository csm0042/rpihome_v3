#!/usr/bin/python3
""" tasks.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import copy
import datetime
import pywemo
from threading import Thread
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
@asyncio.coroutine
def update_adev_status(devices, wemo, loop, sleep, logger):
    """ test """
    logger.debug('Starting update personal device status task')
    while True:
        try:
            for index, device in enumerate(devices):
                if device.devtype == "wemo_switch":
                    devices[index] = yield from wemo.wemo_read_status(devices[index])
            # Do not loop when status flag is false
            if loop is False:
                logger.debug('Breaking out of update_device_status loop')
                break
            # Otherwise wait a pre-determined time period, then re-run the task
            logger.debug('Sleeping task for %s seconds', str(sleep))
            yield from asyncio.sleep(sleep)
        except KeyboardInterrupt:
            logging.debug(
                'Killing task')
            break
            break


# Update automation device status *********************************************
@asyncio.coroutine
def update_pdev_status(devices, loop, sleep, logger):
    """ test """
    logger.debug('Starting update personal device status task')
    while True:
        try:
            for index, device in enumerate(devices):
                if device.devtype == "personal":
                    logger.debug('Executing ping for device [%s]', device.name)
                    devices[index] = yield from rpihome_v3.ping_device(
                        devices[index], logger)
            # Do not loop when status flag is false
            if loop is False:
                logger.debug('Breaking out of update_device_status loop')
                break
            # Otherwise wait a pre-determined time period, then re-run the task
            logger.debug('Sleeping task for %s seconds', str(sleep))
            yield from asyncio.sleep(sleep)
        except KeyboardInterrupt:
            logging.debug(
                'Killing task')
            break
            break



# Update automation device status *********************************************
@asyncio.coroutine
async def update_mdev_status(devices, loop, sleep, logger):
    """ test """
    logger.debug('Starting update personal device status task')
    while True:
        try:
            for index, device in enumerate(devices):
                if device.devtype == "motion_capture":
                    devices[index] = yield from rpihome_v3.check_motion(
                        devices[index], logger)
            # Do not loop when status flag is false
            if loop is False:
                logger.debug('Breaking out of update_device_status loop')
                break
            # Otherwise wait a pre-determined time period, then re-run the task
            logger.debug('Sleeping task for %s seconds', str(sleep))
            yield from asyncio.sleep(sleep)
        except KeyboardInterrupt:
            logging.debug(
                'Killing task')
            break
            break


# Update automation device status *********************************************
@asyncio.coroutine
async def update_adev_cmd(devices, wemo, sun, sched, loop, sleep, logger):
    """ test """
    logger.debug('Starting update personal device status task')
    while True:
        try:
            for index, device in enumerate(devices):
                # Dusk to dawn rule
                if device.devtype == "dusk_to_dawn":
                    devices[index] = yield from rpihome_v3.dusk_to_dawn(
                        devices[index], wemo, sun, logger)
                # Schedule rule
                if device.devtype == "schedule":
                    devices[index] = yield from rpihome_v3.schedule(
                        devices[index], wemo, sched, logger)
            # Do not loop when status flag is false
            if loop is False:
                logger.debug('Breaking out of update_device_status loop')
                break
            # Otherwise wait a pre-determined time period, then re-run the task
            logger.debug('Sleeping task for %s seconds', str(sleep))
            yield from asyncio.sleep(sleep)
        except KeyboardInterrupt:
            logging.debug(
                'Killing task')
            break
            break
