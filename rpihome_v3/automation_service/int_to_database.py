#!/usr/bin/python3
""" interface_to_db.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import datetime
import env
from rpihome_v3.helpers.device import search_device_list
from rpihome_v3.messages.message_lsu import LSUmessage
from rpihome_v3.messages.message_lsu_ack import LSUACKmessage
from rpihome_v3.messages.message_rc import RCmessage
from rpihome_v3.messages.message_rc_ack import RCACKmessage
from rpihome_v3.messages.message_sds import SDSmessage
from rpihome_v3.messages.message_uc import UCmessage
from rpihome_v3.messages.message_uc_ack import UCACKmessage


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Process LOG STATUS UPDATE messages ******************************************
def process_db_lsu(log, msg, service_addresses):
    """ Process Database Log Status Update Message
        When a mis-directed LSU message is received, this function will:
        1) Re-directs LSU messages to database service
    """
    # Initialize result list
    out_msg_list = []

    # Map message into LSU message class
    message = LSUmessage(log=log)
    message.complete = msg

    # Update destination address and port to forward to db service
    log.debug('Revising LSU message to to forward to DB service')
    message.dest_addr = service_addresses['database_addr']
    message.dest_port = service_addresses['database_port']

    # Load revised message into output list
    log.debug('Loading completed msg: %s', message.complete)
    out_msg_list.append(message.complete)

    # Return response messages
    return out_msg_list


# Process LOG STATUS UPDATE ACK messages **************************************
def process_db_lsu_ack(log, msg):
    """ Process Database Log Status Update ACK Message
        When a LSU-ACK message is received, this function will:
        1) Processess the ACK from a LSU message re-direct
    """
    # Map message into LSU message class
    message = LSUACKmessage(log=log)
    message.complete = msg

    # Log receipt of ACK for debug purposes
    log.debug('LSU ACK Received: %s', msg.complete)


# Process RETURN COMMAND message **********************************************
def process_db_rc(log, msg, service_addresses):
    """ Process Database Return Command Message
        When a mis-directed RC message is received, this function will:
        1) Re-direct RC message to database service
    """
    # Initialize result list
    out_msg_list = []

    # Map message into LSU message class
    message = RCmessage(log=log)
    message.complete = msg

    # Update destination address and port to forward to db service
    log.debug('Revising RC message to to forward to DB service')
    message.dest_addr = service_addresses['database_addr']
    message.dest_port = service_addresses['database_port']    
    
    # Load message into output list
    log.debug('Loading completed msg: %s', message.complete)
    out_msg_list.append(message.complete)

    # Return response message
    return out_msg_list


# Process RETURN COMMAND ACK message ******************************************
def process_db_rc_ack(log, ref_num, devices, msg, service_addresses, message_types):
    """ Process Database Return Command ACK Message
        When a RC-ACK message is received, this function will:
        1) Generate and queue a UC message to mark the command as processed
        2) Generate and queue a SDS message to the appropriate device gateway
           to forward to the field device for action
    """
    # Initialize result list
    out_msg_list = []

    # Map message into LSU message class
    message = RCACKmessage(log=log)
    message.complete = msg

    # Search device table to find device name
    log.debug('Searching device table for [%s]', message.dev_name)
    dev_pointer = search_device_list(log, devices, message.dev_name)
    log.debug('Match found at device table index: %s', dev_pointer)

    # Send UC message to acknowledge received command and mark as processed
    log.debug('Generating UC message to mark device cmd as processed')
    out_msg = UCmessage(
        log=log,
        ref=ref_num.new(),
        dest_addr=service_addresses['database_addr'],
        dest_port=service_addresses['database_port'],
        source_addr=service_addresses['automation_addr'],
        source_port=service_addresses['automation_port'],
        msg_type=message_types['database_uc'],
        dev_id=message.dev_id,
        dev_processed=datetime.datetime.now())

    # Load message into output list
    log.debug('Loading completed msg: %s', out_msg.complete)
    out_msg_list.append(out_msg.complete)

    # Create message to wemo service to issue command to device
    if dev_pointer is not None:
        # Wemo switch commands get sent to the wemo service for handling
        if devices[dev_pointer].dev_type == 'wemo_switch':
            # Determine what command to issue
            out_msg = SDSmessage(
                log=log,
                ref=ref_num.new(),
                dest_addr=service_addresses['wemo_addr'],
                dest_port=service_addresses['wemo_port'],
                source_addr=service_addresses['automation_addr'],
                source_port=service_addresses['automation_port'],
                msg_type=message_types['wemo_sds'],
                dev_name=message.dev_name,
                dev_addr=devices[dev_pointer].dev_addr,
                dev_cmd=message.dev_cmd,
                dev_status=devices[dev_pointer].dev_status,
                dev_last_seen=devices[dev_pointer].dev_last_seen)
            # Load message into output list
            log.debug('Loading completed msg: %s', out_msg.complete)
            out_msg_list.append(out_msg.complete)
    else:
        log.debug('Device name not found in known device table')

    # Return response message
    return out_msg_list


# Process UPDATE COMMAND message **********************************************
def process_db_uc(log, msg, service_addresses):
    """ Process Database Update Command Message
        When a mis-directed UC message is received, this function will:
        1) Redirect that message to the database service
    """
    # Initialize result list
    out_msg_list = []

    # Map message into LSU message class
    message = UCmessage(log=log)
    message.complete = msg

    # Update destination address and port to forward to db service
    log.debug('Revising UC message to to forward to DB service')
    message.dest_addr = service_addresses['database_addr']
    message.dest_port = service_addresses['database_port']    
    
    # Load message into output list
    log.debug('Loading completed msg: %s', message.complete)
    out_msg_list.append(message.complete)

    # Return response message
    return out_msg_list



# Process UPDATE COMMAND ACK message ******************************************
def process_db_uc_ack(log, msg):
    """ Process Database Update Command ACK Message
        When a UC-ACK message is received, this function will:
        1) Processess the ACK from a UC message re-direct
    """
    # Map message into LSU message class
    message = UCACKmessage()
    message.complete = msg

    # Log receipt of ACK for debug purposes
    log.debug('UC ACK Received: %s', message.complete)
