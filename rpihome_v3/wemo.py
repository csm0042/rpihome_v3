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


# IPv4 Format helper function *************************************************
def check_ipv4(address):
    ipv4_regex = r'\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
                 r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
                 r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
                 r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
    if re.fullmatch(ipv4_regex, address) is not None:
        return True
    else:
        return False


# pywemo wrapper API **********************************************************
class WemoAPI(object):
    """ Class and methods necessary to read items from a google calendar  """
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.wemo_device = None
        self.wemo_port = None
        self.wemo_url = str()
        self.wemo_known = []
        self.result = None
        self.status = str()


    def wemo_discover(self, device):
        """ discovers wemo device on network based upon known IP address """
        if check_ipv4(device.address) is True:
            self.logger.debug('Valid IP address provided')
            # Attempt to discover wemo device
            try:
                self.wemo_device = None
                self.wemo_port = pywemo.ouimeaux_device.probe_wemo(device.address)
                self.logger.debug('Device discovered at port %s', self.wemo_port)
            except:
                self.wemo_port = None
                self.logger.debug('Failed to discover port for [%s]', device.name)
        else:
            self.wemo_port = None
            self.logger.debug('Invalid IP address in device attributes')
        # If port was found, create url for device and run discovery function
        if self.wemo_port is not None:
            self.wemo_url = 'http://%s:%i/setup.xml' % (device.address, self.wemo_port)
            self.logger.debug('Resulting URL: [%s]', self.wemo_url)
            try:
                self.wemo_device = pywemo.discovery.device_from_description(
                    self.wemo_url,
                    None)
                self.logger.debug('[%s] discovery successful', device.name)
            except:
                self.logger.debug('[%s] discovery failed', device.name)
                self.wemo_device = None
        else:
            self.wemo_device = None


    def wemo_read_status(self, device):
        self.logger.debug(
            'Querrying device [%s] at [%s], original status [%s / %s]',
            device.name,
            device.address,
            device.status,
            device.last_seen)
        # Check if device is already in the list of known wemo devices
        self.result = next(
            (index for index, wemodev in enumerate(self.wemo_known)
             if wemodev.name == device.name), None)
        # Point to existing list record or recently discovered device
        if self.result != None:
            self.wemo_device = self.wemo_known[self.result]
        else:
            self.wemo_discover(device)
        # Perform status query
        if self.wemo_device is not None:
            self.status = str(self.wemo_device.get_state(force_update=True))
            self.logger.debug(
                'Wemo device [%s] found with status [%s]',
                device.name, self.status)
            # Re-define device record based on response from status query
            device.status = copy.copy(self.status)
            device.last_seen = str(datetime.datetime.now())
            # If device was not previously in wemo list, add it for next time
            if self.result == None:
                self.wemo_known.append(copy.copy(self.wemo_device))
        else:
            self.status = 'offline'
            self.logger.debug(
                'Wemo device [%s] discovery failed.  Status set to [%s]',
                device.name, self.status)
            device.status = copy.copy(self.status)


    # Wemo set to on function *****************************************************
    def wemo_set_on(self, device):
        """ Send 'turn on' command to a specific wemo device """
        self.logger.debug(
            'Setting device [%s] at [%s], state to "on"',
            device.name,
            device.address)
        # Check if device is already in the list of known wemo devices
        self.result = next(
            (index for index, wemodev in enumerate(self.wemo_known)
             if wemodev.name == device.name), None)
        # Point to existing list record or recently discovered device
        if self.result == None:
            self.logger.debug('Device not in wemo list.  Running discovery')
            self.wemo_device = self.wemo_discover(device)
        else:
            self.logger.debug(
                'Device already in wemo list as [%s]',
                self.wemo_known[self.result])
            self.wemo_device = self.wemo_known[self.result]
        # Perform command, followed by status query
        if self.wemo_device is not None:
            self.wemo_device.on()
            self.status = 'on'
            self.logger.debug(
                '"on" command sent to wemo device [%s]', self.wemo_device.name)
            # Re-define device record based on response from status query
            device.status = copy.copy(self.status)
            device.last_seen = str(datetime.datetime.now())
            device.cmd = 'on'
            # If device was not previously in wemo list, add it for next time
            if self.result == None:
                self.wemo_known.append(copy.copy(self.wemo_device))
        else:
            self.status = 'offline'
            device.cmd = ''
            self.logger.debug(
                'Wemo device [%s] discovery failed.  Status set to [%s]',
                device.name, self.status)
            device.status = copy.copy(self.status)
            device.cmd = 'on'


    # Wemo set to off function ****************************************************
    def wemo_set_off(self, device):
        """ Send 'turn off' command to a specific wemo device """
        self.logger.debug(
            'Setting device [%s] at [%s], state to "off"',
            device.name,
            device.address)
        # Check if device is already in the list of known wemo devices
        self.result = next(
            (index for index, wemodev in enumerate(self.wemo_known)
             if wemodev.name == device.name), None)
        # Point to existing list record or recently discovered device
        if self.result == None:
            self.logger.debug('Device not in wemo list.  Running discovery')
            self.wemo_device = self.wemo_discover(device)
        else:
            self.logger.debug(
                'Device already in wemo list as [%s]',
                self.wemo_known[self.result])
            self.wemo_device = self.wemo_known[self.result]
        # Perform command, followed by status query
        if self.wemo_device is not None:
            self.wemo_device.off()
            self.status = 'off'
            self.logger.debug(
                '"off" command sent to wemo device [%s]', self.wemo_device.name)
            # Re-define device record based on response from status query
            device.status = copy.copy(self.status)
            device.last_seen = str(datetime.datetime.now())
            device.cmd = 'off'
            # If device was not previously in wemo list, add it for next time
            if self.result == None:
                self.wemo_known.append(copy.copy(self.wemo_device))
        else:
            self.status = 'offline'
            self.logger.debug(
                'Wemo device [%s] discovery failed.  Status set to [%s]',
                device.name, self.status)
            device.status = copy.copy(self.status)
            device.cmd =  ''
