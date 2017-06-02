#!/usr/bin/python3
""" device_cmd.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
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
        device, wemo = rpihome_v3.wemo_set_on(device, wemo, logger)
    # Turn off light if after sunrise and before sunset and currently on
    if ((datetime.datetime.now().time() >= sun.sunrise()
         and
         datetime.datetime.now().time() < sun.sunset())
            and
            device.cmd.lower() != 'off'):
        logger.info('Turning off [%s] based on dusk to dawn rule', device.name)
        device, wemo = rpihome_v3.wemo_set_off(device, wemo, logger)
    # Return updated list to calling routine
    return device


# Dusk to dawn function *******************************************************
def schedule(device, wemo, sched, logger):
    """ test """
    # Configure logger
    logger = logger or logging.getLogger(__name__)    
    # Get schedule sub-set for device
    sched_subet = rpihome_v3.sched_by_name(name=device.name)
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
            device = rpihome_v3.wemo_set_on(device, wemo, logger)
        if desired_state == 'off':
            device = rpihome_v3.wemo_set_off(device, wemo, logger)
    # Return updated device to calling routine
    return device
