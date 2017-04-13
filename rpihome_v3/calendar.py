#!/usr/bin/python3
""" calendar.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import datetime
import logging
import typing

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
async def update_schedule(credentials, loop, logger):
    """ queries google calendar and returns list of items for current week """
    while True:
        logger.debug('Starting 5-second sleep to simulate schedule lookup')
        await asyncio.sleep(5)
        schedule = (1, 2, 3, 4, 5)
        if loop is False:
            logger.debug('Breaking out of update schedule loop')
            break
        logger.debug(
            'Sleeping update_schedule task for 60 seconds before running again')
        await asyncio.sleep(60)
    return schedule
