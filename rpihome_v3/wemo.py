#!/usr/bin/python3
""" wemo.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import copy
import datetime
import pywemo
import rpihome_v3


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Wemo discover / connect function ********************************************
async def wemo_discover(device, logger):
    # Attempt to discover wemo device
    try:
        wemo_device = None
        wemo_device = pywemo.discovery.device_from_description(
            ('http://%s:%i/setup.xml',
             device.address,
             pywemo.ouimeaux_device.probe_wemo(device.address)
            ),
            None)
        return wemo_device
    except:
        return None


# Wemo status check function **************************************************
async def wemo_read_status(device, wemo_list, logger):
    # Wemo devices get a status query message sent to detect if they are
    # on the network or not and what their current state is
    logger.debug(
        'Querrying device [%s] at [%s], original status [%s / %s]',
        device.name,
        device.address,
        device.status,
        device.last_seen)

    # Check if device is already in the list of known wemo devices
    result = next(
        (index for index, wemodev in enumerate(wemo_list)
         if wemodev.name == device.name), None)

    # Point to existing list record or recently discovered device
    if result == None:
        wemo_device = await wemo_discover(device, logger)
    else:
        wemo_device = wemo_list[result]

    # Perform status query
    if wemo_device is not None:
        status = str(wemo_device.get_state(force_update=True))
        logger.debug(
            'Wemo device [%s] found with status [%s]',
            device.name, status)
        # Re-define device record based on response from status query
        device = rpihome_v3.Device(
            device.name, device.devtype, device.address,
            status, device.status_mem, str(datetime.datetime.now()),
            device.cmd, device.cmd_mem, device.rule)
        # If device was not previously in wemo list, add it for next time
        if result == None:
            wemo_list.append(copy.copy(wemo_device))
    else:
        status = 'offline'
        logger.debug(
            'Wemo device [%s] discovery failed.  Status set to [%s]',
            device.name, status)
        device = rpihome_v3.Device(
            device.name, device.devtype, device.address,
            status, device.status_mem, str(datetime.datetime.now()),
            device.cmd, device.cmd_mem, device.rule)
    return device, wemo_list
