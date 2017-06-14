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
import time
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


# Get main event loop *****************************************************
executor = ThreadPoolExecutor(5)
loop = asyncio.get_event_loop()
sd = False


# Flash App for Gui ***********************************************************
app = Flask(__name__)

def flaskThread():
    app.run()

@app.route("/")
def index():
    return render_template('index.html', event_loop_status='Control Disabled')

@app.route('/start')
def start():
    return render_template('index.html', event_loop_status='RUNNING')

@app.route('/stop')
def stop():
    shutdown = True
    loop.stop()
    print('Shutting down')
    time.sleep(10)

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


# Call as script if run as __main__ *******************************************
if __name__ == '__main__':
    # Get configuration
    logger, credentials, location, tasks, database, devices = \
        rpihome_v3.configure_application('config.ini')

    # Start flask server thread for GUI
    gui_thread = threading.Thread(target=flaskThread)
    gui_thread.start()

    # Start event loop
    rpihome_v3.event_loop(
        executor, loop, logger, sd, credentials, location, tasks, database, devices)
