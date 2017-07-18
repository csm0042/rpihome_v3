#!/usr/bin/python3
""" wemo_service_workers.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import copy
import logging
import sys
import time
if __name__ == "__main__":
    sys.path.append("..")
import wemo_service
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