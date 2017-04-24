#!/usr/bin/python3
""" nest.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import configparser
import datetime
import linecache
import logging
import os
import sys
import time
import nest
import rpihome_v3


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# NEST connect and query functions ********************************************
async def connect_to_nest(device, credentials, logger):
    # Get credentials for login
    logger.debug('Getting NEST credentials from file')
    credential_file = configparser.ConfigParser()
    credential_file.read(credentials)
    client_id = credential_file['NEST']['client_id']
    client_secret = credential_file['NEST']['client_secret']
    authorize_url = credential_file['NEST']['authorization_url']
    client_pin = credential_file['NEST']['client_pin']
    access_token_cache_file = credential_file['NEST']['access_token_cache_file']

    # Create connection to Nest API
    logger.debug("Attempting to connect to NEST account")
    try:
        nest_device = nest.Nest(
            client_id=client_id,
            client_secret=client_secret,
            access_token_cache_file=access_token_cache_file)
        logger.debug('Nest instance created')
    except:
        logger.debug('Error creating NEST instance')

    # Authorize connection
    if nest_device.authorization_required:
        logger.debug('Need to authorize via online pin')

        if len(client_pin) > 0:
            logger.debug('Pin found in config file. Requesting token')
            nest_device.request_token(client_pin)
            logger.debug('Pin Sent')

        if len(client_pin) <= 0:
            logger.warning(
                'Go to [%s] to authorize, then enter pin into configuration file',
                nest_device.authorize_url)
    else:
        logger.debug('Did not need to bother with pin this time')
    # Return result
    return nest_device



async def current_conditions(device, nest_list, credentials, logger):
    # Check if device is already in the list of known wemo devices
    logger.debug('Searching list of known NEST devices for [%s]', device.name)
    result = next(
        (index for index, nestdev in enumerate(nest_list)
         if nestdev.name == device.name), None)
    # Point to existing list record or recently discovered device
    if result == None:
        logger.debug(
            '[%s] not found in list of known NEST devices.  Performing discovery',
            device.name)
        nest_device = await connect_to_nest(device, credentials, logger)
    else:
        logger.debug('[%s] Found in list of known NEST devices')
        nest_device = nest_list[result]
    # Perform status query
    if nest_device is not None:
        logger.debug('Performing query for current conditions')
        try:
            structure = nest_device.structures[0]
            current_temp = str(int((structure.weather.current.temperature * 1.8) + 32))
            current_condition = structure.weather.current.condition
            current_wind_dir = structure.weather.current.wind.direction
            current_humid = str(int(structure.weather.current.humidity))
            status = (
                "%s,%s,%s,%s" % (
                    current_condition, current_temp, current_wind_dir, current_humid))
            logger.debug("Data successfully obtained.  Returning [%s] to main" % status)
        except:
            logger.warning("Failure reading current conditions from NEST device")
            status = "??,??,??,??"
        finally:
            # If device was not previously in wemo list, add it for next time
            nest_list.append(copy.copy(nest_device))
    else:
        status = 'offline'
        logger.debug('Cound not connect to NEST device - status set to offline')
    # Re-define device with updated status
    device = rpihome_v3.Device(
        device.name, device.devtype, device.address,
        status, device.status_mem, str(datetime.datetime.now()),
        device.cmd, device.cmd_mem, device.rule)
    # Return result and nest connection for future use
    return device, nest_list



async def current_forecast(device, nest, credentials, logger):
    if nest is None:
        nest = connect_to_nest(device, credentials, logger)
    if nest is not None:
        logger.debug("Attempting to parse data on today's forecast from NEST data")
        try:
            structure = nest.structures[0]
            forecast = structure.weather.daily[0]
            forecast_condition = forecast.condition
            forecast_temp_low = str(int((forecast.temperature[0] * 1.8) + 32))
            forecast_temp_high = str(int((forecast.temperature[1] * 1.8) + 32))
            forecast_humid = str(int(forecast.humidity))
            status = (
                "%s,%s,%s,%s" % (
                    forecast_condition, forecast_temp_low, forecast_temp_high, forecast_humid))
            logger.debug("Data successfully obtained.  Returning [%s] to main" % status)
        except:
            logger.warning("Failure reading tomorrow's forecast data from NEST device")
            status = "??,??,??,??"
    else:
        logger.warning("Failure reading tomorrow's forecast data from NEST device")
        status = "??,??,??,??"
    # Re-define device with updated status
    device = rpihome_v3.Device(
        device.name, device.devtype, device.address,
        status, device.status_mem, str(datetime.datetime.now()),
        device.cmd, device.cmd_mem, device.rule)
    # Return result and nest connection for future use
    return device, nest


async def tomorrow_forecast(device, nest, credentials, logger):
    if nest is None:
        nest = connect_to_nest(device, credentials, logger)
    if nest is not None:
        logger.debug("Attempting to parse data on tomorrow's forecast from NEST data")
        try:
            structure = nest.structures[0]
            forecast = structure.weather.daily[1]
            forecast_condition = forecast.condition
            forecast_temp_low = str(int((forecast.temperature[0] * 1.8) + 32))
            forecast_temp_high = str(int((forecast.temperature[1] * 1.8) + 32))
            forecast_humid = str(int(forecast.humidity))
            status = (
                "%s,%s,%s,%s" % (
                    forecast_condition, forecast_temp_low, forecast_temp_high, forecast_humid))
            logger.debug("Data successfully obtained.  Returning [%s] to main" % status)
        except:
            logger.warning("Failure reading tomorrow's forecast data from NEST device")
            status = "??,??,??,??"
    else:
        logger.warning("Failure reading tomorrow's forecast data from NEST device")
        status = "??,??,??,??"
    # Re-define device with updated status
    device = rpihome_v3.Device(
        device.name, device.devtype, device.address,
        status, device.status_mem, str(datetime.datetime.now()),
        device.cmd, device.cmd_mem, device.rule)
    # Return result and nest connection for future use
    return device, nest

