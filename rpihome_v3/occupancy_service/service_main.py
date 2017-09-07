#!/usr/bin/python3
""" service_main.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import datetime
import logging
import env
from rpihome_v3.occupancy_service.msg_processing import create_heartbeat_msg
from rpihome_v3.occupancy_service.msg_processing import process_heartbeat_msg


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
        self.occupancy_monitor = None
        self.msg_in_queue = None
        self.msg_out_queue = None
        self.service_addresses = []
        self.message_types = []
        self.last_check_hb = datetime.datetime.now()
        self.last_check_om = datetime.datetime.now()
        self.out_msg = str()
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
                if key == "om":
                    self.occupancy_monitor = value
                    self.log.debug('Occupancy monitor set during __init__ '
                                   'to: %s', self.occupancy_monitor)
                if key == "msg_in_queue":
                    self.msg_in_queue = value
                    self.log.debug('Message in queue set during __init__ '
                                   'to: %s', self.msg_in_queue)
                if key == "msg_out_queue":
                    self.msg_out_queue = value
                    self.log.debug('Message out queue set during __init__ '
                                   'to: %s', self.msg_out_queue)
                if key == "service_addresses":
                    self.service_addresses = value
                    self.log.debug('Service address list set during __init__ '
                                   'to: %s', self.service_addresses)
                if key == "message_types":
                    self.message_types = value
                    self.log.debug('Message type list set during __init__ '
                                   'to: %s', self.message_types)


    @asyncio.coroutine
    def run(self):
        """ task to handle the work the service is intended to do """
        self.log.info('Starting occupancy service main task')

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

                # Process heartbeat from remote service
                if self.msg_type == self.message_types['heartbeat']:
                    self.log.debug('Message is a heartbeat')
                    self.out_msg_list = process_heartbeat_msg(
                        self.log,
                        self.ref_num,
                        self.next_msg,
                        self.message_types)

                # Register new devices to monitor
                if self.msg_type == self.message_types['register_occupancy_device']:
                    self.log.debug('Message is a request to register a device for '
                                   'occupancy checking')
                    self.out_msg_list = yield from self.occupancy_monitor.register(
                        self.next_msg,
                        self.message_types)


                # Que up response messages in outgoing msg que
                if len(self.out_msg_list) > 0:
                    self.log.debug('Queueing response message(s)')
                    for self.out_msg in self.out_msg_list:
                        self.msg_out_queue.put_nowait(self.out_msg)
                        self.log.debug('Message [%s] successfully queued', self.out_msg)


            # PERIODIC TASKS
            # Periodically send heartbeats to other services
            if datetime.datetime.now() >= (self.last_check_hb + datetime.timedelta(seconds=5)):
                self.destinations = [
                    (self.service_addresses['automation_addr'], self.service_addresses['automation_port'])
                ]
                self.out_msg_list = create_heartbeat_msg(
                    self.log,
                    self.ref_num,
                    self.destinations,
                    self.service_addresses['occupancy_addr'],
                    self.service_addresses['occupancy_port'],
                    self.message_types)

                # Que up response messages in outgoing msg que
                if len(self.out_msg_list) > 0:
                    self.log.debug('Queueing response message(s)')
                    for self.out_msg in self.out_msg_list:
                        self.msg_out_queue.put_nowait(self.out_msg)
                        self.log.debug('Response message [%s] successfully queued',
                                       self.out_msg)

                # Update last-check
                self.last_check_hb = datetime.datetime.now()


            # PERIODIC TASKS
            # Periodically check state of devices
            if datetime.datetime.now() >= (self.last_check_om + datetime.timedelta(seconds=1)):
                self.log.debug('Performing occupancy check')
                self.out_msg_list = self.occupancy_monitor.check_all()

                # Que up response messages in outgoing msg que
                if len(self.out_msg_list) > 0:
                    self.log.debug('Queueing message(s)')
                    for self.out_msg in self.out_msg_list:
                        self.msg_out_queue.put_nowait(self.out_msg)
                        self.log.debug('Message [%s] successfully queued', self.out_msg)

                # Update last-check
                self.last_check_om = datetime.datetime.now()


            # Yield to other tasks for a while
            yield from asyncio.sleep(0.25)
