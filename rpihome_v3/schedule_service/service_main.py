#!/usr/bin/python3
""" service_main.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import schedule_service as service


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
            log.debug('Splitting message into header / payload')
            next_msg_seg = next_msg.split(sep=',')

            # Split message into header and payload
            msg_header = next_msg_seg[:5]
            msg_payload = next_msg_seg[5:]

            # Map header and payload to usable tags
            msg_ref = msg_header[0]
            msg_dest_addr = msg_header[1]
            msg_dest_port = msg_header[2]
            msg_source_addr = msg_header[3]
            msg_source_port = msg_header[4]

            # Process messages from database service
            if msg_payload[0] == message_types['schedule_CCS']:
                log.debug('Message is a Check Command State (CCS) message')
                out_msg_list = service.process_sched_ccs(
                    log,
                    ref_num,
                    schedule,
                    msg_header,
                    msg_payload,
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
