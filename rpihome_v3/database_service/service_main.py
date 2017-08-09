#!/usr/bin/python3
""" db_service_workers.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import copy
import datetime
import logging
import sys
import env
from rpihome_v3.database_service.int_to_database import process_db_lsu
from rpihome_v3.database_service.int_to_database import process_db_rc
from rpihome_v3.database_service.int_to_database import process_db_uc
from rpihome_v3.messages.message_rc import RCmessage



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
@asyncio.coroutine
def service_main_task(log, rNumGen, database,
                      msg_in_queue, msg_out_queue,
                      service_addresses, message_types):
    """ task to handle the work the service is intended to do """
    # Initialize timestamp for periodic DB checks
    last_check = datetime.datetime.now()

    # Run main task loop
    while True:
        # Initialize result list
        response_msg_list = []

        # Check incoming message queue for any messages to process
        if msg_in_queue.qsize() > 0:
            log.debug('Getting Incoming message from queue')
            next_msg = msg_in_queue.get_nowait()
            log.debug('Message pulled from queue: [%s]', next_msg)

            # Determine message type
            if len(next_msg) >= 6:
                msg_source_addr = next_msg[1]
                msg_type = next_msg[5]

            # Log Device status updates to database
            if msg_type == message_types['database_lsu']:
                log.debug('Message is a device status update')
                response_msg_list = yield from process_db_lsu(
                    log,
                    rNumGen,
                    database,
                    next_msg,
                    message_types)

            # Query for unprocessed device commands
            if msg_type == message_types['database_rc']:
                log.debug('Msg is a device pending cmd query')
                response_msg_list = yield from process_db_rc(
                    log,
                    rNumGen,
                    database,
                    next_msg,
                    message_types)

            # Mark completed device commands as processed
            if msg_type == message_types['database_uc']:
                log.debug('Msg is a device cmd update')
                response_msg_list = yield from process_db_uc(
                    log,
                    rNumGen,
                    database,
                    next_msg,
                    message_types)
        else:
            # Periodically check for pending commands
            if datetime.datetime.now() >= (last_check + datetime.timedelta(seconds=1)):
                # Device command not yet processed query
                log.debug('Performing periodic check of pending commands')
                response_msg_list = yield from process_db_rc(
                    log,
                    rNumGen,
                    database,
                    RCmessage(
                        dest_addr=service_addresses['automation_addr'],
                        dest_port=service_addresses['automation_port'],
                        source_addr=service_addresses['database_addr'],
                        source_port=service_addresses['database_port']),
                    message_types)
                # Update timestamp
                last_check = datetime.datetime.now()

        # Que up response messages in outgoing msg que
        if len(response_msg_list) > 0:
            log.debug('Queueing response message(s)')
            for response_msg in response_msg_list:
                msg_out_queue.put_nowait(response_msg)
                log.debug('Response message [%s] successfully queued',
                          response_msg)

        # Yield to other tasks for a while
        yield from asyncio.sleep(0.25)
