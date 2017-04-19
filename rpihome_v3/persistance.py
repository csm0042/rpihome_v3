#!/usr/bin/python3
""" mysql.py: Class and methods to connect to and query a mySQL database
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import copy
import logging
import mysql.connector
import mysql.connector.errorcode as errorcode
import rpihome_v3


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The rpihome Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Main event loop function ****************************************************
async def update_database(database, devices, loop, logger):
    """ test """
    while True:
        try:
            # Check each device in-turn for updates
            for index, device in enumerate(devices):
                # Log changes of state in automation device status
                if device.devtype == 'wemo_switch':
                    if device.status != device.status_mem:
                        cursor = database.cursor()
                        query = ("INSERT INTO device_log "
                                 "(device, status, timestamp) "
                                 "VALUES (%s, %s, %s)")
                        data = (device.name, device.status, device.last_seen)
                        cursor.execute(query, data)
                        database.commit()
                        cursor.close()
                        devices[index] = rpihome_v3.Device(
                            device.name, device.devtype, device.address,
                            device.status, device.status, device.last_seen,
                            device.cmd, device.cmd_mem, device.rule)
                elif device.devtype == 'personal':
                    if device.status != device.status_mem:
                        cursor = database.cursor()
                        query = ("INSERT INTO connection_log "
                                 "(device, connected, timestamp) "
                                 "VALUES (%s, %s, %s)")
                        data = (device.name, device.status, device.last_seen)
                        cursor.execute(query, data)
                        database.commit()
                        cursor.close()
                        devices[index] = rpihome_v3.Device(
                            device.name, device.devtype, device.address,
                            device.status, device.status, device.last_seen,
                            device.cmd, device.cmd_mem, device.rule)
            # Do not loop when status flag is false
            if loop is False:
                logger.debug('Breaking out of log_status_updates loop')
                break
            # Otherwise wait a pre-determined time period, then re-run the task
            logger.debug(
                'Sleeping log_status_updates task for 10 seconds before running again')
            await asyncio.sleep(10)
        except KeyboardInterrupt:
            logging.debug('Closing connection to database')
            database.close()
            logging.debug('Stopping log_status_updates process loop')
            break
