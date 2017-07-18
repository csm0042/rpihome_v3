#!/usr/bin/python3
""" configure.py:
    Configuration process for the RPiHome application.
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import configparser
import mysql.connector
import mysql.connector.errorcode as errorcodes
import sys
if __name__ == "__main__":
    sys.path.append("..")
import helpers


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
def configure_log(filename):
    # Define connection to configuration file
    config_file = configparser.ConfigParser()
    config_file.read(filename)
    # Set up application logging
    log = helpers.setup_log_handlers(
        __file__,
        config_file['LOG FILES']['debug_log_file'],
        config_file['LOG FILES']['info_log_file'])
    # Return configured objects to main program
    return log


# Obtain Credentials **********************************************************
def configure_credentials(filename, log):
    # Define connection to configuration file
    config_file = configparser.ConfigParser()
    config_file.read(filename)
    # Read credential info from file
    try:
        credentials = config_file['CREDENTIALS']['file']
        log.debug('Credentails file found')
    except:
        log.error('No credentials file found')
    # Return configured objects to main program
    return credentials


# Config Database Connection Function *****************************************
def configure_database(filename, credentials, log):
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
        log.debug("Successfully connected to database")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            database = None
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            database = None
        else:
            database = None
        pass
        log.debug("Could not connect to database")
    # Return configured objects to main program
    return database


# Configure service socket server *********************************************
def configure_server(filename, log):
    # Define connection to configuration file
    config_file = configparser.ConfigParser()
    config_file.read(filename)
    # Read credential info from file
    try:
        address = config_file['PERSISTANCE SERVICE']['address']
        port = (config_file['PERSISTANCE SERVICE']['port'])
        log.debug('Address and port found: %s:%s', address, port)
    except:
        log.error('No address or port configuration found')
        address = '0'
        port = '0'
    # Return configured objects to main program
    return address, port


# Configure service socket server *********************************************
def configure_automation_connection(filename, log):
    # Define connection to configuration file
    config_file = configparser.ConfigParser()
    config_file.read(filename)
    # Read credential info from file
    try:
        address = config_file['AUTOMATION SERVICE']['address']
        port = config_file['AUTOMATION SERVICE']['port']
        log.debug('Address and port found: %s:%s', address, port)
    except:
        log.error('No address or port configuration found')
        address = '0'
        port = '0'
    # Return configured objects to main program
    return address, port
