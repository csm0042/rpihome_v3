#!/usr/bin/python3
""" rpihome_v3 module init
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
from .automation_rules import *
from .configure import *
from .dst import *
from .event_loop import *
from .goog_cal import *
from .log_support import *
from .motion import *
from .nest import *
from .persistance import *
from .ping import *
from .sun import *
from .tasks import *
from .wemo import *


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Device Class Definition *****************************************************
class Device(object):
    """ Class used to define the objects and methods associated with a physical
    device that will be interfaced to/from this application """
    def __init__(self, logger=None, **kwargs):
        # Configure logger
        self.logger = logger or logging.getLogger(__name__)
        self._name = str()
        self._devtype = str()
        self._address = str()
        self._status = str()
        self._status_mem = str()
        self._last_seen = datetime.datetime
        self._cmd = str()
        self._rule = str()
        # Process input variables if present
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "name":
                    self.name = value
                if key == "devtype":
                    self.devtype = value
                if key == "address":
                    self.address = value
                if key == "status":
                    self.status = value
                if key == "last_seen":
                    self.last_seen = value
                if key == "cmd":
                    self.cmd = value
                if key == "rule":
                    self.rule = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = str(value)

    @property
    def devtype(self):
        return self._devtype

    @devtype.setter
    def devtype(self, value):
        self._devtype = str(value)

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = str(value)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = str(value)

    @property
    def status_mem(self):
        return self._status_mem

    @status_mem.setter
    def status_mem(self, value):
        self._status_mem = str(value)

    @property
    def last_seen(self):
        return self._last_seen

    @last_seen.setter
    def last_seen(self, value):
        if isinstance(value, datetime.datetime):
            self._last_seen = value

    @property
    def cmd(self):
        return self._cmd

    @cmd.setter
    def cmd(self, value):
        self._cmd = str(value)

    @property
    def rule(self):
        return self._rule

    @rule.setter
    def rule(self, value):
        self._rule = str(value)


# Schedule Class Definition ***************************************************
class Sched(object):
    """ Class used to define a schedule object used for automatic on/off control of
    devices that will be controlled from this application """
    def __init__(self, logger=None, **kwargs):
        # Configure logger
        self.logger = logger or logging.getLogger(__name__)
        self._name = str()
        self._start = datetime.datetime
        self._end = datetime.datetime
        # Process input variables if present
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "name":
                    self.name = value
                if key == "start":
                    self.start = value
                if key == "end":
                    self.end = value

    @property
    def name(self):
        """ returns the name of the device this schedule items is
        associated with """
        return self._name

    @name.setter
    def name(self, value):
        """ setter for the device name this schedule item corresponds
        to """
        self._name = value

    @property
    def start(self):
        """ returns "start" time associated with this line-item on the
        schedule.  This typically corresponds to the time the device
        is to be set to its non-default state (usually on) """
        return self._start

    @start.setter
    def start(self, value):
        """ setter used to verify only proper data is entered into
        the "start" time field """
        if isinstance(value, datetime.datetime):
            self._start = value

    @property
    def end(self):
        """ returns "end" time associated with this line-item on the
        schedule.  This typically corresponds to the time the device
        is to be returned to its default state (usually off) """
        return self._end

    @end.setter
    def end(self, value):
        """ setter used to verify only proper data is entered into
        the "end" time field """
        if isinstance(value, datetime.datetime):
            self._end = value
