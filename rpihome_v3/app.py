#!/usr/bin/python3
""" app.py:
    Main entry-point into the RPiHome application.
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import datetime
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, render_template
import webbrowser
from . import *

# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Flash App for Gui ***********************************************************
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/start')
def start():
    return 'Started'

@app.route('/stop')
def stop():
    return 'stopped'


# Main event loop function ****************************************************
def main():
    """ main function for the rpihome application """

    # Configure Logging *******************************************************
    logger = rpihome_v3.configure_logger('rpihome_v3//config.ini')
    logger.info('RpiHome v3 Application started @ [%s]',
                str(datetime.datetime.now()))

    # Get user credentials ****************************************************
    credentials = rpihome_v3.configure_credentials('rpihome_v3//config.ini', logger)
    logger.info('Credential info imported')

    # Get gui url *************************************************************
    url = rpihome_v3.configure_gui('rpihome_v3//config.ini', logger)
    logger.info('GUI url info imported')
    webbrowser.open(url, new=2, autoraise=True)

    # Get location info *******************************************************
    location = rpihome_v3.configure_location('rpihome_v3//config.ini', logger)
    logger.info('Location info imported')

    # Determine what tasks should run *****************************************
    tasks = rpihome_v3.configure_tasks('rpihome_v3//config.ini', logger)
    logger.info('Desired task setup info imported')

    # Get database connection info ********************************************
    database = rpihome_v3.configure_database('rpihome_v3//config.ini', credentials, logger)
    logger.info('Database connection info imported')

    # Get list of system devices to monitor/control ***************************
    devices = rpihome_v3.configure_devices('rpihome_v3//config.ini', logger)
    logger.info('System device info imported')

    # Create wemo gateway class ***********************************************
    if tasks[0] is True or tasks[3] is True:
        logger.debug('Creating Wemo device gateway')
        wemo = rpihome_v3.WemoAPI(logger)

    # Create sun class used for calculating sunrise/sunset times **************
    if tasks[3] is True:
        logger.debug('Creating sunrise/sunset class for [%s, %s]',
                     str(location[0]), str(location[1]))
        sun = rpihome_v3.Sun(location[0], location[1], -5, logger)

    # Create schedule class ***************************************************
    if tasks[3] is True:
        logger.debug('Creating device schedule')
        sched = rpihome_v3.GoogleCalSync(
            cal_id='r68pvu542kle1jm7jj9hjdp9o0@group.calendar.google.com',
            logger=logger)

    # Create environmental status class (Nest device) *************************
    if tasks[5] is True:
        logger.debug('Creating Nest device gateway')
        nest = []



    # Get main event loop *****************************************************
    logger.info('Getting main event loop')
    executor = ThreadPoolExecutor(5)
    event_loop = asyncio.get_event_loop()

    # Schedule tasks for execution ********************************************
    if tasks[0] is True:
        asyncio.ensure_future(
            rpihome_v3.update_adev_status(
                devices, wemo, event_loop, executor, 15, logger))
        logger.info('Scheduling update automation device status task')
    if tasks[1] is True:
        asyncio.ensure_future(
            rpihome_v3.update_pdev_status(
                devices, event_loop, executor, 15, logger))
        logger.info('Scheduling update personal device status task')
    if tasks[2] is True:
        asyncio.ensure_future(
            rpihome_v3.update_mdev_status(
                devices, event_loop, executor, 2, logger))
        logger.info('Scheduling update motion detector device status task')
    if tasks[3] is True:
        asyncio.ensure_future(
            rpihome_v3.update_adev_cmd(
                devices, wemo, sun, sched, event_loop, executor, 5, logger))
        logger.info('Scheduling update automation device command task')
    if tasks[4] is True:
        asyncio.ensure_future(
            rpihome_v3.update_database(
                database, devices, event_loop, executor, 5, logger))
        logger.info('Scheduling update persistance task')

    # Run event loop until keyboard interrupt received ************************
    try:
        logger.info('Call run_forever on event loop')
        event_loop.run_forever()
    except KeyboardInterrupt:
        logger.debug('Closing connection to database')
        database.close()
    finally:
        logger.info('RpiHome v3 Application terminated @ [%s]',
                    str(datetime.datetime.now()))
        event_loop.close()


# Call as script if run as __main__ *******************************************
if __name__ == '__main__':
    app.run()
    #main()
