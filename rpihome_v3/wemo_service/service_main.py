#!/usr/bin/python3
""" wemo_service_workers.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import copy
import logging
import sys
import time
import wemo_service as service


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
def service_main_task(log, ref_num, wemo_gw, msg_in_que, msg_out_que, message_types):
    """ task to handle the work the service is intended to do """
    while True:
        # Initialize result list
        response_msg_list = []

        if msg_in_que.qsize() > 0:
            log.debug('Getting Incoming message from queue')
            next_msg = msg_in_que.get_nowait()
            log.debug('Message pulled from queue: [%s]', next_msg)
            
            # Split message into header and payload
            log.debug('Splitting message into header / payload')            
            next_msg_seg = next_msg.split(sep=',')
            msg_header = next_msg_seg[:5]
            log.debug('Split off message header: [%s]', msg_header)
            msg_payload = next_msg_seg[5:]
            log.debug('Split off message payload: [%s]', msg_payload)

            # Wemo Device Status Queries
            if msg_payload[0] == message_types['wemo_gds']:
                log.debug('Message is a device status update request')
                response_msg_list = yield from service.get_wemo_status(
                    log,
                    ref_num,
                    wemo_gw,
                    msg_header,
                    msg_payload,
                    message_types)

            # Wemo Device set state commands
            if msg_payload[0] == message_types['wemo_sds']:
                log.debug('Message is a device set state command')
                response_msg_list = yield from service.set_wemo_state(
                    log,
                    ref_num,
                    wemo_gw,
                    msg_header,
                    msg_payload,
                    message_types)

        # Que up response messages in outgoing msg que
        if len(response_msg_list) > 0:
            log.debug('Queueing response message(s)')
            for response_msg in response_msg_list:
                msg_out_que.put_nowait(response_msg)
                log.debug('Response message [%s] successfully queued',
                          response_msg)
        # Yield to other tasks for a while
        yield from asyncio.sleep(0.25)
