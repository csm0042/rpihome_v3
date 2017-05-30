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



# Async wrapper function ******************************************************
async def asyncio_wrapper(function, loop, sleep, logger):
    """ test """
    while True:
        try:
            # Perform desired function on args
            function

            # Do not loop when status flag is false
            if loop is False:
                logger.debug('Breaking out of update_device_status loop')
                break
            # Otherwise wait a pre-determined time period, then re-run the task
            logger.debug('Sleeping task for %s seconds', str(sleep))
            await asyncio.sleep(sleep)
        except KeyboardInterrupt:
            logging.debug(
                'Killing task')
            break
            break


# Main event loop function ****************************************************
def main():
    """ main function for the rpihome application """

    # Get configuration from INI file for this run
    logger, credentials, database, tasks, devices = (
        rpihome_v3.configure_all('rpihome_v3//config.ini'))
    logger.info('Configuration imported from INI file *********************')

    # Create various support objects
    wemo = rpihome_v3.WemoAPI(logger)
    sun = rpihome_v3.Sun(38.566268, -90.409878, -5, logger)
    sched = rpihome_v3.GoogleCalSync(
        cal_id='r68pvu542kle1jm7jj9hjdp9o0@group.calendar.google.com',
        logger=logger)
    nest = []

    # Get main event loop *****************************************************
    logger.info('Getting main event loop')
    event_loop = asyncio.get_event_loop()

    # Run event loop until keyboard interrupt received ************************
    try:
        logger.info('Call run_until_complete on task list')
        if tasks[0] is True:
            asyncio.async(
                asyncio_wrapper(
                    rpihome_v3.update_adev_status(devices, wemo, logger),
                    True, 5, logger
                    )
                )
        if tasks[1] is True:
            asyncio.async(
                asyncio_wrapper(
                    rpihome_v3.update_pdev_status(devices, logger),
                    True, 15, logger
                    )
                )
        if tasks[2] is True:
            asyncio.async(
                asyncio_wrapper(
                    rpihome_v3.update_mdev_status(devices, logger),
                    True, 2, logger
                    )
                )
        if tasks[3] is True:
            asyncio.async(
                asyncio_wrapper(
                    rpihome_v3.update_adev_cmd(devices, wemo, sun, sched, logger),
                    True, 5, logger
                    )
                )
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
