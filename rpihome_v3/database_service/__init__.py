#!/usr/bin/python3
""" wemo_server module init
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
from .configure import *
from .database import *
from .log_support import *



class DeviceCmd(object):
    """ Class used to define the objects and methods associated with a physical
    device that will be interfaced to/from this application """
    def __init__(self, logger=None, **kwargs):
        # Configure logger
        self.logger = logger or logging.getLogger(__name__)
        self._id_dev = str()
        self._name = str()
        self._cmd = str()
        self._timestamp = str()
        self._processed = str()
        # Process input variables if present
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "id_dev":
                    self.id_dev = value
                if key == "name":
                    self.name = value                    
                if key == "cmd":
                    self.cmd = value
                if key == "address":
                    self.address = value
                if key == "timestamp":
                    self.timestamp = value
                if key == "processed":
                    self.processed = value

    @property
    def id_dev(self):
        return self._id_dev

    @id_dev.setter
    def id_dev(self, value):
        self._id_dev = str(value)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = str(value)

    @property
    def cmd(self):
        return self._cmd

    @cmd.setter
    def cmd(self, value):
        self._cmd = str(value)

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = str(value)

    @property
    def processed(self):
        return self._processed

    @processed.setter
    def processed(self, value):
        self._processed = str(value)
