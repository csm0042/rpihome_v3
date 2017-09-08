#!/usr/bin/python3
""" device.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import datetime
import logging
from .env import *
from rpihome_v3.helpers.ipv4_help import check_ipv4


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Search device list by name **************************************************
def search_device_list(log, devices, dev_name):
    """ function to search a list of items of Device class items and return
        the index of the item in the list that has a match in the dev_name
        element
    """
    # Configure logger
    log = log or logging.getLogger(__name__)
    log.debug('Starting search of device table for matching name: %s', dev_name)
    for i, d in enumerate(devices):
        if dev_name.lower() == d.dev_name.lower():
            log.debug('Match found at index: %s', i)
            return i
    log.debug('No match found for device name: %s', dev_name)
    return None


# Device Class Definition *****************************************************
class Device(object):
    """ Class used to define the objects and methods associated with a physical
    device that will be interfaced to/from this application """
    def __init__(self, log=None, **kwargs):
        # Configure logger
        self.log = log or logging.getLogger(__name__)
        
        # Create class instance objects
        self._dev_name = str()
        self._dev_type = str()
        self._dev_addr = str()
        self._dev_cmd = str()        
        self._dev_status = str()
        self._dev_last_seen = datetime.datetime
        self._dev_rule = str()
        
        # Process input variables if present
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "dev_name":
                    self.dev_name = value
                    self.log.debug('Device name set during __init__ '
                                   'to: %s', self.dev_name)
                if key == "dev_type":
                    self.dev_type = value
                    self.log.debug('Device type set during __init__ '
                                   'to: %s', self.dev_type)
                if key == "dev_addr":
                    self.dev_addr = value
                    self.log.debug('Device address set during __init__ '
                                   'to: %s', self.dev_addr)
                if key == "dev_cmd":
                    self.dev_cmd = value
                    self.log.debug('Device command set during __init__ '
                                   'to: %s', self.dev_cmd)
                if key == "dev_status":
                    self.dev_status = value
                    self.log.debug('Device status set during __init__ '
                                   'to: %s', self.dev_status)
                if key == "dev_last_seen":
                    self.dev_last_seen = value
                    self.log.debug('Device last seen set during __init__ '
                                   'to: %s', self.dev_last_seen)
                if key == "dev_rule":
                    self.dev_rule = value
                    self.log.debug('Device rule set during __init__ '
                                   'to: %s', self.dev_rule)

    # device name field *******************************************************
    @property
    def dev_name(self):
        self.log.debug('Returning current device name: %s', self._dev_name)
        return self._dev_name

    @dev_name.setter
    def dev_name(self, value):
        if isinstance(value, str):
            self._dev_name = value.lower()
        else:
            self._dev_name = (str(value)).lower()
        self.log.debug('Device name updated to: %s', self._dev_name)

    # device type field *******************************************************
    @property
    def dev_type(self):
        self.log.debug('Returning current device type: %s', self._dev_type)
        return self._dev_type

    @dev_type.setter
    def dev_type(self, value):
        if isinstance(value, str):
            self._dev_type = value.lower()
        else:
            self._dev_type = (str(value)).lower()
        self.log.debug('Device type updated to: %s', self._dev_type)

    # device address field ****************************************************
    @property
    def dev_addr(self):
        self.log.debug('Returning current device address: %s', self._dev_addr)
        return self._dev_addr

    @dev_addr.setter
    def dev_addr(self, value):
        if isinstance(value, str):
            if check_ipv4(value) is True:
                self._dev_addr = value
                self.log.debug('Device address updated to: %s', self._dev_addr)
            else:
                self.log.warning('Invalid address: %s', value)
        else:
            if check_ipv4(str(value)) is True:
                self._dev_addr = str(value)
                self.log.debug('Device address updated to: %s', self._dev_addr)
            else:
                self.log.warning('Invalid address: %s', value)

    # device command field ****************************************************
    @property
    def dev_cmd(self):
        self.log.debug('Returning current device command: %s', self._dev_cmd)
        return self._dev_cmd

    @dev_cmd.setter
    def dev_cmd(self, value):
        if isinstance(value, str):
            self._dev_cmd = value.lower()
        else:
            self._dev_cmd = (str(value)).lower()
        self.log.debug('Device command updated to: %s', self._dev_cmd)

    # device status field *****************************************************
    @property
    def dev_status(self):
        self.log.debug('Returning current device status: %s', self._dev_status)
        return self._dev_status

    @dev_status.setter
    def dev_status(self, value):
        if isinstance(value, str):
            self._dev_status = value.lower()
        else:
            self._dev_status = (str(value)).lower()
        self.log.debug('Device status updated to: %s', self._dev_status)

    # device last seen field **************************************************
    @property
    def dev_last_seen(self):
        self.log.debug('Returning current device last seen: %s', self._dev_last_seen)
        return self._dev_last_seen

    @dev_last_seen.setter
    def dev_last_seen(self, value):
        if isinstance(value, datetime.datetime):
            self._dev_last_seen = (str(value))[:19]
        elif isinstance(value, datetime.time):
            self._dev_last_seen = (str(
                datetime.datetime.combine(
                    datetime.datetime.now().date(), value)))[:19]
        elif isinstance(value, datetime.date):
            self._dev_last_seen = (str(
                datetime.datetime.combine(
                    value, datetime.datetime.now().time())))[:19]
        if isinstance(value, str):
            if len(value) >= 19:
                self._dev_last_seen = value[:19]
            else:
                self._dev_last_seen = value
        self.log.debug('Device last seen updated to: %s', self._dev_last_seen)

    # device rule field *******************************************************
    @property
    def dev_rule(self):
        self.log.debug('Returning current device rule: %s', self._dev_rule)
        return self._dev_rule

    @dev_rule.setter
    def dev_rule(self, value):
        if isinstance(value, str):
            self._dev_rule = value.lower()
        else:
            self._dev_rule = (str(value)).lower()
        self.log.debug('Device rule updated to: %s', self._dev_rule)
