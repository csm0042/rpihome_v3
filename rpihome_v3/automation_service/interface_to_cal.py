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
def create_cal_300(rNumGen, devices, log, auto_add, auto_port,
                   cal_add, cal_port):
    """ Msg type 300
    """
    # Initialize result list
    outMsgList = []
    outMsg = str()
    # Create 300 messages for every device in list with "schedule" as their rule
    for d in devices:
        if d.rule == 'schedule' or 'dusk_to_dawn' or '':
            outMsg = '%s,%s,%s,%s,%s,%s,%s' % (
                rNumGen.new(), cal_add, cal_port, auto_add, auto_port,
                '300', d.name)
            outMsgList.append(copy.copy(outMsg))
    # Return response message    
    return outMsgList


# Process messages type 301 ***************************************************
def process_cal_301(rNumGen, devices, log, msgHeader, msgPayload,
                    auto_add, auto_port, wemo_add, wemo_port):
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
    devState = msgPayload[2]

    # Search device list for a device name matching the one in the message
    found = False
    ptr = 0
    for i, d in enumerate(devices):
        if d.name == devName:
            found = True
            ptr = i
            break

    # If a match was found, continue
    if found is True:
        log.debug('Device [%s] was found in device table', devName)
        if devices[ptr].cmd != devState:
            log.debug('New state [%s] commanded for device [%s]',
                      devState, devName)
            devices[ptr].cmd = devState
            if devices[ptr].devtype == 'wemo_switch' and devState == 'on':
                log.debug('Sending "on" command to wemo service for [%s]',
                          devName)
                outMsg = '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (
                    rNumGen.new(), wemo_add, wemo_port, auto_add, auto_port,
                    '202', devName, devices[ptr].address, devices[ptr].status,
                    devices[ptr].last_seen)
                outMsgList.append(copy.copy(outMsg))
            if devices[ptr].devtype == 'wemo_switch' and devState == 'off':
                log.debug('Sending "off" command to wemo service for [%s]',
                          devName)
                outMsg = '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (
                    rNumGen.new(), wemo_add, wemo_port, auto_add, auto_port,
                    '204', devName, devices[ptr].address, devices[ptr].status,
                    devices[ptr].last_seen)
                outMsgList.append(copy.copy(outMsg))

    # Return response message
    return outMsgList
