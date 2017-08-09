#!/usr/bin/python3
""" message_gds_ack.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import datetime
import logging
import env
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


# Message Class Definition ****************************************************
class GDSACKmessage(object):
    """ Log Status Update message class and methods """
    def __init__(self, log=None, **kwargs):
        # Configure logger
        self.log = log or logging.getLogger(__name__)
        self._ref = str()
        self._dest_addr = str()
        self._dest_port = str()
        self._source_addr = str()
        self._source_port = str()
        self._msg_type = str()
        self._dev_name = str()
        self._dev_status = str()
        self._dev_last_seen = str()
        self.temp_list = []
        # Process input variables if present
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "ref":
                    self.ref = value
                    self.log.debug('Ref Number value set during '
                                   '__init__ to: %s', self.ref)
                if key == "dest_addr":
                    self.dest_addr = value
                    self.log.debug('Destination address value set during __init__ '
                                   'to: %s', self.dest_addr)
                if key == "dest_port":
                    self.dest_port = value
                    self.log.debug('Destination port value set during __init__ '
                                   'to: %s', self.dest_port)
                if key == "source_addr":
                    self.source_addr = value
                    self.log.debug('Source address value set during __init__ '
                                   'to: %s', self.source_addr)
                if key == "source_port":
                    self.source_port = value
                    self.log.debug('Source port value set during __init__ to: '
                                   '%s', self.source_port)
                if key == "msg_type":
                    self.msg_type = value
                    self.log.debug('Message type value set during __init__ to: '
                                   '%s', self.msg_type)
                if key == "dev_name":
                    self.dev_name = value
                    self.log.debug('Device name value set during __init__ to: '
                                   '%s', self.dev_name)
                if key == "dev_addr":
                    self.dev_addr = value
                    self.log.debug('Device Address value set during __init__ '
                                   'to: %s', self.dev_addr)
                if key == "dev_status":
                    self.dev_status = value
                    self.log.debug('Device Status value set during __init__ '
                                   'to: %s', self.dev_status)                                   
                if key == "dev_last_seen":
                    self.dev_last_seen = value
                    self.log.debug('Device last seen value set during __init__ '
                                   'to: %s', self.dev_last_seen)

    # ref number field ********************************************************
    @property
    def ref(self):
        self.log.debug('Returning current value of ref number: %s', self._ref)
        return self._ref

    @ref.setter
    def ref(self, value):
        if isinstance(value, str):
            self._ref = value
        else:
            self._ref = str(value)
        self.log.debug('Ref number value updated to: %s', self._ref)

    # destination address *****************************************************
    @property
    def dest_addr(self):
        self.log.debug('Returning current value of destination address: '
                       '%s', self._dest_addr)
        return self._dest_addr

    @dest_addr.setter
    def dest_addr(self, value):
        if isinstance(value, str):
            if check_ipv4(value) is True:
                self._dest_addr = value
                self.log.debug('Destination address value updated to: '
                               '%s', self._dest_addr)
            else:
                self.log.warning('Invalid address provided for destination '
                                 'address: %s', value)
        else:
            if check_ipv4(str(value)) is True:
                self._dest_addr = str(value)
                self.log.debug('Destination address value updated to: '
                               '%s', self._dest_addr)
            else:
                self.log.warning('Invalid address provided for destination '
                                 'address: %s', value)

    # destination port ********************************************************
    @property
    def dest_port(self):
        self.log.debug('Returning current value of destination port: '
                       '%s', self._dest_port)
        return self._dest_port

    @dest_port.setter
    def dest_port(self, value):
        if isinstance(value, str):
            try:
                if 10000 <= int(value) <= 60000:
                    self._dest_port = value
                    self.log.debug('Destination port value updated to: '
                                '%s', self._dest_port)
                else:
                    self.log.warning('Invalid port number provided for '
                                    'destination port: %s', value)
            except Exception:
                self.log.warning('Invalid port number provided for '
                                 'destination port: %s', value)
        elif isinstance(value, int):
            if 10000 <= value <= 60000:
                self._dest_port = str(value)
                self.log.debug('Destination port value updated to: '
                               '%s', self._dest_port)
            else:
                self.log.warning('Invalid port number provided for '
                                 'destination port: %s', value)
        else:
            self.log.warning('Invalid port number rovided for '
                             'destination port: %s', value)

    # source address field ****************************************************
    @property
    def source_addr(self):
        self.log.debug('Returning current value of source address: '
                       '%s', self._source_addr)
        return self._source_addr

    @source_addr.setter
    def source_addr(self, value):
        if isinstance(value, str):
            if check_ipv4(value) is True:
                self._source_addr = value
                self.log.debug('source address value updated to: '
                               '%s', self._source_addr)
            else:
                self.log.warning('Invalid address provided for source '
                                 'address: %s', value)
        else:
            if check_ipv4(str(value)) is True:
                self._source_addr = str(value)
                self.log.debug('source address value updated to: '
                               '%s', self._source_addr)
            else:
                self.log.warning('Invalid address provided for source '
                                 'address: %s', value)

    # source port field *******************************************************
    @property
    def source_port(self):
        self.log.debug('Returning current value of source port: '
                       '%s', self._source_port)
        return self._source_port

    @source_port.setter
    def source_port(self, value):
        if isinstance(value, str):
            try:
                if 10000 <= int(value) <= 60000:
                    self._source_port = value
                    self.log.debug('Source port value updated to: '
                                '%s', self._source_port)
                else:
                    self.log.warning('Invalid port number provided for '
                                    'Source port: %s', value)
            except Exception:
                self.log.warning('Invalid port number provided for '
                                 'Source port: %s', value)
        elif isinstance(value, int):
            if 10000 <= value <= 60000:
                self._source_port = str(value)
                self.log.debug('Source port value updated to: '
                               '%s', self._source_port)
            else:
                self.log.warning('Invalid port number provided for '
                                 'Source port: %s', value)
        else:
            self.log.warning('Invalid port number rovided for '
                             'Source port: %s', value)

    # message type field ******************************************************
    @property
    def msg_type(self):
        self.log.debug('Returning current value of message type: '
                       '%s', self._msg_type)
        return self._msg_type

    @msg_type.setter
    def msg_type(self, value):
        if isinstance(value, str):
            self._msg_type = value
        else:
            self._msg_type = str(value)
        self.log.debug('Message type value updated to: '
                       '%s', self._msg_type)

    # device name field *******************************************************
    @property
    def dev_name(self):
        self.log.debug('Returning current value of device name: '
                       '%s', self._dev_name)
        return self._dev_name

    @dev_name.setter
    def dev_name(self, value):
        if isinstance(value, str):
            self._dev_name = value
        else:
            self._dev_name = str(value)
        self.log.debug('Device name value updated to: '
                       '%s', self._dev_name)

    # device status field *****************************************************
    @property
    def dev_status(self):
        self.log.debug('Returning current value of device status: '
                       '%s', self._dev_status)
        return self._dev_status

    @dev_status.setter
    def dev_status(self, value):
        if isinstance(value, str):
            self._dev_status = value.lower()
        else:
            self._dev_status = (str(value)).lower()
        self.log.debug('Device status value updated to: '
                       '%s', self._dev_status)

    # device last seen field **************************************************
    @property
    def dev_last_seen(self):
        self.log.debug('Returning current value of device last seen: '
                       '%s', self._dev_last_seen)
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
        self.log.debug('Device last seen value updated to: '
                       '%s', self._dev_last_seen)

    # complete message encode/decode methods **********************************
    @property
    def complete(self):
        self.log.debug('Returning current value of complete message: '
                       '%s,%s,%s,%s,%s,%s,%s,%s,%s',
                       self._ref, self._dest_addr, self._dest_port,
                       self._source_addr, self._source_port,
                       self._msg_type, self._dev_name,
                       self._dev_status, self._dev_last_seen)
        return '%s,%s,%s,%s,%s,%s,%s,%s,%s' % (
            self._ref, self._dest_addr, self._dest_port,
            self._source_addr, self._source_port,
            self._msg_type, self._dev_name,
            self._dev_status, self._dev_last_seen)

    @complete.setter
    def complete(self, value):
        if isinstance(value, str):
            self.temp_list = value.split(',')
            if len(self.temp_list) == 9:
                self.log.debug('Message was properly formatted for decoding')
                self.ref = self.temp_list[0]
                self.dest_addr = self.temp_list[1]
                self.dest_port = self.temp_list[2]
                self.source_addr = self.temp_list[3]
                self.source_port = self.temp_list[4]
                self.msg_type = self.temp_list[5]
                self.dev_name = self.temp_list[6]
                self.dev_status = self.temp_list[7]
                self.dev_last_seen = self.temp_list[8]
