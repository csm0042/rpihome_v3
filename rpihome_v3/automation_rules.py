#!/usr/bin/python3
""" device_cmd.py:
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


# Dusk to dawn function *******************************************************
async def dusk_to_dawn(device, wemo, sun, logger):
    """ test """
    # Turn on light if after sunset or before sunrise and not already on
    if ((datetime.datetime.now().time() < sun.sunrise()
         or
         datetime.datetime.now().time() >= sun.sunset())
            and
            device.cmd.lower() != 'on'):
        logger.info('Turning on [%s] based on dusk to dawn rule', device.name)
        device, wemo = await rpihome_v3.wemo_set_on(device, wemo, logger)
    # Turn off light if after sunrise and before sunset and currently on
    if ((datetime.datetime.now().time() >= sun.sunrise()
         and
         datetime.datetime.now().time() < sun.sunset())
            and
            device.cmd.lower() != 'off'):
        logger.info('Turning off [%s] based on dusk to dawn rule', device.name)
        device, wemo = await rpihome_v3.wemo_set_off(device, wemo, logger)
    # Return updated list to calling routine
    return device, wemo