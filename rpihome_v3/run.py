#!/usr/bin/python3
""" main.py:
    Main entry-point into the RPiHome application.
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import datetime
from configure import configure_logger
from configure import configure_database
from configure import configure_pdevice
from configure import configure_adevice


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
def main():
    """ main function for the rpihome application """
    
    # Gather application configuration data from config.ini file
    logger = configure_logger('config.ini')
    database = configure_database('config.ini', logger)
    p_devices = configure_pdevice('config.ini', logger)
    a_devices = configure_adevice('config.ini', logger)
    logger.info('Finished call to configuration function')






if __name__ == '__main__':
    print('\n\n\n')
    main()
    print('\n')


