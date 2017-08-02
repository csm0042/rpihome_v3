#!/usr/bin/python3
""" db_service_workers.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import copy
import datetime
import logging
import sys
if __name__ == "__main__":
    sys.path.append("..")
import database_service as service



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

            log.debug('Splitting message into header / payload')
            next_msg_seg = next_msg.split(sep=',')
            msg_header = next_msg_seg[:5]
            msg_payload = next_msg_seg[5:]

            # Map header and payload to usable tags
            msg_ref = msg_header[0]
            msg_dest_addr = msg_header[1]
            msg_dest_port = msg_header[2]
            msg_source_addr = msg_header[3]
            msg_source_port = msg_header[4]
            msg_type = msg_payload[0]

            # Log Device status updates to database
            if msg_type == message_types['database_LSU']:
                log.debug('Message is a device status update')
                response_msg_list = yield from service.process_db_lsu(
                    log,
                    rNumGen,
                    database,
                    msg_header,
                    msg_payload,
                    message_types)

            # Query for unprocessed device commands
            if msg_type == message_types['database_RC']:
                log.debug('Msg is a device pending cmd query')
                response_msg_list = yield from service.process_db_rc(
                    log,
                    rNumGen,
                    database,
                    msg_source_addr,
                    msg_source_port,
                    msg_dest_addr,
                    msg_dest_port,
                    message_types)

            # Mark completed device commands as processed
            if msg_type == message_types['database_UC']:
                log.debug('Msg is a device cmd update')
                response_msg_list = yield from service.process_db_uc(
                    log,
                    rNumGen,
                    database,
                    msg_header,
                    msg_payload,
                    message_types)
        else:
            # Periodically check for pending commands
            if datetime.datetime.now() >= (last_check + datetime.timedelta(seconds=1)):
                # Device command not yet processed query
                log.debug('Performing periodic check of pending commands')
                response_msg_list = yield from service.process_db_rc(
                    log,
                    rNumGen,
                    database,
                    service_addresses['automation_addr'],
                    service_addresses['automation_port'],
                    service_addresses['database_addr'],
                    service_addresses['database_port'],
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
