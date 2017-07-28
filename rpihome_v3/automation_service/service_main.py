#!/usr/bin/python3
""" service_main.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import copy
import logging
import sys
import time
import automation_service as service


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
def service_main_task(msg_in_que, msg_out_que, rNumGen, log,
                      devices, calendar,
                      address, port,
                      cal_add, cal_port,
                      db_add, db_port,
                      wemo_add, wemo_port):
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

            # Process messages from database service
            if msgHeader[3] == db_add:
                if msgPayload[0] == '100':
                    log.debug('Message is a DB device status update '
                              '(type 100)')
                    out_msg_list = service.process_db_100(
                        rNumGen, log, msgHeader, msgPayload, db_add, db_port)
                elif msgPayload[0] == '101':
                    log.debug('Message is a DB device status update ACK '
                              '(type 101)')                    
                    out_msg_list = service.process_db_101(
                        log, msgHeader, msgPayload)
                elif msgPayload[0] == '102':
                    log.debug('Message is a read trigger for the DB command '
                              'table (type 102)')
                    out_msg_list = service.process_db_102(
                        rNumGen, log, msgHeader, msgPayload, db_add, db_port)
                elif msgPayload[0] == '103':
                    log.debug('Message is a device command received from the '
                              'DB device command table (type 103)')                    
                    out_msg_list = service.process_db_103(
                        rNumGen, devices, log, msgHeader, msgPayload,
                        address, port, wemo_add, wemo_port, db_add, db_port)
                elif msgPayload[0] == '104':
                    log.debug('Message is a DB command table record update '
                              '(type 104)')                    
                    out_msg_list = service.process_db_104(
                        rNumGen, log, msgHeader, msgPayload,
                        db_add, db_port)
                elif msgPayload[0] == '105':
                    log.debug('Message is a DB command table record update ACK '
                              '(type 105)')                    
                    out_msg_list = service.process_db_105(
                        log, msgHeader, msgPayload)

            # Process messages from wemo service
            if msgHeader[3] == wemo_add:
                if msgPayload[0] == '200':
                    log.debug('Message is a command to the wemo service to '
                              'get the current state of a wemo device '
                              '(type 200)')
                    out_msg_list = service.process_wemo_200(
                        rNumGen, log, msgHeader, msgPayload, wemo_add, wemo_port)
                elif msgPayload[0] == '201':
                    log.debug('Message is a response from the wemo service with'
                              'the current state of a wemo device (type 201)')
                    out_msg_list = service.process_wemo_201(
                        rNumGen, devices, log, msgHeader, msgPayload)
                elif msgPayload[0] == '202':
                    log.debug('Message is a command to the wemo service to'
                              'turn on a particular wemo device (type 202)')
                    out_msg_list = service.process_wemo_202(
                        rNumGen, log, msgHeader, msgPayload, wemo_add, wemo_port)
                elif msgPayload[0] == '203':
                    log.debug('Message is a response from the wemo service '
                              'indicating a wemo device was recently turned '
                              'on (type 203)')
                    out_msg_list = service.process_wemo_203(
                        rNumGen, devices, log, msgHeader, msgPayload)
                elif msgPayload[0] == '204':
                    log.debug('Message is a command to the wemo service to'
                              'turn off a particular wemo device (type 204)')
                    out_msg_list = service.process_wemo_204(
                        rNumGen, log, msgHeader, msgPayload, wemo_add, wemo_port)
                elif msgPayload[0] == '205':
                    log.debug('Message is a response from the wemo service '
                              'indicating a wemo device was recently turned '
                              'off (type 205)')
                    out_msg_list = service.process_wemo_205(
                        rNumGen, devices, log, msgHeader, msgPayload)

            # Process messages from calendar/schedule service
            if msgHeader[3] == cal_add:
                if msgPayload[0] == '300':
                    log.debug('Message is a command to the calendar service to '
                              'get the current schedule associated with a '
                              'device (type 300)')
                    out_msg_list = service.process_cal_300(
                        rNumGen, calendar, log, msgHeader, msgPayload)
                if msgPayload[0] == '301':
                    log.debug('Message is a schedule record item associated '
                              'with a device (type 301)')
                    out_msg_list = service.process_cal_301(
                        rNumGen, devices, log, msgHeader, msgPayload)

        # Que up response messages in outgoing msg que
        if len(out_msg_list) > 0:
            log.debug('Queueing response message(s)')
            for out_msg in out_msg_list:
                msg_out_que.put_nowait(out_msg)
                log.debug('Response message [%s] successfully queued',
                          out_msg)
        # Yield to other tasks for a while
        yield from asyncio.sleep(0.25)
