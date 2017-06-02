#!/usr/bin/python3
""" run.py:
    Main entry-point into the RPiHome application.
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import datetime
import logging
import typing
from concurrent.futures import ThreadPoolExecutor
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
    logger, credentials, location, tasks, database, devices = (
        rpihome_v3.configure_all('rpihome_v3//config.ini'))
    logger.info('Configuration imported from INI file *********************')

    # Create various support objects
    if tasks[0] is True or tasks[3] is True:
        logger.debug('Creating wemo gateway')
        wemo = rpihome_v3.WemoAPI(logger)
    if tasks[3] is True:
        logger.debug('Creating sunrise/sunset class')
        sun = rpihome_v3.Sun(location[0], location[1], -5, logger)
    if tasks[3] is True:
        logger.debug('Polling online device schedule')
        sched = rpihome_v3.GoogleCalSync(
            cal_id='r68pvu542kle1jm7jj9hjdp9o0@group.calendar.google.com',
            logger=logger)
        logger.debug('Creating Nest device class')
        nest = []

    # Get main event loop *****************************************************
    logger.info('Getting main event loop')
    executor = ThreadPoolExecutor(5)
    event_loop = asyncio.get_event_loop()

    # Run event loop until keyboard interrupt received ************************
    try:
        logger.info('Call run_until_complete on task list')
        if tasks[0] is True:
            asyncio.ensure_future(
                rpihome_v3.update_adev_status(
                    devices, wemo, event_loop, executor, 15, logger))
        if tasks[1] is True:
            asyncio.ensure_future(
                rpihome_v3.update_pdev_status(
                    devices, event_loop, executor, 15, logger))
        if tasks[2] is True:
            asyncio.ensure_future(
                rpihome_v3.update_mdev_status(
                    devices, event_loop, executor, 2, logger))
        if tasks[3] is True:
            asyncio.ensure_future(
                rpihome_v3.update_adev_cmd(
                    devices, wemo, sun, sched, event_loop, executor, 5, logger))
        if tasks[4] is True:
            asyncio.ensure_future(
                rpihome_v3.update_database(
                    database, devices, event_loop, executor, 5, logger))
        logger.info('Tasks are started')
        event_loop.run_forever()
    except KeyboardInterrupt:
        logger.debug('Closing connection to database')
        database.close()
    finally:
        logger.info(
            'Main event loop terminated @ [%s] ******************************',
            str(datetime.datetime.now()))
        event_loop.close()


# Call as script if run as __main__ *******************************************
if __name__ == '__main__':
    main()
