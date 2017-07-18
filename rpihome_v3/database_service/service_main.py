#!/usr/bin/python3
""" db_service_workers.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import copy
import logging
import sys
import time
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
def service_main_task(msg_in_que, msg_out_que, rNumGen, database, log,
                      address, port, auto_address, auto_port):
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
            # Log Device status updates to database
            if msgPayload[0] == '100':
                log.debug('Message is a device status update')
                response_msg_list = yield from log_status_update(
                    rNumGen, database, log, msgHeader, msgPayload)
            # Device command not yet processed query
            if msgPayload[0] == '102':
                log.debug('Msg is a device pending cmd query')
                response_msg_list = yield from read_device_cmd(
                    rNumGen, database, log, msgHeader[1], msgHeader[2],
                    msgHeader[3], msgHeader[4])
            # Device command sent timestamp updates
            if msgPayload[0] == '104':
                log.debug('Msg is a device cmd update')
                response_msg_list = yield from update_device_cmd(
                    rNumGen, database, log, msgHeader, msgPayload)
        else:
            # Periodically check for pending commands
            if time.time() >= (last_check + 1):
                # Device command not yet processed query
                log.debug('Performing periodic check of pending commands')
                response_msg_list = yield from read_device_cmd(
                    rNumGen, database, log, address, port,
                    auto_address, auto_port)
                # Update timestamp
                last_check = time.time()
        # Que up response messages in outgoing msg que
        if len(response_msg_list) > 0:
            log.debug('Queueing response message(s)')
            for response_msg in response_msg_list:
                msg_out_que.put_nowait(response_msg)
                log.debug('Response message [%s] successfully queued',
                          response_msg)
        # Yield to other tasks for a while
        yield from asyncio.sleep(0.25)
        

# Internal Service Work Subtask - log status updates **************************
@asyncio.coroutine
def log_status_update(rNum, database, log, msgH, msgP):
    """ Function to insert status updates into device_log table """
    # Initialize result list
    response_msg_list = []
    # Map message header to usable tags
    msgRef = msgH[0]
    msgDestAdd = msgH[1]
    msgDestPort = msgH[2]
    msgSourceAdd = msgH[3]
    msgSourcePort = msgH[4]
    # Map message payload to usable tags
    msgType = msgP[0]
    devName = msgP[1]
    devAdd = msgP[2]
    devStatus = msgP[3]
    devLastSeen = msgP[4]
    # Execute Insert Query
    log.debug('Logging status change to database for [%s].  New '
              'status is [%s] with a last seen time of [%s]',
              devName, devStatus, devLastSeen)
    service.insert_record(
        database, devName, devStatus, devLastSeen, log)
    # Send response indicating query was executed
    log.debug('Building response message header')
    response_header = rNum.new() + ',' + msgSourceAdd + ',' + \
                      msgSourcePort + ',' + msgDestAdd + ',' + \
                      msgDestPort
    log.debug('Building response message payload')
    response_payload = '101,' + devName
    log.debug('Building complete response message')                    
    response_msg = response_header + ',' + response_payload
    log.debug('Appending complete response message to result list: [%s]',
              response_msg)
    response_msg_list.append(copy.copy(response_msg))
    # Return response message
    return response_msg_list


# Internal Service Work Subtask - wemo turn on ********************************
@asyncio.coroutine
def read_device_cmd(rNum, database, log, msgDestAdd, msgDestPort,
                    msgSourceAdd, msgSourcePort):
    """ Function to query database for any un-processed device commands """
    # Initialize result list
    response_msg_list = []
    # Execute select Query
    log.debug('Querying database for pending device commands')
    pending_cmd_list = service.query_command(database, log)
    # Send response message for each record returned by query
    if len(pending_cmd_list) <= 0:
        log.debug('No pending commands found')
    else:
        log.debug('Preparing response messages for pending commands')
        for pending_cmd in pending_cmd_list:
            log.debug('Building response message header')
            response_header = rNum.new() + ',' + msgSourceAdd + ',' + \
                              msgSourcePort + ',' + msgDestAdd + ',' + \
                              msgDestPort
            log.debug('Building response message payload')
            response_payload = '103,' + pending_cmd
            log.debug('Building complete response message')
            response_msg = response_header + ',' + response_payload
            log.debug('Appending complete response message to result list: [%s]',
                      response_msg)
            response_msg_list.append(copy.copy(response_msg))
    # Return list of response messages from query
    return response_msg_list


# Internal Service Work Subtask - wemo turn off *******************************
@asyncio.coroutine
def update_device_cmd(rNum, database, log, msgH, msgP):
    """ Function to set state of wemo device to "off" """
    # Initialize result list
    response_msg_list = []
    # Map message header to usable tags
    msgRef = msgH[0]
    msgDestAdd = msgH[1]
    msgDestPort = msgH[2]
    msgSourceAdd = msgH[3]
    msgSourcePort = msgH[4]
    # Map message payload to usable tags
    msgType = msgP[0]
    cmdId = msgP[1]
    cmdProcessed = msgP[2]
    # Execute update Query
    log.debug('Querying database to mark command with ID [%s] as complete '
              'with timestamp [%s]', cmdId, cmdProcessed)
    service.update_command(database, cmdId, cmdProcessed, log)
    # Send response indicating query was executed
    log.debug('Building response message header')
    response_header = rNum.new() + ',' + msgSourceAdd + ',' + \
                      msgSourcePort + ',' + msgDestAdd + ',' + \
                      msgDestPort
    log.debug('Building response message payload')
    response_payload = '105,' + cmdId
    log.debug('Building complete response message')                    
    response_msg = response_header + ',' + response_payload
    log.debug('Appending complete response message to result list: [%s]',
              response_msg)
    response_msg_list.append(copy.copy(response_msg))
    # Return response message
    return response_msg_list
