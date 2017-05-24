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
def update_adev_status(devices, wemo, logger):
    """ test """
    threads = []
    for index, device in enumerate(devices):
        if device.devtype == "wemo_switch":
            threads.append(Thread(
                target=rpihome_v3.wemo_read_status,
                args=(devices[index], wemo, logger)))
            logger.debug('Spawning thread to check status of device [%s]',
                         device.name)
    for thread in threads:
        thread.start()
        logger.debug('Starting thread to check status of device [%s]',
                     device.name)


# Update automation device status *********************************************
def update_pdev_status(devices, logger):
    """ test """
    threads = []
    for index, device in enumerate(devices):
        if device.devtype == "personal":
            threads.append(Thread(
                target=rpihome_v3.ping_device,
                args=(devices[index], logger)))
            logger.debug('Spawning thread to check status of device [%s]',
                         device.name)
    for thread in threads:
        thread.start()
        logger.debug('Starting thread to check status of device [%s]',
                     device.name)


# Update automation device status *********************************************
def update_mdev_status(devices, logger):
    """ test """
    threads = []
    for index, device in enumerate(devices):
        if device.devtype == "motion_capture":
            threads.append(Thread(
                target=rpihome_v3.check_motion,
                args=(devices[index], logger)))
            logger.debug('Spawning thread to check status of device [%s]',
                         device.name)
    for thread in threads:
        thread.start()
        logger.debug('Starting thread to check status of device [%s]',
                     device.name)


# Update automation device status *********************************************
def update_adev_cmd(devices, wemo, cal, sched, logger):
    """ test """
    threads = []
    for index, device in enumerate(devices):
        # Dusk to dawn rule
        if device.devtype == "dusk_to_dawn":
            threads.append(Thread(
                target=rpihome_v3.dusk_to_dawn,
                args=(devices[index], wemo, sun, logger)))
            logger.debug('Spawning thread to check d-to-d rule for device [%s]',
                         device.name)
        # Schedule rule
        if device.devtype == "schedule":
            threads.append(Thread(
                target=rpihome_v3.schedule,
                args=(devices[index], wemo, sched, logger)))
            logger.debug('Spawning thread to check schedule rule for device [%s]',
                         device.name)
    for thread in threads:
        thread.start()
        logger.debug('Starting thread to check rule for device [%s]',
                     device.name)
                                    