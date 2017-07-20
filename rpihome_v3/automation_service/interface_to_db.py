#!/usr/bin/python3
""" interface_to_db.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import copy


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Process messages type 100 ***************************************************
def process_db_100(rNumGen, log, msgHeader, msgPayload, db_add, db_port):
    """ This function performs the custom operations required when a message
        type 100 is received.  These messages are forwarded to the database
        service for processing """
    # Initialize result list
    outMsgList = []
    # Map header and payload to usable tags
    msgRef = msgHeader[0]
    msgDestAdd = msgHeader[1]
    msgDestPort = msgHeader[2]
    msgSourceAdd = msgHeader[3]
    msgSourcePort = msgHeader[4]
    # Map message payload to usable tags
    msgType = msgPayload[0]
    devName = msgPayload[1]
    devAdd = msgPayload[2]
    devStatus = msgPayload[3]
    devLastSeen = msgPayload[4]
    # Build new message to forward to db service
    log.debug('Building revised message header for msg to to forward '
              'to DB service')
    outMsgHeader = '%s,%s,%s,%s,%s' % (
        rNumGen.new(), db_add, db_port, msgSourceAdd, msgSourcePort)
    log.debug('Building revised message payload for msg to forward '
              'to db service')
    outMsgPayload = '%s,%s,%s,%s,%s' % (
        msgType, devName, devAdd, devStatus, devLastSeen)
    log.debug('Building complete revised message to forward'
              'to db service')                    
    outMsg = '%s,%s' % (outMsgHeader, outMsgPayload)
    log.debug('Appending complete response message to result '
              'list: [%s]', outMsg)
    outMsgList.append(copy.copy(outMsg))
    # Return response message    
    return outMsgList


# Process messages type 101 ***************************************************
def process_db_101(log, msgHeader, msgPayload):
    """ This function performs the custom operations required when a message
        type 101 is received. """
    # Initialize result list
    outMsgList = []
    # Map header and payload to usable tags
    msgRef = msgHeader[0]
    msgDestAdd = msgHeader[1]
    msgDestPort = msgHeader[2]
    msgSourceAdd = msgHeader[3]
    msgSourcePort = msgHeader[4]
    # Map message payload to usable tags
    msgType = msgPayload[0]
    devName = msgPayload[1]
    # Build new message to forward to db service
    log.debug('Log status update [%s,%s] message successfully acknowledged '
              'by db service', msgHeader, msgPayload)
    # Return response message    
    return outMsgList


# Process messages type 100 ***************************************************
def process_db_102(rNumGen, log, msgHeader, msgPayload, db_add, db_port):
    """ This function performs the custom operations required when a message
        type 102 is received.  These messages are forwarded to the database
        service for processing """
    # Initialize result list
    outMsgList = []
    # Map header and payload to usable tags
    msgRef = msgHeader[0]
    msgDestAdd = msgHeader[1]
    msgDestPort = msgHeader[2]
    msgSourceAdd = msgHeader[3]
    msgSourcePort = msgHeader[4]
    # Map message payload to usable tags
    msgType = msgPayload[0]
    # Build new message to forward to db service
    log.debug('Building revised message header for msg to to forward '
              'to DB service')
    outMsgHeader = '%s,%s,%s,%s,%s' % (
        rNumGen.new(), db_add, db_port, msgSourceAdd, msgSourcePort)
    log.debug('Building revised message payload for msg to forward '
              'to db service')
    outMsgPayload = msgType
    log.debug('Building complete revised message to forward'
              'to db service')                    
    outMsg = '%s,%s' % (outMsgHeader, outMsgPayload)
    log.debug('Appending complete response message to result '
              'list: [%s]', outMsg)
    outMsgList.append(copy.copy(outMsg))
    # Return response message    
    return outMsgList


# Process messages type 101 ***************************************************
def process_db_103(rNumGen, devices, log, msgHeader, msgPayload,
                   address, port, wemo_add, wemo_port):
    """ This function performs the custom operations required when a message
        type 101 is received. """
    # Initialize result list
    outMsgList = []
    # Map header and payload to usable tags
    msgRef = msgHeader[0]
    msgDestAdd = msgHeader[1]
    msgDestPort = msgHeader[2]
    msgSourceAdd = msgHeader[3]
    msgSourcePort = msgHeader[4]
    # Map message payload to usable tags
    msgType = msgPayload[0]
    cmdId = msgPayload[1]
    devName = msgPayload[2]
    devCmd = msgPayload[3]
    cmdTimestamp = msgPayload[4]
    cmdProcessed = msgPayload[5]
    # Search device table to find device name
    devPointer = search_device_list(devName, devices)
    if devPointer is not None:
        # Wemo switch commands get sent to the wemo service for handling
        if devices[devPointer] == 'wemo_switch':
            log.debug('Building msg header for msg to wemo service')
            outMsgHeader = '%s,%s,%s,%s,%s' % (
                rNumGen.new(), wemo_add, wemo_port, address, port)
            log.debug('Choosing msg type based on command')
            if devCmd == 'on' or devCmd == '1':
                cmdType = '102'
            elif devCmd == 'off' or devCmd == '0':
                cmdType = '104'
            else:
                cmdType = 'None'
            log.debug('Building msg payload for msg to wemo service')
            outMsgPayload = '%s,%s,%s,%s,%s' % (
                cmdType, devName, devices[devPointer].address,
                devices[devPointer].status, devices[devPointer].last_seen)
            log.debug('Assembling parts to form complete message')
            outMsg = '%s,%s' % (outMsgHeader, outMsgPayload)
            outMsgList.append(copy.copy(outMsg))
    # Return response message
    return outMsgList            


def search_device_list(name, devices):
    for i, d in enumerate(devices):
        if name == devices.name:
            return i
    return None
