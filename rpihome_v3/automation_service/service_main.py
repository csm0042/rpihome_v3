#!/usr/bin/python3
""" service_main.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import datetime
import logging
if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from rpihome_v3.automation_service.msg_processing import create_heartbeat_msg
from rpihome_v3.automation_service.msg_processing import process_heartbeat_msg

from rpihome_v3.automation_service.msg_processing_db import process_log_status_update_msg
from rpihome_v3.automation_service.msg_processing_db import process_log_status_update_msg_ack
from rpihome_v3.automation_service.msg_processing_db import process_return_command_msg
from rpihome_v3.automation_service.msg_processing_db import process_return_command_msg_ack
from rpihome_v3.automation_service.msg_processing_db import process_update_command_msg
from rpihome_v3.automation_service.msg_processing_db import process_update_command_msg_ack

from rpihome_v3.automation_service.msg_processing_wemo import process_get_device_state_msg
from rpihome_v3.automation_service.msg_processing_wemo import process_get_device_state_msg_ack
from rpihome_v3.automation_service.msg_processing_wemo import process_set_device_state_msg
from rpihome_v3.automation_service.msg_processing_wemo import process_set_device_state_msg_ack

from rpihome_v3.automation_service.msg_processing_schedule import create_get_device_scheduled_state_msg
from rpihome_v3.automation_service.msg_processing_schedule import process_get_device_scheduled_state_msg
from rpihome_v3.automation_service.msg_processing_schedule import process_get_device_scheduled_state_msg_ack


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
        self.devices = None
        self.msg_in_queue = None
        self.msg_out_queue = None
        self.service_addresses = []
        self.message_types = []
        self.last_check_schedule = datetime.datetime.now()
        self.last_check_hb = datetime.datetime.now()
        self.out_msg = str()
        self.out_msg_list = []
        self.next_msg = str()
        self.next_msg_split = []
        self.msg_source_addr = str()
        self.msg_type = str()
        self.destinations = []
        # Map input variables
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "ref":
                    self.ref_num = value
                    self.log.debug('Ref number generator set during __init__ '
                                   'to: %s', self.ref_num)
                if key == "devices":
                    self.devices = value
                    self.log.debug('Device list set during __init__ '
                                   'to: %s', self.devices)
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
        self.log.info('Starting automation service main task')

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

                # Process messages from database service
                if self.msg_source_addr == self.service_addresses['database_addr']:

                    # Process log status update message
                    if self.msg_type == self.message_types['log_status_update']:
                        self.log.debug('Message is a Log Status Update message')
                        self.out_msg_list = process_log_status_update_msg(
                            self.log,
                            self.next_msg,
                            self.service_addresses)

                    # # Process log status update ACK message
                    elif self.msg_type == self.message_types['log_status_update_ack']:
                        self.log.debug('Message is a Log Status Update ACK message')
                        process_log_status_update_msg_ack(
                            self.log,
                            self.next_msg)

                    # Process return command message
                    elif self.msg_type == self.message_types['return_command']:
                        self.log.debug('Message is a Return Command (RC) message')
                        self.out_msg_list = process_return_command_msg(
                            self.log,
                            self.next_msg,
                            self.service_addresses)

                    # Process return command ACK message
                    elif self.msg_type == self.message_types['return_command_ack']:
                        self.log.debug('Message is a Return Command ACK (RCA) message')
                        self.out_msg_list = process_return_command_msg_ack(
                            self.log,
                            self.ref_num,
                            self.devices,
                            self.next_msg,
                            self.service_addresses,
                            self.message_types)

                    # Process update command message
                    elif self.msg_type == self.message_types['update_command']:
                        self.log.debug('Message is a Update Command (UC) message')
                        self.out_msg_list = process_update_command_msg(
                            self.log,
                            self.next_msg,
                            self.service_addresses)

                    # Process update command ACK message
                    elif self.msg_type == self.message_types['update_command_ack']:
                        self.log.debug('Message is a Update Command ACK (UCA) message')
                        process_update_command_msg_ack(
                            self.log,
                            self.next_msg)

                # Process messages from wemo service
                if self.msg_source_addr == self.service_addresses['wemo_addr']:

                    # Process get device state message
                    if self.msg_type == self.message_types['get_device_state']:
                        self.log.debug('Message is a Get Device Status (GDS) message')
                        self.out_msg_list = process_get_device_state_msg(
                            self.log,
                            self.devices,
                            self.next_msg,
                            self.service_addresses)

                    # Process get device state ACK message
                    elif self.msg_type == self.message_types['get_device_state_ack']:
                        self.log.debug('Message is a Get Device Status ACK (GDSA) message')
                        self.out_msg_list = process_get_device_state_msg_ack(
                            self.log,
                            self.devices,
                            self.next_msg)

                    # Process set device state message
                    elif self.msg_type == self.message_types['set_device_state']:
                        self.log.debug('Message is a Set Device Status (SDS) message')
                        self.out_msg_list = process_set_device_state_msg(
                            self.log,
                            self.devices,
                            self.next_msg,
                            self.service_addresses)

                    # Process set device state ACK message
                    elif self.msg_type == self.message_types['set_device_state_ack']:
                        self.log.debug('Message is a Set Device Status ACK (SDSA) message')
                        self.out_msg_list = process_set_device_state_msg_ack(
                            self.log,
                            self.devices,
                            self.next_msg)

                # Process messages from calendar/schedule service
                if self.msg_source_addr == self.service_addresses['schedule_addr']:

                    # Process get device scheduled state message
                    if self.msg_type == self.message_types['get_device_scheduled_state']:
                        self.log.debug('Message is a get device scheduled state message')
                        self.out_msg_list = process_get_device_scheduled_state_msg(
                            self.log,
                            self.devices,
                            self.next_msg,
                            self.service_addresses)

                    # Process get device scheduled state ACK message
                    if self.msg_type == self.message_types['get_device_scheduled_state_ack']:
                        self.log.debug('Message is a get device scheduled state ACK message')
                        self.out_msg_list = process_get_device_scheduled_state_msg_ack(
                            self.log,
                            self.ref_num,
                            self.devices,
                            self.next_msg,
                            self.service_addresses,
                            self.message_types)

                # Que up response messages in outgoing msg que
                if len(self.out_msg_list) > 0:
                    self.log.debug('Queueing response message(s)')
                    for self.out_msg in self.out_msg_list:
                        self.msg_out_queue.put_nowait(self.out_msg)
                        self.log.debug('Message [%s] successfully queued', self.out_msg)


            # PERIODIC TASKS
            # Periodically send heartbeats to other services
            if datetime.datetime.now() >= (self.last_check_hb + datetime.timedelta(seconds=120)):
                self.destinations = [
                    (self.service_addresses['database_addr'], self.service_addresses['database_port']),
                    (self.service_addresses['motion_addr'], self.service_addresses['motion_port']),
                    (self.service_addresses['nest_addr'], self.service_addresses['nest_port']),
                    (self.service_addresses['occupancy_addr'], self.service_addresses['occupancy_port']),
                    (self.service_addresses['schedule_addr'], self.service_addresses['schedule_port']),
                    (self.service_addresses['wemo_addr'], self.service_addresses['wemo_port'])
                ]
                self.out_msg_list = create_heartbeat_msg(
                    self.log,
                    self.ref_num,
                    self.destinations,
                    self.service_addresses['automation_addr'],
                    self.service_addresses['automation_port'],
                    self.message_types)

                # Que up response messages in outgoing msg que
                if len(self.out_msg_list) > 0:
                    self.log.debug('Queueing message(s)')
                    for self.out_msg in self.out_msg_list:
                        self.msg_out_queue.put_nowait(self.out_msg)
                        self.log.debug('Message [%s] successfully queued', self.out_msg)

                # Update last-check
                self.last_check_hb = datetime.datetime.now()


            # PERIODIC TASKS
            # Periodically check scheduled on/off commands for devices
            if datetime.datetime.now() >= (self.last_check_schedule + datetime.timedelta(minutes=1)):
                self.out_msg_list = create_get_device_scheduled_state_msg(
                    self.log,
                    self.ref_num,
                    self.devices,
                    self.service_addresses,
                    self.message_types)

                # Que up response messages in outgoing msg que
                if len(self.out_msg_list) > 0:
                    self.log.debug('Queueing message(s)')
                    for self.out_msg in self.out_msg_list:
                        self.msg_out_queue.put_nowait(self.out_msg)
                        self.log.debug('Message [%s] successfully queued', self.out_msg)

                # Update last-check
                self.last_check_schedule = datetime.datetime.now()




            # Yield to other tasks for a while
            yield from asyncio.sleep(0.25)
