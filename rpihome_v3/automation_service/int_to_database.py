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


# Process LOG STATUS UPDATE messages ******************************************
def process_db_lsu(log, ref_num, msg_header, msg_payload,
                   service_addresses, message_types):
    """ Process Database Log Status Update Message
        This function triggers an insert query in the device status table to
        log updated device status(es) whenever state changes are detected.
    """
    # Initialize result list
    out_msg_list = []

    # Map header and payload to usable tags
    msg_source_add = msg_header[3]
    msg_source_port = msg_header[4]
    dev_name = msg_payload[1]
    dev_addr = msg_payload[2]
    dev_status = msg_payload[3]
    dev_last_seen = msg_payload[4]

    # Build new message to forward to db service
    log.debug('Building LSU message to to forward to DB service')
    out_msg = '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (
        ref_num.new(),
        service_addresses['database_addr'],
        service_addresses['database_port'],
        msg_source_add,
        msg_source_port,
        message_types['database_lsu'],
        dev_name,
        dev_addr,
        dev_status,
        dev_last_seen)
    # Load message into output list
    log.debug('Loading completed msg: [%s]', out_msg)
    out_msg_list.append(copy.copy(out_msg))

    # Return response messages
    return out_msg_list


# Process LOG STATUS UPDATE ACK messages **************************************
def process_db_lsu_ack(log, msg_header, msg_payload):
    """ Process Database Log Status Update ACK Message
        This function processes the positive ACK that is returned when a LSU
        message is successfully processed
    """ 
    # Log receipt of ACK for debug purposes
    log.debug('LSU ACK Received: [%s,%s]', msg_header, msg_payload)


# Process RETURN COMMAND message **********************************************
def process_db_rc(log, ref_num, msg_header, msg_payload,
                  service_addresses, message_types):
    """ Process Database Return Command Message
        This function triggers a select query for the pending command table in
        the database.  Commands that are not processed and less than 5 minutes
        old will be returned in the ACK for this message.
    """
    # Initialize result list
    out_msg_list = []
    
    # Map header and payload to usable tags
    msg_ref = msg_header[0]
    msg_dest_addr = msg_header[1]
    msg_dest_port = msg_header[2]
    msg_source_addr = msg_header[3]
    msg_source_port = msg_header[4]
    msg_type = msg_payload[0]
    dev_name = msg_payload[1]
    
    # Build new message to forward to db service
    log.debug('Building RC message to to forward to DB service')
    out_msg = '%s,%s,%s,%s,%s,%s,%s' % (
        ref_num.new(),
        service_addresses['database_addr'],
        service_addresses['database_port'],
        msg_source_addr,
        msg_source_port,
        message_types['database_rc'],
        dev_name)
    # Load message into output list
    log.debug('Loading completed msg: [%s]', out_msg)
    out_msg_list.append(copy.copy(out_msg))

    # Return response message
    return out_msg_list


# Process RETURN COMMAND ACK message ******************************************
def process_db_rc_ack(log, ref_num, devices, msg_payload,
                      service_addresses, message_types):
    """ Process Database Return Command ACK Message
        This function takes the results of the select query from the pending
        command table and sends out messages as necessary to other processes
        so those commands get executed
    """
    # Initialize result list
    out_msg_list = []

    # Map message payload to usable tags
    msg_type = msg_payload[0]
    cmd_id = msg_payload[1]
    dev_name = msg_payload[2]
    dev_cmd = msg_payload[3]

    # Search device table to find device name
    log.debug('Searching device table for [%s]', dev_name)
    dev_pointer = helpers.search_device_list(log, devices, dev_name)
    log.debug('Match found at device table index: %s', dev_pointer)

    # Create message to wemo service to issue command to device
    if dev_pointer is not None:
        # Wemo switch commands get sent to the wemo service for handling
        if devices[dev_pointer].devtype == 'wemo_switch':
            # Determine what command to issue
            out_msg = '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (
                ref_num.new(),
                service_addresses['wemo_addr'],
                service_addresses['wemo_port'],
                service_addresses['automation_addr'],
                service_addresses['automation_port'],
                message_types['wemo_sds'],
                dev_name,
                devices[dev_pointer].address,
                dev_cmd,
                devices[dev_pointer].status,
                devices[dev_pointer].last_seen)
            # Load message into output list
            log.debug('Loading completed msg: [%s]', out_msg)
            out_msg_list.append(copy.copy(out_msg))
    else:
        log.debug('Device name not found in known device table')
    # Regardless what was done with device command, perform database update
    # to mark it as processed to avoid executing it again
    log.debug('Generating RC ACK message to mark device cmd as processed')
    out_msg = '%s,%s,%s,%s,%s,%s,%s,%s' % (
        ref_num.new(),
        service_addresses['database_addr'],
        service_addresses['database_port'],
        service_addresses['automation_addr'],
        service_addresses['automation_port'],
        message_types['database_uc'],
        cmd_id,
        str(datetime.datetime.now())[:19])

    # Load message into output list
    log.debug('Loading completed msg: [%s]', out_msg)
    out_msg_list.append(copy.copy(out_msg))
    
    # Return response message
    return out_msg_list


# Process UPDATE COMMAND message **********************************************
def process_db_uc(log, ref_num, msg_header, msg_payload,
                  service_addresses, message_types):
    """ Process Database Update Command Message
        This function triggers and update query to add a timestamp to the
        "processed" column for records in the pending command table.  This
        prevents commands from being executed more than once.
    """
    # Initialize result list
    out_msg_list = []
    # Map header and payload to usable tags
    msg_source_addr = msg_header[3]
    msg_source_port = msg_header[4]
    # Map message payload to usable tags
    cmd_id = msg_payload[1]
    cmd_processed = msg_payload[2]
    # Build new message to forward to db service
    log.debug('Generating UC message to mark device cmd as processed')
    out_msg = '%s,%s,%s,%s,%s,%s,%s,%s' % (
        ref_num.new(),
        service_addresses['database_addr'],
        service_addresses['database_port'],
        msg_source_addr,
        msg_source_port,
        message_types['database_uc'],
        cmd_id,
        cmd_processed)
    # Load message into output list
    log.debug('Loading completed msg: [%s]', out_msg)
    out_msg_list.append(copy.copy(out_msg))
    # Return response message
    return out_msg_list


# Process UPDATE COMMAND ACK message ******************************************
def process_db_uc_ack(log, msg_header, msg_payload):
    """ Process Database Update Command ACK Message
        This function processes the positive ACK that is retunred when a UC
        message is successfully processed
    """
    # Log receipt of ACK for debug purposes
    log.debug('LSU ACK Received: [%s,%s]', msg_header, msg_payload)
