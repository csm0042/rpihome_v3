#!/usr/bin/python3
""" tasks.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import copy
import logging
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
def update_adev_status(devices, wemo, loop, executor, sleep, logger, shutdown):
    """ test """
    # Configure logger
    logger = logger or logging.getLogger(__name__)
    logger.debug('Starting update personal device status task')
    while True:
        try:
            for index, device in enumerate(devices):
                if device.devtype == "wemo_switch":
                    logger.debug('Checking status of device [%s]', device.name)
                    yield from loop.run_in_executor(
                        executor,
                        wemo.read_status,
                        devices[index])
            # Wait a pre-determined time period, then re-run the task
            logger.debug('Sleeping task for %s seconds', str(sleep))
            yield from asyncio.sleep(sleep)
        except KeyboardInterrupt:
            logger.debug('Killing task')
            break
        if shutdown:
            break


# Update automation device status *********************************************
@asyncio.coroutine
def update_pdev_status(devices, loop, executor, sleep, logger, shutdown):
    """ test """
    # Configure logger
    logger = logger or logging.getLogger(__name__)
    logger.debug('Starting update personal device status task')
    while True:
        try:
            for index, device in enumerate(devices):
                if device.devtype == "personal":
                    logger.debug('Executing ping for device [%s]', device.name)
                    yield from loop.run_in_executor(
                        executor,
                        rpihome_v3.ping_device,
                        devices[index], logger)
            # Wait a pre-determined time period, then re-run the task
            logger.debug('Sleeping task for %s seconds', str(sleep))
            yield from asyncio.sleep(sleep)
        except KeyboardInterrupt:
            logger.debug('Killing task')
            break
        if shutdown:
            break


# Update automation device status *********************************************
@asyncio.coroutine
def update_mdev_status(devices, loop, executor, sleep, logger, shutdown):
    """ test """
    # Configure logger
    logger = logger or logging.getLogger(__name__)
    logger.debug('Starting update personal device status task')
    while True:
        try:
            for index, device in enumerate(devices):
                if device.devtype == "motion_capture":
                    yield from loop.run_in_executor(
                        executor,
                        rpihome_v3.check_motion,
                        devices[index], logger)
            # Wwait a pre-determined time period, then re-run the task
            logger.debug('Sleeping task for %s seconds', str(sleep))
            yield from asyncio.sleep(sleep)
        except KeyboardInterrupt:
            logger.debug('Killing task')
            break
        if shutdown:
            break


# Update automation device status *********************************************
@asyncio.coroutine
def update_adev_cmd(devices, wemo, sun, sched, loop, executor, sleep, logger, shutdown):
    """ test """
    # Configure logger
    logger = logger or logging.getLogger(__name__)
    logger.debug('Starting update personal device status task')
    while True:
        try:
            for index, device in enumerate(devices):
                # Dusk to dawn rule
                if device.devtype == "dusk_to_dawn":
                    yield from loop.run_in_executor(
                        executor,
                        rpihome_v3.dusk_to_dawn,
                        devices[index], wemo, sun, logger)
                # Schedule rule
                if device.devtype == "schedule":
                    yield from loop.run_in_executor(
                        executor,
                        rpihome_v3.schedule,
                        devices[index], wemo, sched, logger)
            # Wait a pre-determined time period, then re-run the task
            logger.debug('Sleeping task for %s seconds', str(sleep))
            yield from asyncio.sleep(sleep)
        except KeyboardInterrupt:
            logger.debug('Killing task')
            break
        if shutdown:
            break


# Update automation device status *********************************************
@asyncio.coroutine
def update_database(database, devices, loop, executor, sleep, logger, shutdown):
    """ test """
    # Configure logger
    logger = logger or logging.getLogger(__name__)
    logger.debug('Starting update personal device status task')
    while True:
        try:
            for index, device in enumerate(devices):
                # Log changes of state in automation device status
                if device.status != device.status_mem:
                    yield from loop.run_in_executor(
                        executor,
                        rpihome_v3.insert_record,
                        database, devices[index], logger)
                    device.status_mem = copy.copy(device.status)
            # Wait a pre-determined time period, then re-run the task
            logger.debug('Sleeping task for %s seconds', str(sleep))
            yield from asyncio.sleep(sleep)
        except KeyboardInterrupt:
            logger.debug('Killing task')
            break
        if shutdown:
            break


# Update automation device status *********************************************
@asyncio.coroutine
def update_commands(database, devices, loop, executor, sleep, logger, shutdown):
    """ test """
    # Configure logger
    logger = logger or logging.getLogger(__name__)
    logger.debug('Starting update personal device status task')
    while True:
        try:
            # Query pending commands from database
            pending_cmds = yield from loop.run_in_executor(
                executor,
                rpihome_v3.query_cmds,
                database, logger)
            # Check if any pending commands were returned
            if len(pending_cmds) > 0:
                # Cycle through pending command list and process
                for index, cmd in enumerate(pending_cmds):
                    # Search for matching device, then process command
                    for device in devices:
                        if device.name == pending_cmds.name:
                            # do something
                            pass
                    # Perform update query to database to mark command as "sent"
                    yield from loop.run_in_executor(
                        executor,
                        rpihome_v3.update_record,
                        database, record, logger)

            # Wait a pre-determined time period, then re-run the task
            logger.debug('Sleeping task for %s seconds', str(sleep))
            yield from asyncio.sleep(sleep)
        except KeyboardInterrupt:
            logger.debug('Killing task')
            break
        if shutdown:
            break


@asyncio.coroutine
def update_db_cmd(database, devices, wemo, loop, executor, sleep, logger, shutdown):
    """ test """
    # Configure logger
    logger = logger or logging.getLogger(__name__)
    logger.debug('update_db_cmd function called')
    while True:
        try:
            cmd_list = rpihome_v3.query_command(database, logger)
            for cmd in cmd_list:
                if cmd.name in devices.name:
                    

            for index, device in enumerate(devices):
                if device.devtype == "wemo_switch":
                    logger.debug('Checking status of device [%s]', device.name)
                    yield from loop.run_in_executor(
                        executor,
                        wemo.read_status,
                        devices[index])
            # Wait a pre-determined time period, then re-run the task
            logger.debug('Sleeping task for %s seconds', str(sleep))
            yield from asyncio.sleep(sleep)
        except KeyboardInterrupt:
            logger.debug('Killing task')
            break
        if shutdown:
            break