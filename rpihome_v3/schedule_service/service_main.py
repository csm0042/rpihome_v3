#!/usr/bin/python3
""" service_main.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import env
from rpihome_v3.schedule_service.int_to_schedule import process_sched_ccs


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
def service_main_task(log, ref_num, schedule, msg_in_que, msg_out_que,
                      message_types):
    """ task to handle the work the service is intended to do """
    while True:
        # Initialize result list
        out_msg_list = []

        if msg_in_que.qsize() > 0:
            log.debug('Getting Incoming message from queue')
            next_msg = msg_in_que.get_nowait()
            log.debug('Message pulled from queue: [%s]', next_msg)

            # Determine message type
            next_msg_split = next_msg.split(',')
            if len(next_msg_split) >= 6:
                log.debug('Extracting source address and message type')
                msg_source_addr = next_msg_split[1]
                msg_type = next_msg_split[5]
                log.debug('Source Address: %s', msg_source_addr)
                log.debug('Message Type: %s', msg_type)

            # Process messages from database service
            if msg_type == message_types['schedule_ccs']:
                log.debug('Message is a Check Command State (CCS) message')
                out_msg_list = process_sched_ccs(
                    log,
                    ref_num,
                    schedule,
                    next_msg,
                    message_types)

        # Que up response messages in outgoing msg que
        if len(out_msg_list) > 0:
            log.debug('Queueing response message(s)')
            for out_msg in out_msg_list:
                msg_out_que.put_nowait(out_msg)
                log.debug('Response message [%s] successfully queued',
                          out_msg)

        # Yield to other tasks for a while
        yield from asyncio.sleep(0.25)
