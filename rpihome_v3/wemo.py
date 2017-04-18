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
async def wemo_check_status(device, logger):
    """ Discovery and status query for wemo device """
    try:
        wemo_device = pywemo.discovery.device_from_description(
            ('http://%s:%i/setup.xml',
             device.address, pywemo.ouimeaux_device.probe_wemo(device.address)
            ),
            None)
        status = str(wemo_device.get_state(force_update=True))
        logger.debug(
            'Wemo device [%s] found with status [%s]', device.name, status)
        return rpihome_v3.Device(
            device.name, device.devtype, device.address,
            status, device.status_mem, str(datetime.datetime.now()),
            device.cmd, device.cmd_mem, device.rule)
    except:
        logger.debug('Could not find device [%s] on network')
        return rpihome_v3.Device(
            device.name, device.devtype, device.address,
            'offline', device.status_mem, device.last_seen,
            device.cmd, device.cmd_mem, device.rule)
