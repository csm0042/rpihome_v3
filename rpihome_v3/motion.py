#!/usr/bin/python3
""" motion.py:
    Motion sensing function.  Monitors a folder on a network for screen captures
    provided by a motion sensing security camera.  When a new screen shot is
    detected, it returns "true"
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import datetime
import os
import shutil
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


# Defined named tuples for various object types *******************************
async def check_motion(device, logger):
    """ Monitors network folder for picture files.  These files are stored in
    this location by a separate process whenever a security camera detects
    motion """
    timeout = 2 #minutes
    capture_count = 0
    capture_dir = device.address
    archive_dir = os.path.join(device.address, 'archive')
    # Search capture dir for capture files
    dir_contents = os.listdir(capture_dir)
    # Count files in found contents (ignore directories)
    for item in dir_contents:
        if os.path.isfile(os.path.join(device.address, item)):
            capture_count += 1
    if capture_count > 0:
        logger.debug(
            'Motion capture found in search folder. ' +
            'Setting motion detection to True')
        for file in dir_contents:
            rpihome_v3.move_file(file, capture_dir, archive_dir, logger)
            # Update device record
            device = rpihome_v3.Device(
                device.name, device.devtype, device.address,
                "true", device.status_mem, str(datetime.datetime.now()),
                device.cmd, device.cmd_mem, device.rule)
    # When a capture is not found AND a certain time has elapsed since
    # the last find
    elif datetime.datetime.now() >= (
            datetime.datetime.strptime(device.last_seen[0:18], '%Y-%m-%d %H:%M:%S') +
            datetime.timedelta(minutes=timeout)):
        logger.debug(
            'No captures seen in the timeout period.  ' +
            'Motion detection status set back to false')
        device = rpihome_v3.Device(
            device.name, device.devtype, device.address,
            'false', device.status_mem, str(datetime.datetime.now()),
            device.cmd, device.cmd_mem, device.rule)
    # When a capture is not found AND the timeout has not yet completed
    else:
        logger.debug(
            'No captures detected. ' +
            'Timeout not yet elapsed.  Status remains unchanged')
        device = rpihome_v3.Device(
            device.name, device.devtype, device.address,
            device.status, device.status_mem, device.last_seen,
            device.cmd, device.cmd_mem, device.rule)
    return device


def move_file(filename, source_dir, dest_dir, logger):
    try:
        if os.path.isfile(os.path.join(source_dir, filename)):
            shutil.move(
                os.path.join(source_dir, filename),
                os.path.join(dest_dir, filename)
                )
            logger.debug('Successfully moved capture file')
    except:
        logger.warning('Oh crap, couldn\'t remove the requested file')
