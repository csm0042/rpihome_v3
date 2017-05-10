#!/usr/bin/python3
""" wemo.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import copy
import datetime
import pywemo
import re
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


# Wemo discover / connect function ********************************************
async def wemo_discover(device, logger):
    """ discovers wemo device on network based upon known IP address """
    # Regular expression for a valid IPv4 address
    ipv4_regex = r'\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
                 r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
                 r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
                 r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'

    # Check if valid IP address was provided in device attributes
    if re.fullmatch(ipv4_regex, device.address) is not None:
        logger.debug('Valid IP address provided')
        # Attempt to discover wemo device
        try:
            wemo_device = None
            wemo_port = pywemo.ouimeaux_device.probe_wemo(device.address)
            logger.debug('Device discovered at port %s', wemo_port)
        except:
            wemo_port = None
            logger.debug('Failed to discover port for [%s]', device.name)
    else:
        wemo_port = None
        logger.debug('Invalid IP address in device attributes')

    # If port was found, create url for device and run discovery function
    if wemo_port is not None:
        wemo_url = 'http://%s:%i/setup.xml' % (device.address, wemo_port)
        logger.debug('Resulting URL: [%s]', wemo_url)
        try:
            wemo_device = pywemo.discovery.device_from_description(wemo_url, None)
            logger.debug('[%s] discovery successful', device.name)
            return wemo_device
        except:
            logger.debug('[%s] discovery failed', device.name)
            return None
    else:
        return None


# Wemo status check function **************************************************
async def wemo_read_status(device, wemo_list, logger):
    # Wemo devices get a status query message sent to detect if they are
    # on the network or not and what their current state is
    logger.debug(
        'Querrying device [%s] at [%s], original status [%s / %s]',
        device.name,
        device.address,
        device.status,
        device.last_seen)

    # Check if device is already in the list of known wemo devices
    result = next(
        (index for index, wemodev in enumerate(wemo_list)
         if wemodev.name == device.name), None)

    # Point to existing list record or recently discovered device
    if result == None:
        wemo_device = await wemo_discover(device, logger)
    else:
        wemo_device = wemo_list[result]

    # Perform status query
    if wemo_device is not None:
        status = str(wemo_device.get_state(force_update=True))
        logger.debug(
            'Wemo device [%s] found with status [%s]',
            device.name, status)
        # Re-define device record based on response from status query
        device = rpihome_v3.Device(
            device.name, device.devtype, device.address,
            status, device.status_mem, str(datetime.datetime.now()),
            device.cmd, device.cmd_mem, device.rule)
        # If device was not previously in wemo list, add it for next time
        if result == None:
            wemo_list.append(copy.copy(wemo_device))
    else:
        status = 'offline'
        logger.debug(
            'Wemo device [%s] discovery failed.  Status set to [%s]',
            device.name, status)
        device = rpihome_v3.Device(
            device.name, device.devtype, device.address,
            status, device.status_mem, str(datetime.datetime.now()),
            device.cmd, device.cmd_mem, device.rule)
    return device, wemo_list


# Wemo set to on function *****************************************************
async def wemo_set_on(device, wemo_list, logger):
    # Wemo devices get a status query message sent to detect if they are
    # on the network or not and what their current state is
    logger.debug(
        'Setting device [%s] at [%s], state to "on"',
        device.name,
        device.address)

    # Check if device is already in the list of known wemo devices
    result = next(
        (index for index, wemodev in enumerate(wemo_list)
         if wemodev.name == device.name), None)

    # Point to existing list record or recently discovered device
    if result == None:
        logger.debug('Device not in wemo list.  Running discovery')
        wemo_device = await wemo_discover(device, logger)
    else:
        logger.debug(
            'Device already in wemo list as [%s]',
            wemo_list[result])
        wemo_device = wemo_list[result]

    # Perform command, followed by status query
    if wemo_device is not None:
        wemo_device.on()
        status = '1'
        logger.debug(
            '"on" command sent to wemo device [%s]', wemo_device.name)
        # Re-define device record based on response from status query
        device = rpihome_v3.Device(
            device.name, device.devtype, device.address,
            status, device.status_mem, str(datetime.datetime.now()),
            device.cmd, device.cmd_mem, device.rule)
        # If device was not previously in wemo list, add it for next time
        if result == None:
            wemo_list.append(copy.copy(wemo_device))
    else:
        status = 'offline'
        logger.debug(
            'Wemo device [%s] discovery failed.  Status set to [%s]',
            device.name, status)
        device = rpihome_v3.Device(
            device.name, device.devtype, device.address,
            status, device.status_mem, str(datetime.datetime.now()),
            'on', device.cmd_mem, device.rule)
    return device, wemo_list


# Wemo set to off function ****************************************************
async def wemo_set_off(device, wemo_list, logger):
    # Wemo devices get a status query message sent to detect if they are
    # on the network or not and what their current state is
    logger.debug(
        'Setting device [%s] at [%s], state to "off"',
        device.name,
        device.address)

    # Check if device is already in the list of known wemo devices
    result = next(
        (index for index, wemodev in enumerate(wemo_list)
         if wemodev.name == device.name), None)

    # Point to existing list record or recently discovered device
    if result == None:
        logger.debug('Device not in wemo list.  Running discovery')
        wemo_device = await wemo_discover(device, logger)
    else:
        logger.debug(
            'Device already in wemo list as [%s]',
            wemo_list[result])
        wemo_device = wemo_list[result]

    # Perform command, followed by status query
    if wemo_device is not None:
        wemo_device.off()
        status = '0'
        logger.debug(
            '"off" command sent to wemo device [%s]', wemo_device.name)
        # Re-define device record based on response from status query
        device = rpihome_v3.Device(
            device.name, device.devtype, device.address,
            status, device.status_mem, str(datetime.datetime.now()),
            'off', device.cmd_mem, device.rule)
        # If device was not previously in wemo list, add it for next time
        if result == None:
            wemo_list.append(copy.copy(wemo_device))
    else:
        status = 'offline'
        logger.debug(
            'Wemo device [%s] discovery failed.  Status set to [%s]',
            device.name, status)
        device = rpihome_v3.Device(
            device.name, device.devtype, device.address,
            status, device.status_mem, str(datetime.datetime.now()),
            device.cmd, device.cmd_mem, device.rule)
    return device, wemo_list
