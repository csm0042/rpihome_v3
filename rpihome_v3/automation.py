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
async def update_device_status(devices, loop, logger):
    """ test """
    while True:
        try:
            # Evaluate each device in turn
            for index, device in enumerate(devices):
                # Personal devices get ping'd to detect if they are on the network or not
                if device.devtype == 'personal':
                    logger.debug(
                        'Pinging device [%s] at [%s], original status [%s / %s]',
                        device.name,
                        device.address,
                        device.status,
                        device.last_seen)
                    response = await rpihome_v3.ping_device(device.address, logger)
                    if response is True:
                        devices[index] = rpihome_v3.Device(
                            device.name,
                            device.devtype,
                            device.address,
                            'true',
                            device.status_mem,
                            str(datetime.datetime.now()))
                    else:
                        devices[index] = rpihome_v3.Device(
                            device.name,
                            device.devtype,
                            device.address,
                            'false',
                            device.status_mem,
                            device.last_seen)
                    logger.debug(
                        'Updating device status to [%s / %s]',
                        device.status, device.last_seen)

                # Wemo devices are querried for the current state
                elif device.devtype == "wemo_switch":
                    pass

            # Do not loop when status flag is false
            if loop is False:
                logger.debug('Breaking out of update_device_status loop')
                break
            # Otherwise wait a pre-determined time period, then re-run the task
            logger.debug(
                'Sleeping update_device_status task for 10 seconds before running again')
            await asyncio.sleep(10)
        except KeyboardInterrupt:
            logging.debug('Stopping update_device_status process loop')
            break





def automate(a_devices, p_devices, logger):
    # Cycle through automation devices and execute rules
    logger.info('Called automate function')
    for index, device in enumerate(a_devices):

        # Check motion sensor(s)
        if device.devtype == 'motion_capture':
            if rpihome_v3.check_motion(device.address, logger) is True:
                logger.info('Motion sensed by device [%s]', device.name)

