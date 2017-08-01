#!/usr/bin/python3
""" interface_to_cal.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import copy
import datetime


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
def process_cal_300(rNumGen, calendar, log, msgHeader, msgPayload):
    """ Msg type 300
    """
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

    # Check schedule for device
    log.debug('Checking schedule to determine desired state of device [%s]',
              devName)
    desiredCmd = calendar.check_schedule(name=devName)
    
    # Create ACK message (type 301) with desired device state per schedule
    if desiredCmd is True:
        log.debug('Device [%s] should be "on" according to schedule', devName)
        outMsg = '%s,%s,%s,%s,%s,%s,%s,%s' % (
            rNumGen.new(), msgSourceAdd, msgSourcePort, msgDestAdd, msgDestPort,
            '301', devName, 'on')
    else:
        log.debug('Device [%s] should be "off" according to schedule', devName)
        outMsg = '%s,%s,%s,%s,%s,%s,%s,%s' % (
            rNumGen.new(), msgSourceAdd, msgSourcePort, msgDestAdd, msgDestPort,
            '301', devName, 'off')
    
    # Append response message (type 301) to outgoing msg queue
    log.debug('Returning message: [%s]', outMsg)
    outMsgList.append(copy.copy(outMsg))
    # Return response message
    return outMsgList
