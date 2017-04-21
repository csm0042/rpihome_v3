#!/usr/bin/python3
""" nest.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import configparser
import datetime
import linecache
import os
import sys
import time
import nest


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
    credential_file = configparser.ConfigParser()
    credential_file.read(credentials)
    username = credential_file['NEST']['username']
    password = credential_file['NEST']['password']

    # Login to Nest account
    logger.debug("Attempting to connect to NEST account")
    try:
        nest = nest.Nest(username, password)
        logger.debug("Connection successful")
    except:
        nest = None
        logger.error("Could not connect to NEST account")
    return nest


async def current_conditions(device, nest, credentials, logger):
    if nest is None:
        nest = connect_to_nest(device, credentials, logger)
    if nest is not None:
        logger.debug("Attempting to parse data on current conditons from NEST data")
        try:
            structure = nest.structures[0]
            current_temp = str(int((structure.weather.current.temperature * 1.8) + 32))
            current_condition = structure.weather.current.condition
            current_wind_dir = structure.weather.current.wind.direction
            current_humid = str(int(structure.weather.current.humidity))
            status = (
                "%s,%s,%s,%s" % (
                    current_condition, current_temp, current_wind_dir, current_humid))
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
