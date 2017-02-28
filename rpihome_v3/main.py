#!/usr/bin/python3
""" main.py:
    Main entry-point into the RPiHome application.
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import collections
import datetime
import file_logger
import device_ping


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Configure Logging ***********************************************************
debug_file, info_file = file_logger.setup_log_files(__file__)
logger = file_logger.setup_log_handlers(__file__, debug_file, info_file)


# Function Defs ***************************************************************
def main_event_loop(loop):
    """ Main event loop.  Calls coroutines as necessary """
    logger.info(
        "Calling main at %s",
        str(datetime.datetime.now().time()))
    loop.call_later(1, main_event_loop, loop)


async def scan_for_devices(device_list, rescan_seconds):
    """ Pings devices in a defined list to see if they are active on network"""
    while True:
        logger.info(
            "Calling 'read_calendar_coroutine' at %s",
            str(datetime.datetime.now().time())
            )
        for device in device_list:
            device_ping.ping_device(device.address)
        logger.info(
            "Finished 'read_calendar_coroutine' at %s",
            str(datetime.datetime.now().time())
            )
        await asyncio.sleep(rescan_seconds)


# Get Calendar Updates
async def read_calendar_coroutine():
    """ Reads google calendar to obtain current user home/away schedule """
    while True:
        logger.info(
            "Calling 'read_calendar_coroutine' at %s",
            str(datetime.datetime.now().time())
            )
        await asyncio.sleep(1.5)
        logger.info(
            "Finished 'read_calendar_coroutine' at %s",
            str(datetime.datetime.now().time())
            )
        await asyncio.sleep(900.0)


# Check Home / Away Status
async def check_home_coroutine():
    """ Checks to see if users are home """
    while True:
        logger.info(
            "Calling 'check_home_coroutine' at %s",
            str(datetime.datetime.now().time())
            )
        await asyncio.sleep(0.1)
        logger.info(
            "Finished 'check_home_coroutine' at %s",
            str(datetime.datetime.now().time())
            )
        await asyncio.sleep(60.0)


# Calculate sunrise/sunset times
async def calc_sun_coroutine():
    """ calculates sunrise/sunset times for current date """
    while True:
        logger.info(
            "Calling 'calc_sun_coroutine' at %s",
            str(datetime.datetime.now().time())
            )
        await asyncio.sleep(0.1)
        logger.info(
            "Finished 'calc_sun_coroutine' at %s",
            str(datetime.datetime.now().time())
            )
        await asyncio.sleep(900.0)


# Get Nest Updates
async def read_nest_coroutine():
    """ Reads current environmental condtions from Nest account """
    while True:
        logger.info(
            "Calling 'read_nest_coroutine' at %s",
            str(datetime.datetime.now().time())
            )
        await asyncio.sleep(1.5)
        logger.info(
            "Finished 'read_nest_coroutine' at %s",
            str(datetime.datetime.now().time())
            )
        await asyncio.sleep(900.0)


# Automation Engine
async def run_automation_coroutine():
    """ Evaluates rules and determines desired on/off state of devices """
    while True:
        logger.info(
            "Calling 'run_automation_coroutine' at %s",
            str(datetime.datetime.now().time())
            )
        await asyncio.sleep(0.2)
        logger.info(
            "Finished 'run_automation_coroutine' at %s",
            str(datetime.datetime.now().time())
            )
        await asyncio.sleep(1.0)


# Define values specific to this house
Device = collections.namedtuple("Device", "name, address, state")
phones = []
phones.append(Device("chris", "192.168.86.40", "False"))
phones.append(Device("aiden", "192.168.86.41", "False"))
phones.append(Device("sarah", "192.168.86.42", "False"))


# Call functions from main loop ***********************************************
eventloop = asyncio.get_event_loop()
eventloop.call_soon(main_event_loop, eventloop)
eventloop.run_until_complete(
    asyncio.gather(
        scan_for_devices(phones, 60.0),
        read_calendar_coroutine(),
        check_home_coroutine(),
        calc_sun_coroutine(),
        read_nest_coroutine(),
        run_automation_coroutine()
        ))


# Run main event loop *********************************************************
try:
    eventloop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print('step: loop.close()')
    eventloop.close()
