#!/usr/bin/python3
""" interface_to_cal.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
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


# Process messages type 300 ***************************************************
def process_cal_300(rNumGen, log, msgHeader, msgPayload):
    """ Msg type 300
    """
    # Initialize result list
    outMsgList = []
    outMsg = str()
    # Map header and payload to usable tags
    msgRef = msgHeader[0]
    msgDestAdd = msgHeader[1]
    msgDestPort = msgHeader[2]
    msgSourceAdd = msgHeader[3]
    msgSourcePort = msgHeader[4]
    # Map message payload to usable tags
    msgType = msgPayload[0]
    devName = msgPayload[1]
    devStart = msgPayload[2]

    outMsgList.append(copy.copy(outMsg))
    # Return response message    
    return outMsgList


# Process messages type 301 ***************************************************
def process_cal_301(rNumGen, devices, log, msgHeader, msgPayload):
    """ Msg type 301
    """
    # Initialize result list
    outMsgList = []
    outMsg = str()
    # Map header and payload to usable tags
    msgRef = msgHeader[0]
    msgDestAdd = msgHeader[1]
    msgDestPort = msgHeader[2]
    msgSourceAdd = msgHeader[3]
    msgSourcePort = msgHeader[4]
    # Map message payload to usable tags
    msgType = msgPayload[0]
    devName = msgPayload[1]
    devStart = msgPayload[2]

    outMsgList.append(copy.copy(outMsg))
    # Return response message    
    return outMsgList

