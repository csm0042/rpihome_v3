#!/usr/bin/python3
""" main.py:
    Main entry-point into the RPiHome application.
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
from concurrent.futures import ProcessPoolExecutor
import datetime
from configure import configure_logger
from configure import configure_database
from configure import configure_pdevice
from configure import configure_adevice
from configure import Adevice
from configure import Pdevice
from ping import ping_device


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Helper Function Definiions **************************************************
def setup(filename):
    """ Gather application configuration data from config.ini file """
    logger = configure_logger(filename)
    database = configure_database(filename, logger)
    p_devices = configure_pdevice(filename, logger)
    a_devices = configure_adevice(filename, logger)
    logger.info('Finished call to configuration function')
    return logger, p_devices, a_devices


def async_wrapper(function, arguments):
    """ wrapper to allow user to call a non-async function as a
	coroutine """
    result = function(arguments)
    return result


def ping_devices(loop, device_list, sleeptime):
	""" Pings every device in a list periodically as defined by sleeptime
	input variable.  Each device is ping'd using an individual coroutine
	so nothing blocks the main thread """
	while True:
		for index, device in enumerate(device_list):
			result = loop.call_soon(async_wrapper(ping_device, (device.address)))
			device = Pdevice(
				device.name, device.address,
				str(result), str(datetime.datetime.now())
				)
                device_list[index] = device
		return device_list
		await asyncio.sleep(sleeptime)
		
	
async def main():
	""" main function for the rpihome application """
    executor = ProcessPoolExecutor(2)
    while True:

        await asyncio.sleep(1.0)


if __name__ == '__main__':
    # Configure application using settings from INI file **********************
	logger, p_devices, a_devices = setup('config.ini')

    # Create main event loop **************************************************
    executor = ProcessPoolExecutor(2)
	loop = asyncio.get_event_loop()

    # Parallel process threads ************************************************
    p_devices = 


    # Run main event loop & coroutines ****************************************
	try:
		loop.run_forever()
	except KeyboardInterrupt:
		pass
	finally:
		print('\n\nMain event loop terminated\n\n')
		loop.close()



