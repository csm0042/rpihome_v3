#!/usr/bin/python3
""" rpihome_v3 module init
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
from .automation_rules import *
from .configure import *
from .dst import *
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


# Defined named tuples for various object types *******************************
class Device(object):
    def __init__(self, logger=None, **kwargs):
        # Configure logger
        self.logger = logger or logging.getLogger(__name__)
        self._name = str()
        self._devtype = str()
        self._address = str()
        self._status = str()
        self._status_mem = str()
        self._last_seen = str()
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
        self._last_seen = str(value)

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


class Sched(object):
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
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        if isinstance(value, datetime.datetime):
            self._start = value

    @property
    def end(self):
        return self._start

    @end.setter
    def end(self, value):
        if isinstance(value, datetime.datetime):
            self._end = value
