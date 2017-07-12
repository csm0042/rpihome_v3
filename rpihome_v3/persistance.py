#!/usr/bin/python3
""" mysql.py: Class and methods to connect to and query a mySQL database
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import copy
import datetime
import logging
import mysql.connector
import mysql.connector.errorcode as errorcode
import sys
import time
if __name__ == "__main__":
    sys.path.append("..")
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
def insert_record(database, device, logger):
    """ test """
    # Configure logger
    logger = logger or logging.getLogger(__name__)
    # Attempt database record insert
    try:
        # Check first if valid database connection was made
        if database is not None:
            cursor = database.cursor()
            query = ("INSERT INTO device_log "
                     "(device, status, timestamp) "
                     "VALUES (%s, %s, %s)")
            data = (device.name, device.status, str(device.last_seen))
            cursor.execute(query, data)
            database.commit()
            cursor.close()
        else:
            logger.warning(
                'No connection to database. Updates are not being logged')
    except:
        logger.warning(
            'Attempt to inesrt record into database failed')


def query_command(database, logger):
    """ test """
    # Configure logger
    logger = logger or logging.getLogger(__name__)
    # Attempt database record insert
    try:
        # Check first if valid database connection was made
        result_list = []
        if database is not None:
            cursor = database.cursor()
            query = ("SELECT id_device_cmd, device, cmd, timestamp, processed "
                     "FROM device_cmd "
                     "WHERE (timestamp >= '%s' AND processed IS NULL)")
            current_time = (str(datetime.datetime.now() + datetime.timedelta(days=-30)))[:19]
            data = (current_time)
            cursor.execute(query, data)

            row = cursor.fetchone()
            while row is not None:
                result_list.append(copy.copy(row))
                print(row)
                row = cursor.fetchone()

        else:
            logger.warning(
                'No connection to database. Cannot perform query')
    except:
        logger.warning(
            'Attempt to query database failed')
    finally:
        database.commit()
        cursor.close() 



if __name__ == "__main__":
    # Get configuration
    logger, credentials, location, tasks, database, devices = \
        rpihome_v3.configure_application('config.ini')
    while True:
        query_command(database, logger)
        time.sleep(0.25)
