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
    resultList = []
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

    # Query update from google calendar for that device
    log.debug('Requesting schedule from calendar object for device: [%s]',
              devName)
    resultList = calendar.sched_by_name(name=devName)

    # Build new message to forward to db service
    for result in resultList:
        log.debug('Building revised message for schedule item to return '
                  'to requesting service')
        outMsg = '%s,%s,%s,%s,%s,%s,%s,%s,%s,' % (
            rNumGen.new(), msgSourceAdd, msgSourcePort, msgDestAdd, msgDestPort,
            '301', devName, str(result.start)[:19], str(result.end)[:19])
        log.debug('Appending complete response message to outgoing msg queue: '
                  '[%s]', outMsg)
        outMsgList.append(copy.copy(outMsg))
    # Return response message
    return outMsgList
