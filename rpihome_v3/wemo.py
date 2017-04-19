#!/usr/bin/python3
""" wemo.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
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


# Wemo status check function **************************************************
async def wemo_status(device, logger):
    # Wemo devices get a status query message sent to detect if they are
    # on the network or not and what their current state is
    logger.debug(
        'Querrying device [%s] at [%s], original status [%s / %s]',
        device.name,
        device.address,
        device.status,
        device.last_seen)

    # Attempt to discover, then query state of wemo device
    try:
        wemo_device = None
        wemo_device = pywemo.discovery.device_from_description(
            ('http://%s:%i/setup.xml',
             device.address,
             pywemo.ouimeaux_device.probe_wemo(device.address)
            ),
            None)
        if wemo_device is not None:
            status = str(wemo_device.get_state(force_update=True))
            logger.debug(
                'Wemo device [%s] found with status [%s]',
                device.name, status)
            device = rpihome_v3.Device(
                device.name, device.devtype, device.address,
                status, device.status_mem, str(datetime.datetime.now()),
                device.cmd, device.cmd_mem, device.rule)
        else:
            status = 'offline'
            logger.debug(
                'Wemo device [%s] discovery failed.  Status set to [%s]',
                device.name, status)
            device = rpihome_v3.Device(
                device.name, device.devtype, device.address,
                status, device.status_mem, str(datetime.datetime.now()),
                device.cmd, device.cmd_mem, device.rule)
    except:
        status = 'offline'
        logger.debug('Could not find device [%s] on network')
        device = rpihome_v3.Device(
            device.name, device.devtype, device.address,
            status, device.status_mem, device.last_seen,
            device.cmd, device.cmd_mem, device.rule)
    return device
