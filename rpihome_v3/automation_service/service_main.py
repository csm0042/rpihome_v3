#!/usr/bin/python3
""" service_main.py:
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
def service_main_task(msg_in_que, msg_out_que, rNumGen, devices, log,
                      address, port,
                      db_add, db_port,
                      wemo_add, wemo_port):
    """ task to handle the work the service is intended to do """
    # Initialize timestamp for periodic DB checks
    last_check = time.time()
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

            # Process messages from database service
            if msgHeader[3] == db_add:
                response_msg_list = process_db_messages(
                    rNumGen, devices, msgHeader, msgPayload, log,
                    address, port, db_add, db_port, wemo_add, wemo_port)

            # Process messages from wemo service
            if msgHeader[3] == wemo_add:
                response_msg_list = process_wemo_messages(
                    rNumGen, devices, msgHeader, msgPayload, log)
           
        # Que up response messages in outgoing msg que
        if len(response_msg_list) > 0:
            log.debug('Queueing response message(s)')
            for response_msg in response_msg_list:
                msg_out_que.put_nowait(response_msg)
                log.debug('Response message [%s] successfully queued',
                          response_msg)
        # Yield to other tasks for a while
        yield from asyncio.sleep(0.25)


# Process messages from database service **************************************
def process_db_messages(rNumGen, devices, msgHeader, msgPayload, log,
                        address, port, db_add, db_port, wemo_add, wemo_port):
    """ This function performs the custom operations required when a message
        is received from the db service """
    # Initialize result list
    response_msg_list = []        
    # message type 101 - log status update ACK
    if msgPayload[0] == '101':
        pass
    # Message type 103 - device command from DB
    elif msgPayload[0] == '103':
        # Find matching device in device list
        address = str()
        status = str()
        lastSeen = str()
        log.debug('Finding device in known device list with name: [%s]',
                  msgPayload[1])
        for d in devices:
            if d.name.lower() == msgPayload[2].lower():
                log.debug('Match found with address: [%s]', d.address)
                address = d.address
                status = d.status
                lastSeen =  d.last_seen
                break
        if len(address) > 0 and (
            msgPayload[3].lower() == 'on' or msgPayload[3].lower() == '1', or \
            msgPayload[3].lower() == 'off' or msgPayload[3].lower() == '0'):
            # Create message to wemo service to execute command
            log.debug('Building message header for msg to wemo service')
            response_header = rNumGen.new() + ',' + wemo_add + ',' + \
                            wemo_port + ',' + address + ',' + \
                            port
            log.debug('Building message payload for msg to wemo service')
            if msgPayload[3].lower() == "on" or msgPayload[3].lower() == '1':
                response_payload = '102,' + msgPayload[2] + ',' + address + ',' + \
                                   status + ',' + lastSeen
            if msgPayload[3].lower() == 'off' or msgPayload[3].lower() == '0'
                response_payload = '104,' + msgPayload[2] + ',' + address + ',' + \
                                   status + ',' + lastSeen
            log.debug('Building complete response message')                    
            response_msg = response_header + ',' + response_payload
            log.debug('Appending complete response message to result list: [%s]',
                      response_msg)
            response_msg_list.append(copy.copy(response_msg))
            # Create message to db service to mark command as executed
            log.debug('Building message header for msg to DB service')
            response_header = rNumGen.new() + ',' + db_add + ',' + \
                            db_port + ',' + address + ',' + \
                            port
            log.debug('Building message payload for msg to wemo service')
            response_payload = '104,' + msgPayload[1] + ',' + address + ',' + \
                               status + ',' + lastSeen
            log.debug('Building complete response message')                    
            response_msg = response_header + ',' + response_payload
            log.debug('Appending complete response message to result list: [%s]',
                    response_msg)
            response_msg_list.append(copy.copy(response_msg))            
        else:
            log.warning('Unrecoginized device name in command received from DB')
    # Message type 105 - device command from
    elif msgPayload[0] == '105':
        pass
    # Return response message
    return response_msg_list        


# Process messages from wemo service ******************************************
def process_wemo_messages(rNumGen, msgHeader, msgPayload, log):
    """ This function performs the custom operations required when a message
        is received from the wemo service """
    # Initialize result list
    response_msg_list = []        
    # Message type 101 - wemo status update
    if msgPayload[0] == '101':
        pass
    # Message type 103 - wemo set on ACK
    elif msgPayload[0] == '103':
        pass
    # Message type 105 - wemo set off ACK
    elif msgPayload[0] == '105':
        pass
    # Return response message
    return response_msg_list        
