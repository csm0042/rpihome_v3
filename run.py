#!/usr/bin/python3
""" main.py:
    Main entry-point into the RPiHome application.
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import datetime
import logging
import typing
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


# Main event loop function ****************************************************
def main():
    """ main function for the rpihome application """

    # Get configuration from INI file for this run
    logger, database, devices, cal_credentials = (
        rpihome_v3.configure_all('rpihome_v3//config.ini'))
    logger.info(
        'RpiHome-v3 Application Started @ [%s] ******************************',
        str(datetime.datetime.now()))
    logger.info('Configuration imported from INI file')

    # Get main event loop *****************************************************
    logger.info('Getting main event loop')
    event_loop = asyncio.get_event_loop()

    # Perform initial schedule query ******************************************
    schedule = rpihome_v3.update_schedule(cal_credentials, False, logger)

    # Run event loop until keyboard interrupt received ************************
    try:
        logger.info('Call run_until_complete on task list')
        event_loop.run_until_complete(
            asyncio.gather(
                #rpihome_v3.update_schedule(cal_credentials, True, logger),
                rpihome_v3.update_adevice_status(devices, True, logger),
                rpihome_v3.update_pdevice_status(devices, True, logger),
                rpihome_v3.update_database(database, devices, True, logger)
                ))
        logger.info('Tasks are started')
    except KeyboardInterrupt:
        logger.debug('Closing connection to database')
        database.close()
        pass
    finally:
        logger.info(
            'Main event loop terminated @ [%s] ******************************',
            str(datetime.datetime.now()))
        event_loop.close()


# Call as script if run as __main__ *******************************************
if __name__ == '__main__':
    main()
