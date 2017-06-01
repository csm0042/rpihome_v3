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
def update_adev_status(devices, wemo, loop, executor, sleep, logger):
    """ test """
    logger.debug('Starting update personal device status task')
    while True:
        try:
            for index, device in enumerate(devices):
                if device.devtype == "wemo_switch":
                    logger.debug(
                        'Before status check: %s, %s, %s, %s, %s, %s, %s',
                        device.name, device.devtype, device.address,
                        device.status, device.last_seen, device.cmd, device.rule)
                    yield from loop.run_in_executor(
                        executor,
                        wemo.wemo_read_status,
                        devices[index]
                        )
                    logger.debug(
                        'After status check: %s, %s, %s, %s, %s, %s, %s',
                        device.name, device.devtype, device.address,
                        device.status, device.last_seen, device.cmd, device.rule)
                    logger.debug('finished processing device [%s]', device.name)
            # Wait a pre-determined time period, then re-run the task
            logger.debug('Sleeping task for %s seconds', str(sleep))
            yield from asyncio.sleep(sleep)
        except KeyboardInterrupt:
            logger.debug(
                'Killing task')
            break


# Update automation device status *********************************************
@asyncio.coroutine
def update_pdev_status(devices, loop, executor, sleep, logger):
    """ test """
    logger.debug('Starting update personal device status task')
    while True:
        try:
            for index, device in enumerate(devices):
                if device.devtype == "personal":
                    logger.debug('Executing ping for device [%s]', device.name)
                    yield from loop.run_in_executor(
                        executor,
                        rpihome_v3.ping_device,
                        devices[index], logger
                    )
            # Wait a pre-determined time period, then re-run the task
            logger.debug('Sleeping task for %s seconds', str(sleep))
            yield from asyncio.sleep(sleep)
        except KeyboardInterrupt:
            logger.debug(
                'Killing task')
            break


# Update automation device status *********************************************
@asyncio.coroutine
def update_mdev_status(devices, loop, executor, sleep, logger):
    """ test """
    logger.debug('Starting update personal device status task')
    while True:
        try:
            for index, device in enumerate(devices):
                if device.devtype == "motion_capture":
                    yield from loop.run_in_executor(
                        executor,
                        rpihome_v3.check_motion,
                        devices[index], logger
                    )
            # Wwait a pre-determined time period, then re-run the task
            logger.debug('Sleeping task for %s seconds', str(sleep))
            yield from asyncio.sleep(sleep)
        except KeyboardInterrupt:
            logger.debug(
                'Killing task')
            break


# Update automation device status *********************************************
@asyncio.coroutine
def update_adev_cmd(devices, wemo, sun, sched, loop, executor, sleep, logger):
    """ test """
    logger.debug('Starting update personal device status task')
    while True:
        try:
            for index, device in enumerate(devices):
                # Dusk to dawn rule
                if device.devtype == "dusk_to_dawn":
                    yield from rpihome_v3.dusk_to_dawn(
                        devices[index], wemo, sun, logger)
                # Schedule rule
                if device.devtype == "schedule":
                    yield from loop.run_in_executor(
                        executor,
                        rpihome_v3.schedule,
                        devices[index], wemo, sched, logger
                    )
            # Wait a pre-determined time period, then re-run the task
            logger.debug('Sleeping task for %s seconds', str(sleep))
            yield from asyncio.sleep(sleep)
        except KeyboardInterrupt:
            logger.debug(
                'Killing task')
            break


# Update automation device status *********************************************
@asyncio.coroutine
def update_database(database, devices, loop, executor, sleep, logger):
    """ test """
    logger.debug('Starting update personal device status task')
    while True:
        try:
            for index, device in enumerate(devices):
                # Log changes of state in automation device status
                if device.status != device.status_mem:
                    yield from loop.run_in_executor(
                        executor,
                        rpihome_v3.insert_record,
                        database, devices[index], logger
                        )
                    device.status_mem = copy.copy(device.status)
            # Wait a pre-determined time period, then re-run the task
            logger.debug('Sleeping task for %s seconds', str(sleep))
            yield from asyncio.sleep(sleep)
        except KeyboardInterrupt:
            logger.debug(
                'Killing task')
            break
