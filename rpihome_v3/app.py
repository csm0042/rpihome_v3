#!/usr/bin/python3
""" app.py:
    Main entry-point into the RPiHome application.
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import datetime
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, render_template
import sys
import threading
import webbrowser
if __name__ == "__main__":
    sys.path.append("..")
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


# Flash App for Gui ***********************************************************
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html', event_loop_status='Control Disabled')

@app.route('/start')
def start():
    return render_template('index.html', event_loop_status='RUNNING')

@app.route('/stop')
def stop():
    return render_template('index.html', event_loop_status='Control Disabled')

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down'

@app.route('/start_adev_status')
def start_adev_status(devices, wemo, loop, executor, delay, logger):
    asyncio.ensure_future(
        rpihome_v3.update_adev_status(
            devices, wemo, loop, executor, delay, logger))
    logger.info('Scheduling update automation device status task')


# Main event loop function ****************************************************
def event_loop(logger, credentials, location, tasks, database, devices):
    """ main function for the rpihome application """
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
    loop = asyncio.get_event_loop()

    # Schedule tasks for execution ********************************************
    if tasks[0] is True:
        asyncio.ensure_future(
            rpihome_v3.update_adev_status(
                devices, wemo, loop, executor, 15, logger))
        logger.info('Scheduling update automation device status task')
    if tasks[1] is True:
        asyncio.ensure_future(
            rpihome_v3.update_pdev_status(
                devices, loop, executor, 15, logger))
        logger.info('Scheduling update personal device status task')
    if tasks[2] is True:
        asyncio.ensure_future(
            rpihome_v3.update_mdev_status(
                devices, loop, executor, 2, logger))
        logger.info('Scheduling update motion detector device status task')
    if tasks[3] is True:
        asyncio.ensure_future(
            rpihome_v3.update_adev_cmd(
                devices, wemo, sun, sched, loop, executor, 5, logger))
        logger.info('Scheduling update automation device command task')
    if tasks[4] is True:
        asyncio.ensure_future(
            rpihome_v3.update_database(
                database, devices, loop, executor, 5, logger))
        logger.info('Scheduling update persistance task')

    # Run event loop until keyboard interrupt received ************************
    try:
        logger.info('Call run_forever on event loop')
        loop.run_forever()
    except KeyboardInterrupt:
        logger.debug('Closing connection to database')
        database.close()
    finally:
        logger.info('RpiHome v3 Application terminated @ [%s]',
                    str(datetime.datetime.now()))
        loop.close()




# Call as script if run as __main__ *******************************************
if __name__ == '__main__':
    # Get configuration 
    logger, credentials, location, tasks, database, devices = \
        rpihome_v3.configure_application('config.ini')

    
    # Start event loop
    rpihome_v3.event_loop(
        logger, credentials, location, tasks, database, devices)


    app.run()
