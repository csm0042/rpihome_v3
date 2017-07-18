#!/usr/bin/python3
""" device_cmd.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import datetime
import logging


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
def dusk_to_dawn(device, wemo, sun, logger):
    """ test """
    # Configure logger
    logger = logger or logging.getLogger(__name__)
    # Turn on light if after sunset or before sunrise and not already on
    if ((datetime.datetime.now().time() < sun.sunrise()
         or
         datetime.datetime.now().time() >= sun.sunset())
            and
            device.cmd.lower() != 'on'):
        logger.info('Turning on [%s] based on dusk to dawn rule', device.name)
        wemo.turn_on(device)
    # Turn off light if after sunrise and before sunset and currently on
    if ((datetime.datetime.now().time() >= sun.sunrise()
         and
         datetime.datetime.now().time() < sun.sunset())
            and
            device.cmd.lower() != 'off'):
        logger.info('Turning off [%s] based on dusk to dawn rule', device.name)
        wemo.turn_off(device)


# Dusk to dawn function *******************************************************
def schedule(device, wemo, sched, logger):
    """ test """
    # Configure logger
    logger = logger or logging.getLogger(__name__)
    # Get schedule sub-set for device
    sched_subset = sched.sched_by_name(name=device.name)
    # Initialize state
    desired_state = 'off'
    # Cycle through schedule sub-set looking for match
    for s in sched_subset:
        if (datetime.datetime.now() >= sched_subset.start and
                datetime.datetime.now() < sched_subset.end):
            desired_state = 'on'
    # Check for change of state and send commands if necessary
    if device.cmd != desired_state:
        if desired_state == 'on':
            wemo.turn_on(device)
        if desired_state == 'off':
            wemo.turn_off(device)
    # Return updated device to calling routine
