#!/usr/bin/python3
""" run.py:
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
    logger, credentials, database, tasks, devices = (
        rpihome_v3.configure_all('rpihome_v3//config.ini'))
    logger.info('Configuration imported from INI file *********************')

    # Create various support objects
    logger.debug('Creating wemo gateway')
    wemo = rpihome_v3.WemoAPI(logger)
    logger.debug('Creating sunrise/sunset class')
    sun = rpihome_v3.Sun(38.566268, -90.409878, -5, logger)
    logger.debug('Polling online device schedule')
    sched = rpihome_v3.GoogleCalSync(
        cal_id='r68pvu542kle1jm7jj9hjdp9o0@group.calendar.google.com',
        logger=logger)
    logger.debug('Creating Nest device class')
    nest = []

    # Get main event loop *****************************************************
    logger.info('Getting main event loop')
    event_loop = asyncio.get_event_loop()

    # Run event loop until keyboard interrupt received ************************
    try:
        logger.info('Call run_until_complete on task list')
        if tasks[0] is True:
            asyncio.ensure_future(
                rpihome_v3.update_adev_status(devices, wemo, True, 15, logger))
        if tasks[1] is True:
            asyncio.ensure_future(
                rpihome_v3.update_pdev_status(devices, True, 15, logger))
        if tasks[2] is True:
            asyncio.ensure_future(
                rpihome_v3.update_mdev_status(devices, True, 2, logger))
        if tasks[3] is True:
            asyncio.ensure_future(
                rpihome_v3.update_adev_cmd(devices, wemo, sun, sched, True, 5, logger))
        logger.info('Tasks are started')
        event_loop.run_forever()
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
