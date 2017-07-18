#!/usr/bin/python3
""" wemo_service_workers.py:
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
def service_main_task(msg_in_que, msg_out_que, rNumGen, wemoGw, log):
    """ task to handle the work the service is intended to do """
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
            # Wemo Device Status Queries
            if msgPayload[0] == '100':
                log.debug('Message is a device status update request')                
                response_msg_list = yield from get_wemo_status(
                    rNumGen, wemoGw, log, msgHeader, msgPayload)
            # Wemo Device on commands
            if msgPayload[0] == '102':
                log.debug('Message is a device set "on" command')
                response_msg_list = yield from set_wemo_on(
                    rNumGen, wemoGw, log, msgHeader, msgPayload)
            # Wemo Device off commands
            if msgPayload[0] == '104':
                log.debug('Message is a device set "off" command')
                response_msg_list = yield from set_wemo_off(
                    rNumGen, wemoGw, log, msgHeader, msgPayload)
        # Que up response messages in outgoing msg que                    
        if len(response_msg_list) > 0:
            log.debug('Queueing response message(s)')
            for response_msg in response_msg_list:
                msg_out_que.put_nowait(response_msg)
                log.debug('Response message [%s] successfully queued',
                          response_msg)                                      
        # Yield to other tasks for a while
        yield from asyncio.sleep(0.25)


# Internal Service Work Subtask - wemo get status *****************************
@asyncio.coroutine
def get_wemo_status(rNum, wemo_gw, log, msgH, msgP):
    """ Function to properly process wemo device status requests """
    # Initialize result list
    response_msg_list = []
    # Map message header to usable tags    
    msgRef = msgH[0]
    msgDestAdd = msgH[1]
    msgDestPort = msgH[2]
    msgSourceAdd = msgH[3]
    msgSourcePort = msgH[4]
    # Map message payload to usable tags    
    devName = msgP[1]
    devAdd = msgP[2]
    devStatus = msgP[3]
    devLastSeen = msgP[4]
    # Execute Status Update
    log.debug('Requesting status for [%s] at [%s] with original status '
              '[%s] and update time [%s]', devName, devAdd, devStatus,
              devLastSeen)
    devStatusNew, devLastSeenNew = wemo_gw.read_status(
        devName, devAdd, devStatus, devLastSeen)
    # Send response indicating query was executed        
    log.debug('Building response message header')
    response_header = rNum.new() + ',' + msgSourceAdd + ',' + \
                      msgSourcePort + ',' + msgDestAdd + ',' + \
                      msgDestPort
    log.debug('Building response message payload')
    response_payload = '101,' + devName + ',' + str(devStatusNew) + ',' + \
                       str(devLastSeenNew)[:19]
    log.debug('Building complete response message')                    
    response_msg = response_header + ',' + response_payload
    log.debug('Appending complete response message to result list: [%s]',
              response_msg)
    response_msg_list.append(copy.copy(response_msg))
    # Return response message
    return response_msg_list


# Internal Service Work Subtask - wemo turn on ********************************
@asyncio.coroutine
def set_wemo_on(rNum, wemo_gw, log, msgH, msgP):
    """ Function to set state of wemo device to "on" """
    # Initialize result list
    response_msg_list = []
    # Map message header to usable tags      
    msgRef = msgH[0]
    msgDestAdd = msgH[1]
    msgDestPort = msgH[2]
    msgSourceAdd = msgH[3]
    msgSourcePort = msgH[4]
    # Map message payload to usable tags    
    devName = msgP[1]
    devAdd = msgP[2]
    devStatus = msgP[3]
    devLastSeen = msgP[4]
    # Execute Wemo On Command    
    log.debug('Commanding state to "on" for [%s] at [%s] with original '
              'status [%s] and update time [%s]', 
              devName, devAdd, devStatus, devLastSeen)
    devStatusNew, devLastSeenNew = wemo_gw.turn_on(devName, devAdd,
                                                   devStatus, devLastSeen)
    # Send response indicating command was executed                                                   
    log.debug('Building response message header')
    response_header = rNum.new() + ',' + msgSourceAdd + ',' + \
                      msgSourcePort + ',' + msgDestAdd + ',' + \
                      msgDestPort
    log.debug('Building response message payload')
    response_payload = '103,' + devName + ',' + \
                       str(devStatusNew) + ',' + str(devLastSeenNew)
    log.debug('Building complete response message')                    
    response_msg = response_header + ',' + response_payload
    log.debug('Appending complete response message to result list: [%s]',
              response_msg)
    response_msg_list.append(copy.copy(response_msg))
    # Return response message
    return response_msg_list


# Internal Service Work Subtask - wemo turn off *******************************
@asyncio.coroutine
def set_wemo_off(rNum, wemo_gw, log, msgH, msgP):
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
    devName = msgP[1]
    devAdd = msgP[2]
    devStatus = msgP[3]
    devLastSeen = msgP[4]
    # Execute Wemo Off Command      
    log.debug('Commanding state to "off" for [%s] at [%s] with original status '
              '[%s] and update time [%s]', devName, devAdd, devStatus,
              devLastSeen)
    devStatusNew, devLastSeenNew = wemo_gw.turn_off(devName, devAdd,
                                                    devStatus, devLastSeen)
    # Send response indicating command was executed  
    log.debug('Building response message header')
    response_header = rNum.new() + ',' + msgSourceAdd + ',' + \
                      msgSourcePort + ',' + msgDestAdd + ',' + \
                      msgDestPort
    log.debug('Building response message payload')
    response_payload = '105,' + devName + ',' + \
                       str(devStatusNew) + ',' + str(devLastSeenNew)
    log.debug('Building complete response message')                    
    response_msg = response_header + ',' + response_payload
    log.debug('Appending complete response message to result list: [%s]',
              response_msg)
    response_msg_list.append(copy.copy(response_msg))
    # Return response message
    return response_msg_list