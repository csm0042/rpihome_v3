#!/usr/bin/python3
""" wemo_service_main.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import datetime
import logging
import env
from rpihome_v3.messages.heartbeat import HeartbeatMessage
from rpihome_v3.wemo_service.msg_processing import reply_to_hb
from rpihome_v3.wemo_service.msg_processing import get_wemo_state
from rpihome_v3.wemo_service.msg_processing import set_wemo_state



# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Internal Service Work Task **************************************************
class MainTask(object):
    def __init__(self, log, **kwargs):
        # Configure logger
        self.log = log or logging.getLogger(__name__)
        # Define instance variables
        self.ref_num = None
        self.gateway = None
        self.msg_in_queue = None
        self.msg_out_queue = None
        self.service_addresses = []
        self.message_types = []
        self.last_check = datetime.datetime.now()
        self.out_msg_list = []
        self.next_msg = str()
        self.next_msg_split = []
        self.msg_source_addr = str()
        self.msg_type = str()
        # Map input variables
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "ref":
                    self.ref_num = value
                    self.log.debug('Ref number generator set during __init__ '
                                   'to: %s', self.ref_num)
                if key == "gw":
                    self.gateway = value
                    self.log.debug('Device gateway set during __init__ '
                                   'to: %s', self.ref_num)
                if key == "msg_in_queue":
                    self.msg_in_queue = value
                    self.log.debug('Message in queue set during __init__ '
                                   'to: %s', self.ref_num)
                if key == "msg_out_queue":
                    self.msg_out_queue = value
                    self.log.debug('Message out queue set during __init__ '
                                   'to: %s', self.ref_num)
                if key == "service_addresses":
                    self.service_addresses = value
                    self.log.debug('Service address list set during __init__ '
                                   'to: %s', self.ref_num)
                if key == "message_types":
                    self.message_types = value
                    self.log.debug('Message type list set during __init__ '
                                   'to: %s', self.ref_num)

    @asyncio.coroutine
    def run(self):
        """ task to handle the work the service is intended to do """

        while True:
            # Initialize result list
            self.out_msg_list = []

            # INCOMING MESSAGE HANDLING
            if self.msg_in_queue.qsize() > 0:
                self.log.debug('Getting Incoming message from queue')
                self.next_msg = self.msg_in_queue.get_nowait()
                self.log.debug('Message pulled from queue: [%s]', self.next_msg)

                # Determine message type
                self.next_msg_split = self.next_msg.split(',')
                if len(self.next_msg_split) >= 6:
                    self.log.debug('Extracting source address and message type')
                    self.msg_source_addr = self.next_msg_split[1]
                    self.msg_type = self.next_msg_split[5]
                    self.log.debug('Source Address: %s', self.msg_source_addr)
                    self.log.debug('Message Type: %s', self.msg_type)

                # Wemo Service Check
                if self.msg_type == self.message_types['heartbeat']:
                    self.log.debug('Message is a heartbeat')
                    self.out_msg_list = yield from reply_to_hb(
                        self.log,
                        self.ref_num,
                        self.next_msg,
                        self.message_types)

                # Wemo Device Status Queries
                if self.msg_type == self.message_types['get_device_state']:
                    self.log.debug('Message is a device status update request')
                    self.out_msg_list = yield from get_wemo_state(
                        self.log,
                        self.ref_num,
                        self.gateway,
                        self.next_msg,
                        self.message_types)

                # Wemo Device set state commands
                if self.msg_type == self.message_types['set_device_state']:
                    self.log.debug('Message is a device set state command')
                    self.out_msg_list = yield from set_wemo_state(
                        self.log,
                        self.ref_num,
                        self.gateway,
                        self.next_msg,
                        self.message_types)

            # PERIODIC TASKS
            if datetime.datetime.now() >= (self.last_check + datetime.timedelta(seconds=5)):
                # Send heartbeat to automation task
                self.out_msg_list.append(
                    HeartbeatMessage(
                        log=self.log,
                        ref=self.ref_num.new(),
                        dest_addr=self.service_addresses['automation_addr'],
                        dest_port=self.service_addresses['automation_port'],
                        source_addr=self.service_addresses['wemo_addr'],
                        source_port=self.service_addresses['wemo_port'],
                        msg_type=self.message_types['heartbeat']
                    ).complete
                )
                # Update last-check
                self.last_check = datetime.datetime.now()

            # OUTGOING MESSAGE HANDLING
            if len(self.out_msg_list) > 0:
                self.log.debug('Queueing response message(s)')
                for out_msg in self.out_msg_list:
                    self.msg_out_queue.put_nowait(out_msg)
                    self.log.debug('Response message [%s] successfully queued',
                                   out_msg)

            # Yield to other tasks for a while
            yield from asyncio.sleep(0.25)
