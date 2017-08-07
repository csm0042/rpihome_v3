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


# Process GET DEVICE STATUS message *******************************************
def process_wemo_gds(log, devices, msg, service_addresses):
    """ Get Device Status
        When a mis-directed GDS message is received, this function will:
        1) Update destination addr and port values in the GDS message to the
           appropraite values for the wemo service
        2) Update the device address, status, and last_seen values to the most
           current values known
        3) Queue the message to be sent to the wemo service
    """
    # Initialize result list
    out_msg_list = []

    # Map message into CCS message class
    message = helpers.GDSmessage()
    message.complete = msg

    # Search device table to find device name
    log.debug('Searching device table for [%s]', message.dev_name)
    dev_pointer = helpers.search_device_list(log, devices, message.dev_name)
    log.debug('Match found at device table index: %s', dev_pointer)

    # Modify CCS message to forward to wemo service
    if dev_pointer is not None:
        message.dest_addr = service_addresses['wemo_addr']
        message.dest_port = service_addresses['wemo_port']
        message.dev_addr = devices[dev_pointer].address
        message.dev_status = devices[dev_pointer].status,
        message.dev_last_seen = devices[dev_pointer].last_seen

        # Load message into output list
        log.debug('Loading completed msg: [%s]', message.complete)
        out_msg_list.append(message.complete)

    else:
        log.debug('Device not in device list: %s', message.dev_name)

    # Return response message
    return out_msg_list


# Process messages type 201 ***************************************************
def process_wemo_gds_ack(log, devices, msg):
    """ Get Device Status ACK
        When a GDS-ACK message is received, this function will:
        1) Search for the device in the active device table
        2) If found, update the status and last-seen values in the device
           table to the values encoded in the message.
    """
    # Initialize result list
    out_msg_list = []

    # Map message into CCS message class
    message = helpers.GDSACKmessage()
    message.complete = msg

    # Search device table to find device name
    log.debug('Searching device table for [%s]', message.dev_name)
    dev_pointer = helpers.search_device_list(log, devices, message.dev_name)
    log.debug('Match found at device table index: %s', dev_pointer)    

    # Update values based on message content
    if dev_pointer is not None:
        log.debug('Updating device [%s] status to [%s] and last seen to [%s]',
                  message.dev_name,
                  message.dev_status,
                  message.dev_last_seen)
        devices[dev_pointer].status = copy.copy(message.dev_status)
        devices[dev_pointer].last_seen = copy.copy(message.dev_last_seen)
    else:
        log.debug('Device [%s] not found in active device table. '
                  'No further action being taken', message.dev_name)

    # Return response message
    return out_msg_list


# Process messages type 202 ***************************************************
def process_wemo_sds(log, devices, msg, service_addresses):
    """ Set Device Status
        When a mis-directed SDS message is received, this function will:
        1) Update destination addr and port values in the SDS message to the
           appropraite values for the wemo service
        2) Update the device address, status, and last_seen values to the most
           current values known
        3) Queue the message to be sent to the wemo service
    """
    # Initialize result list
    out_msg_list = []

    # Map message into CCS message class
    message = helpers.SDSmessage()
    message.complete = msg

    # Search device table to find device name
    log.debug('Searching device table for [%s]', message.dev_name)
    dev_pointer = helpers.search_device_list(log, devices, message.dev_name)
    log.debug('Match found at device table index: %s', dev_pointer)

    # Update values based on message content
    if dev_pointer is not None:
        # Update message to forward to wemo service
        log.debug('Updating SDS message to forward to wemo service')
        message.dest_addr=service_addresses['wemo_addr']
        message.dest_port=service_addresses['wemo_port']
        message.dev_status=devices[dev_pointer].status
        message.dev_last_seen=devices[dev_pointer].last_seen
        
        # Load message into output list
        log.debug('Loading completed msg: [%s]', out_msg.complete)
        out_msg_list.append(out_msg.complete)
    else:
        log.debug('Device [%s] not found in active device table. '
                  'No further action being taken', message.dev_name)

    # Return response message
    return out_msg_list


# Process messages type 203 ***************************************************
def process_wemo_sds_ack(log, devices, msg):
    """ Set Device Status ACK
        When a SDS-ACK message is received, this function will:
        1) Search for the device in the active device table
        2) If found, update the status and last-seen values in the device
           table to the values encoded in the message.
    """
    # Initialize result list
    out_msg_list = []

    # Map message into CCS message class
    message = helpers.SDSACKmessage()
    message.complete = msg

    # Search device table to find device name
    log.debug('Searching device table for [%s]', message.dev_name)
    dev_pointer = helpers.search_device_list(log, devices, message.dev_name)
    log.debug('Match found at device table index: %s', dev_pointer)  

    # Update values based on message content
    if dev_pointer is not None:
        log.debug('Updating device [%s] status to [%s] and last seen to [%s]',
                  message.dev_name,
                  message.dev_status,
                  message.dev_last_seen)
        devices[dev_pointer].status = copy.copy(message.dev_status)
        devices[dev_pointer].last_seen = copy.copy(message.dev_last_seen)
    else:
        log.debug('Device [%s] not found in active device table. '
                  'No further action being taken', message.dev_name)

    # Return response message
    return out_msg_list
