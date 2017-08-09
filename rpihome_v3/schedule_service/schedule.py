#!/usr/bin/python3
""" schedule.py:
"""

# Im_port Required Libraries (Standard, Third Party, Local) ********************
import datetime
import logging


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Schedule Class Definition ***************************************************
class Sched(object):
    """ Class used to define a schedule object used for automatic on/off control of
    devices that will be controlled from this application """
    def __init__(self, log=None, **kwargs):
        # Configure logger
        self.log = log or logging.getLogger(__name__)

        # Create class instance objects
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
        self._name = value.lower()

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
        elif isinstance(value, datetime.date):
            self._start = datetime.datetime.combine(
                value,
                datetime.datetime.now().time()
            )
        elif isinstance(value, datetime.time):
            self._start = datetime.datetime.combine(
                datetime.datetime.now().date(),
                value
            )


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
        elif isinstance(value, datetime.date):
            self._end = datetime.datetime.combine(
                value,
                datetime.datetime.now().time()
            )
        elif isinstance(value, datetime.time):
            self._end = datetime.datetime.combine(
                datetime.datetime.now().date(),
                value
            )
            