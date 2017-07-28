#!/usr/bin/python3
""" service_main.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import copy
import logging
import sys
import time
import cal_service as service


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
def service_main_task(msg_in_que, msg_out_que, rNumGen, calendar, log,
                      address, port, auto_add, auto_port):
    """ task to handle the work the service is intended to do """
    # Initialize timestamp for periodic DB checks
    last_check = time.time()
    while True:
        # Initialize result list
        out_msg_list = []
        if msg_in_que.qsize() > 0:
            log.debug('Getting Incoming message from queue')
            next_msg = msg_in_que.get_nowait()
            log.debug('Splitting message into header / payload')
            next_msg_seg = next_msg.split(sep=',')

            # Split message into header and payload
            msgHeader = next_msg_seg[:5]
            msgPayload = next_msg_seg[5:]

            # Map header and payload to usable tags
            msgRef = msgHeader[0]
            msgDestAdd = msgHeader[1]
            msgDestPort = msgHeader[2]
            msgSourceAdd = msgHeader[3]
            msgSourcePort = msgHeader[4]

        # Que up response messages in outgoing msg que
        if len(out_msg_list) > 0:
            log.debug('Queueing response message(s)')
            for out_msg in out_msg_list:
                msg_out_que.put_nowait(out_msg)
                log.debug('Response message [%s] successfully queued',
                          out_msg)
        # Yield to other tasks for a while
        yield from asyncio.sleep(0.25)
