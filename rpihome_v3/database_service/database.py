#!/usr/bin/python3
""" mysql.py: Class and methods to connect to and query a mySQL database
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import datetime
import logging
import sys
if __name__ == "__main__":
    import sys
    sys.path.append("..")
import database_service


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The rpihome Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Insert Record into log table in database function ***************************
def insert_record(database, device, logger):
    """ Inserts a new record into the device log table """
    # Configure logger
    logger = logger or logging.getLogger(__name__)
    logger.debug('insert_record function has been called')
    # Attempt database record insert
    try:
        # Check first if valid database connection was made
        if database is not None:
            logger.debug('Connection to database is ok')
            cursor = database.cursor()
            logger.debug('Connection to cursor successful')
            query = ("INSERT INTO device_log "
                     "(device, status, timestamp) "
                     "VALUES (%s, %s, %s)")
            data = (device.name, device.status, str(device.last_seen))
            full_query = query % data
            logger.debug('Ready to execute query: %s', full_query)            
            cursor.execute(query, data)
            logger.debug('Query execution successful')            
        else:
            logger.warning('No connection to database')
    except:
        logger.warning('Attempt to inesrt record into database failed')
    finally:
        database.commit()
        logger.debug('Changed committed to database')
        cursor.close()
        logger.debug('Closed connection to database cursor')


# Return pending commands from device_cmd table function **********************
def query_command(database, logger):
    """ Returns a list of un-processed commands from the device_cmd table """
    # Configure logger
    logger = logger or logging.getLogger(__name__)
    logger.debug('query_command function has been called')
    # initialize result list
    result_list = []
    # Attempt database record insert
    try:
        # Check first if valid database connection was made
        if database is not None:
            logger.debug('Connection to database is ok')
            # Grab cursor and prepare query
            cursor = database.cursor()
            logger.debug('Connection to cursor successful')
            query = ("SELECT id_device_cmd, device, cmd, timestamp, processed "
                     "FROM device_cmd "
                     "WHERE (timestamp >= '%s' AND processed IS NULL)")
            current_time = (str(datetime.datetime.now() + datetime.timedelta(days=-30)))[:19]
            data = (current_time)
            full_query = query % data
            logger.debug('Ready to execute query: %s', full_query)            
            cursor.execute(query, data)
            logger.debug('Query execution successful')
            row = cursor.fetchone()
            while row is not None:
                result_list.append(
                    database_service.DeviceCmd(
                        id_dev=row[0],
                        name=row[1],
                        cmd=row[2],
                        timestamp=row[3],
                        processed=row[4])
                    )
                row = cursor.fetchone()
            logger.debug('Select query successful')
            print('Results found: %s' % str(len(result_list)))

        else:
            logger.warning('No connection to database')
    except:
        logger.warning('Attempt to query database failed')
    finally:
        database.commit()
        logger.debug('Changed committed to database')
        cursor.close()
        logger.debug('Closed connection to database cursor') 
    return result_list


# Update processed status of commands in device_cmd table function ************
def update_command(database, id_dev, logger):
    """ Updates processed field for an individual record in the device cmd table """
    # Configure logger
    logger = logger or logging.getLogger(__name__)
    logger.debug('update_command function has been called')
    # Attempt database record insert
    try:
        # Check first if valid database connection was made
        if database is not None:
            logger.debug('Connection to database is ok')
            # Grab cursor and prepare query
            cursor = database.cursor()
            logger.debug('Connection to cursor successful')
            query = ("UPDATE device_cmd "
                     "SET processed = %s "
                     "WHERE id_device_cmd = %s")
            current_time = str(datetime.datetime.now())[:19]
            data = (current_time, id_dev)
            full_query = query % data
            logger.debug('Ready to execute query: %s', full_query) 
            cursor.execute(query, data)
            logger.debug('Query execution successful')
        else:
            logger.warning('No connection to database')
    except:
        logger.warning('Attempt to query database failed')
    finally:
        database.commit()
        logger.debug('Changed committed to database')
        cursor.close()
        logger.debug('Closed connection to database cursor')          
