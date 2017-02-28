#!/usr/bin/python3
""" device_ping.py:   
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import os
import platform


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Ping Function ***************************************************************
def ping_device(address):
    """ Pings a device with a given address and returns a True/False based
    upon whether or not the device responded  """
    # Set ping command flags based upon operating system used
    if platform.system().lower() == "windows":
        ping_flags = "-n 1"
    else:
        ping_flags = "-c 1"
    # Perform ping
    result = os.system("ping " + ping_flags + " " + address)
    # evaluate result
    if result == 0:
        return True
    else:
        return False


def insert_db_record(address, schema, user, pwd, table, device, state):
    """ Inserts a record into a mySQL data table """
    # Create connection to database
    try:
        db = mysql.connector.connect(host=address,
                                     database=schema,
                                     user=user,
                                     password=pwd)
        cursor = db.cursor()
        query = "INSERT INTO '%s'.'%s' ('device', 'connected') \
        VALUES ('%s', '%s')", schema, table, device, state
        cursor.execute(query)
        db.commit()
        cursor.close()
        db.close()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            self.connected = False
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            self.connected = False
        else:
            self.connected = False
