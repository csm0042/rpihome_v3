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





# Call as script if run as __main__ *******************************************
if __name__ == '__main__':
    logger, credentials, location, tasks, database, devices = \
        rpihome_v3.configure_application('config.ini')

    app.run()
    riphome_v3.event_loop(logger, credentials, location, tasks, database, devices)
