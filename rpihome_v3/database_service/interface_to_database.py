#!/usr/bin/python3
""" interface_to_db.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import copy
import datetime
import helpers


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


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
