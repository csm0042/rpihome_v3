#!/usr/bin/python3
""" configure.py:
    Configuration process for the RPiHome application.
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import configparser
import mysql.connector
import mysql.connector.errorcode as errorcodes
if __name__ == "__main__":
    import sys
    sys.path.append("..")
import database_service


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Config Function Def *********************************************************
def configure_logger(filename):
    # Define connection to configuration file
    config_file = configparser.ConfigParser()
    config_file.read(filename)
    # Set up application logging
    logger = database_service.setup_log_handlers(
        __file__,
        config_file['LOG FILES']['debug_log_file'],
        config_file['LOG FILES']['info_log_file'])
    # Return configured objects to main program
    return logger


# Obtain Credentials **********************************************************
def configure_credentials(filename, logger):
    # Define connection to configuration file
    config_file = configparser.ConfigParser()
    config_file.read(filename)
    # Read credential info from file
    try:
        credentials = config_file['CREDENTIALS']['file']
        logger.debug('Credentails file found')
    except:
        logger.error('No credentials file found')
    # Return configured objects to main program
    return credentials


# Config Database Connection Function *****************************************
def configure_database(filename, credentials, logger):
    # Define connection to configuration file
    config_file = configparser.ConfigParser()
    config_file.read(filename)
    credential_file = configparser.ConfigParser()
    credential_file.read(credentials)
    # Set up database connection
    try:
        database = mysql.connector.connect(
            host=config_file['DATABASE']['host'],
            port=config_file['DATABASE']['port'],
            database=config_file['DATABASE']['schema'],
            user=credential_file['DATABASE']['username'],
            password=credential_file['DATABASE']['password'])
        logger.debug("Successfully connected to database")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            database = None
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            database = None
        else:
            database = None
        pass
        logger.debug("Could not connect to database")
    # Return configured objects to main program
    return database


# Configure service socket server *********************************************
def configure_server(filename, logger):
    # Define connection to configuration file
    config_file = configparser.ConfigParser()
    config_file.read(filename)
    # Read credential info from file
    try:
        address = config_file['SOCKET SERVER']['address']
        port = int(config_file['SOCKET SERVER']['port'])
        logger.debug('Address and port found: %s:%s', address, port)
    except:
        logger.error('No address or port configuration found')
        address = None
        port = 0
    # Return configured objects to main program
    return address, port


# Simple function test ********************************************************
if __name__ == "__main__":
    logger = configure_logger('config.ini')
    credentials = configure_credentials('config.ini', logger)
    print(credentials)
    database = configure_database('config.ini', credentials, logger)
    print(database)
    address, port = configure_server('config.ini', logger)
    print(address, ":", port)
