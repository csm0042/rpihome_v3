#!/usr/bin/python3
""" interface_to_wemo.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import copy
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


# Process messages type 100 ***************************************************
def process_wemo_200(rNumGen, log, msgHeader, msgPayload, db_add, db_port):
    """ 
    This function performs the custom operations required when a message
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