#!/usr/bin/python3
""" service_main.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import copy
import logging
import sys
import time



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
def service_main_task(msg_in_que, msg_out_que, rNumGen, devices, log,
                      address, port,
                      db_add, db_port,
                      wemo_add, wemo_port):
    """ task to handle the work the service is intended to do """
    # Initialize timestamp for periodic DB checks
    last_check = time.time()
    while True:
        # Initialize result list
        response_msg_list = []
        if msg_in_que.qsize() > 0:
            log.debug('Getting Incoming message from queue')
            next_msg = msg_in_que.get_nowait()
            log.debug('Splitting message into header / payload')
            next_msg_seg = next_msg.split(sep=',')
            msgHeader = next_msg_seg[:5]
            msgPayload = next_msg_seg[5:]
            
            # Do Stuff
            
        # Que up response messages in outgoing msg que
        if len(response_msg_list) > 0:
            log.debug('Queueing response message(s)')
            for response_msg in response_msg_list:
                msg_out_que.put_nowait(response_msg)
                log.debug('Response message [%s] successfully queued',
                          response_msg)
        # Yield to other tasks for a while
        yield from asyncio.sleep(0.25)
