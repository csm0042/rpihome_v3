#!/usr/bin/python3
""" tuples.py

"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import typing
import datetime


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
class Device(typing.NamedTuple):
    name: str
    devtype: str
    address: str
    status: str
    status_mem: str
    last_seen: str
    cmd: str
    cmd_mem: str
    rule: str


class Sched(typing.NamedTuple):
    name: str
    start: datetime.datetime
    end: datetime.datetime
