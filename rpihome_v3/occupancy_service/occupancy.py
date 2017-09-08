#!/usr/bin/python3
""" occupancy.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import copy
import sys
from .env import *
from rpihome_v3.helpers.ref_num import RefNum
from rpihome_v3.messages.register_occupancy_device import RegisterOccupancyDeviceMessage
from rpihome_v3.messages.register_occupancy_device_ack import RegisterOccupancyDeviceMessageACK


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Message Handler Class Def ***************************************************
class OccupancyMonitor(object):
    def __init__(self, log, watch_folder, msg_types):
        self.log = log
        self.watch_folder = watch_folder
        self.msg = RegisterOccupancyDeviceMessage
        self.device_list = []


    def register(self, msg):
        # Load raw message into class for ease of decoding
        self.msg.complete = msg
        # If device name not already in list, add it
        if msg.name.lower() not in self.device_list:
            self.device_list.append(copy.copy(msg.name.lower()))
        # ACK original message to confirm receipt and processing
        return RegisterOccupancyDeviceMessage(
            ref=msg.ref,
            dest_addr=msg.source_addr,
            dest_port=msg.source_port,
            source_addr=msg.dest_addr,
            source_port=msg.dest_port,
            msg_type=msg.msg_type,
            dev_name=msg.dev_name
            )


    def check_all(self):
        pass
        return []
