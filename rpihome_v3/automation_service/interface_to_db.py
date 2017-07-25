#!/usr/bin/python3
""" interface_to_db.py:
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


# Process messages type 100 ***************************************************
def process_db_100(rNumGen, log, msgHeader, msgPayload, db_add, db_port):
    """ Msg type 100
        Insert record into database status table

        This function triggers an insert query in the device status table to
        log updated device status(es) whenever state changes are detected.
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
    """ Msg type 101
        Insert record into database status table ACK

        This function processes the positive ACK that is retunred when a 101
        message is successfully processed
    """
    # Initialize result list
    outMsgList = []
    # Log receipt of ACK for debug purposes
    log.debug('Log status update message successfully acknowledged '
              'by db service [%s,%s]', msgHeader, msgPayload)
    # Return response message    
    return outMsgList


# Process messages type 102 ***************************************************
def process_db_102(rNumGen, log, msgHeader, msgPayload, db_add, db_port):
    """ Msg type 102
        Select pending commands from database command table

        This function triggers a select query for the pending command table in
        the database.  Commands that are not processed and less than 5 minutes
        old will be returned in the ACK for this message.
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


# Process messages type 103 ***************************************************
def process_db_103(rNumGen, devices, log, msgHeader, msgPayload,
                   address, port, wemo_add, wemo_port, db_add, db_port):
    """ Msg type 103
        Select pending commands from database command table ACK

        This function takes the results of the select query from the pending
        command table and sends out messages as necessary to other processes
        so those commands get executed
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
    cmdId = msgPayload[1]
    devName = msgPayload[2]
    devCmd = msgPayload[3]
    cmdTimestamp = msgPayload[4]
    cmdProcessed = msgPayload[5]
    # Search device table to find device name
    log.debug('Searching device table for [%s]', devName)
    devPointer = helpers.search_device_list(devName, devices, log)
    log.debug('Match found at device table index: %s', devPointer)
    if devPointer is not None:
        # Wemo switch commands get sent to the wemo service for handling
        if devices[devPointer].devtype == 'wemo_switch':
            # Generate and queue command to wemo gateway service
            if devCmd == 'on' or devCmd == '1':
                log.debug('Generating msg 202 to turn wemo device "on"')
                cmdType = '202'
            elif devCmd == 'off' or devCmd == '0':
                log.debug('Generating msg 202 to turn wemo device "on"')
                cmdType = '204'
            else:
                log.debug('Invalid command in pending cmd table')
                cmdType = 'None'
            # Build actual command
            outMsg = '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (
                rNumGen.new(), wemo_add, wemo_port, address, port,
                cmdType, devName, devices[devPointer].address,
                devices[devPointer].status, devices[devPointer].last_seen)
            log.debug('Loading completed msg 202/204 into outgoing msg buffer '
                      '[%s]', outMsg)
            outMsgList.append(copy.copy(outMsg))
    else:
        log.debug('Device name not found in known device table')
    # Regardless what was done with device command, perform database update
    # to mark it as processed to avoid executing it again
    log.debug('Generating msg 104 to mark device cmd as processed')
    outMsg = '%s,%s,%s,%s,%s,%s,%s,%s' % (
        rNumGen.new(), db_add, db_port, address, port,
        '104', cmdId, str(datetime.datetime.now())[:19])
    log.debug('Loading completed msg 104 into outgoing msg buffer '
              '[%s]', outMsg)            
    outMsgList.append(copy.copy(outMsg))        
    # Return response message
    return outMsgList


# Process messages type 104 ***************************************************
def process_db_104(rNumGen, log, msgHeader, msgPayload, db_add, db_port):
    """ Msg type 104
        Update processed flag for record in database command table

        This function triggers and update query to add a timestamp to the
        "processed" column for records in the pending command table.  This
        prevents commands from being executed more than once.
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
    cmdId = msgPayload[1]
    cmdProcessed = msgPayload[2]
    # Build new message to forward to db service
    log.debug('Generating msg 104 to mark device cmd as processed')
    outMsg = '%s,%s,%s,%s,%s,%s,%s,%s' % (
        rNumGen.new(), db_add, db_port, msgSourceAdd, msgSourcePort,
        msgType, cmdId, cmdProcessed)
    log.debug('Loading completed msg 104 into outgoing msg buffer '
              '[%s]', outMsg)
    outMsgList.append(copy.copy(outMsg))
    # Return response message    
    return outMsgList   


# Process messages type 105 ***************************************************
def process_db_105(log, msgHeader, msgPayload):
    """ Msg type 105
        Update processed flag for record in database command table ACK

        This function processes the positive ACK that is retunred when a 104
        message is successfully processed        
    """
    # Initialize result list
    outMsgList = []
    # Log that ACK was received
    log.debug('Log status update message successfully acknowledged '
              'by db service [%s,%s]', msgHeader, msgPayload)
    # Return response message
    return outMsgList
