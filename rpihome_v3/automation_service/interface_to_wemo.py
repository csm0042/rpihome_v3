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


# Process messages type 200 ***************************************************
def process_wemo_200(rNumGen, log, msgHeader, msgPayload, wemo_add, wemo_port):
    """ Msg type 200
        Get wemo device status

        This function takes any type 200 messages and forwards them on to the
        wemo service.  The forwarded message is updated to contain the source
        info for the original service that initially sent the message so the
        response gets back to where the reqeust originated.
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
    devAdd = msgPayload[2]
    devStatus = msgPayload[3]
    devLastSeen = msgPayload[4]
    # Build new message to forward to wemo service
    log.debug('Generating revised msg 200 to forward to wemo service')
    outMsg = '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (
        rNumGen.new(), wemo_add, wemo_port, msgSourceAdd, msgSourcePort,
        msgType, devName, devAdd, devStatus, devLastSeen)
    log.debug('Loading completed msg 200 into outgoing msg buffer: '
              '%s', outMsg)
    outMsgList.append(copy.copy(outMsg))
    # Return response message
    return outMsgList


# Process messages type 201 ***************************************************
def process_wemo_201(rNumGen, devices, log, msgHeader, msgPayload):
    """ Msg type 201
        Get wemo device status ACK

        This function takes a type 201 messages uses it to update the status
        of a device as currently defined in the device list.
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
    devStatus = msgPayload[2]
    devLastSeen = msgPayload[3]
    # Search active device list for a device naming matching the name
    # in the message
    log.debug('Search active device table for matching device name: '
              '[%s]', devName)
    devIndex = helpers.search_device_list(devName, devices, log)
    # If found, update the status and last-seen attribute associated with
    # the device.  If not found, discard the message and do nothing
    if devIndex is not None:
        log.debug('Updating device [%s] status to [%s] and last seen to [%s]',
                  devStatus, devLastSeen)
        devices[devIndex].status = copy.copy(devStatus)
        devices[devIndex].last_seen = copy.copy(devLastSeen)
    else:
        log.debug('Device [%s] not found in active device table.  No further '
                  'action being taken', devName)
    # Return response message
    return outMsgList


# Process messages type 202 ***************************************************
def process_wemo_202(rNumGen, log, msgHeader, msgPayload, wemo_add, wemo_port):
    """ Msg type 202
        Set wemo device to "on"

        This function takes any type 202 messages and forwards them on to the
        wemo service.  The forwarded message is updated to contain the source
        info for the original service that initially sent the message so the
        response gets back to where the reqeust originated.
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
    devAdd = msgPayload[2]
    devStatus = msgPayload[3]
    devLastSeen = msgPayload[4]
    # Build new message to forward to wemo service
    log.debug('Generating revised msg 202 to forward to wemo service')
    outMsg = '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (
        rNumGen.new(), wemo_add, wemo_port, msgSourceAdd, msgSourcePort,
        msgType, devName, devAdd, devStatus, devLastSeen)
    log.debug('Loading completed msg 202 into outgoing msg buffer: '
              '%s', outMsg)
    outMsgList.append(copy.copy(outMsg))
    # Return response message
    return outMsgList


# Process messages type 203 ***************************************************
def process_wemo_203(rNumGen, devices, log, msgHeader, msgPayload):
    """ Msg type 203
        Set wemo device to "on" ACK

        This function takes a type 203 messages uses it to update the status
        of a device as currently defined in the device list.
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
    devStatus = msgPayload[2]
    devLastSeen = msgPayload[3]
    # Search active device list for a device naming matching the name
    # in the message
    log.debug('Search active device table for matching device name: '
              '[%s]', devName)
    devIndex = helpers.search_device_list(devName, devices, log)
    # If found, update the status and last-seen attribute associated with
    # the device.  If not found, discard the message and do nothing
    if devIndex is not None:
        log.debug('Updating device [%s] status to [%s] and last seen to [%s]',
                  devName, devStatus, devLastSeen)
        devices[devIndex].status = copy.copy(devStatus)
        devices[devIndex].last_seen = copy.copy(devLastSeen)
    else:
        log.debug('Device [%s] not found in active device table.  No further '
                  'action being taken', devName)
    # Return response message
    return outMsgList


# Process messages type 204 ***************************************************
def process_wemo_204(rNumGen, log, msgHeader, msgPayload, wemo_add, wemo_port):
    """ Msg type 204
        Set wemo device to "off"

        This function takes any type 204 messages and forwards them on to the
        wemo service.  The forwarded message is updated to contain the source
        info for the original service that initially sent the message so the
        response gets back to where the reqeust originated.
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
    devAdd = msgPayload[2]
    devStatus = msgPayload[3]
    devLastSeen = msgPayload[4]
    # Build new message to forward to wemo service
    log.debug('Generating revised msg 204 to forward to wemo service')
    outMsg = '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (
        rNumGen.new(), wemo_add, wemo_port, msgSourceAdd, msgSourcePort,
        msgType, devName, devAdd, devStatus, devLastSeen)
    log.debug('Loading completed msg 204 into outgoing msg buffer: '
              '%s', outMsg)
    outMsgList.append(copy.copy(outMsg))
    # Return response message
    return outMsgList


# Process messages type 205 ***************************************************
def process_wemo_205(rNumGen, devices, log, msgHeader, msgPayload):
    """ Msg type 205
        Set wemo device to "off" ACK

        This function takes a type 205 messages uses it to update the status
        of a device as currently defined in the device list.
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
    devStatus = msgPayload[2]
    devLastSeen = msgPayload[3]
    # Search active device list for a device naming matching the name
    # in the message
    log.debug('Search active device table for matching device name: '
              '[%s]', devName)
    devIndex = helpers.search_device_list(devName, devices, log)
    # If found, update the status and last-seen attribute associated with
    # the device.  If not found, discard the message and do nothing
    if devIndex is not None:
        log.debug('Updating device [%s] status to [%s] and last seen to [%s]', 
                  devName, devStatus, devLastSeen)
        devices[devIndex].status = copy.copy(devStatus)
        devices[devIndex].last_seen = copy.copy(devLastSeen)
    else:
        log.debug('Device [%s] not found in active device table.  No further '
                  'action being taken', devName)
    # Return response message
    return outMsgList
