#!/usr/bin/python3
""" interface_to_database.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import copy
import database_service as service


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Internal Service Work Subtask - log status updates **************************
@asyncio.coroutine
def process_db_lsu(log, ref_num, database, msg_header, msg_payload,
                   message_types):
    """ Function to insert status updates into device_log table """
    # Initialize result list
    out_msg_list = []

    # Map message header & payload to usable tags
    msg_ref = msg_header[0]
    msg_dest_addr = msg_header[1]
    msg_dest_port = msg_header[2]
    msg_source_addr = msg_header[3]
    msg_source_port = msg_header[4]
    msg_type = msg_payload[0]
    dev_name = msg_payload[1]
    dev_addr = msg_payload[2]
    dev_status = msg_payload[3]
    dev_last_seen = msg_payload[4]

    # Execute Insert Query
    log.debug('Logging status change to database for [%s].  New '
              'status is [%s] with a last seen time of [%s]',
              dev_name,
              dev_status,
              dev_last_seen)
    service.insert_record(
        log,
        database,
        dev_name,
        dev_status,
        dev_last_seen)

    # Send response indicating query was executed
    log.debug('Building LSU ACK message')
    out_msg = '%s,%s,%s,%s,%s,%s,%s' % (
        ref_num.new(),
        msg_source_addr,
        msg_source_port,
        msg_dest_addr,
        msg_dest_port,
        message_types['database_LSU_ACK'],
        dev_name)

    # Load message into output list
    log.debug('Loading completed msg: [%s]', out_msg)
    out_msg_list.append(copy.copy(out_msg))

    # Return response message
    return out_msg_list


# Internal Service Work Subtask - wemo turn on ********************************
@asyncio.coroutine
def process_db_rc(log, ref_num, database, msg_dest_addr, msg_dest_port,
                  msg_source_addr, msg_source_port, message_types):
    """ Function to query database for any un-processed device commands """
    # Initialize result list
    out_msg_list = []
    result_list = []

    # Execute select Query
    log.debug('Querying database for pending device commands')
    result_list = service.query_command(
        log,
        database)

    # Send response message for each record returned by query
    if len(result_list) <= 0:
        log.debug('Preparing response messages for pending commands')
        for pending_cmd in result_list:
            # Determine what command to issue
            out_msg = '%s,%s,%s,%s,%s,%s,%s' % (
                ref_num.new(),
                msg_dest_addr,
                msg_dest_port,
                msg_source_addr,
                msg_source_port,
                message_types['database_RC'],
                pending_cmd)

            # Load message into output list
            log.debug('Loading completed msg: [%s]', out_msg)
            out_msg_list.append(copy.copy(out_msg))
    else:
        log.debug('No pending commands found')

    # Return list of response messages from query
    return out_msg_list


# Internal Service Work Subtask - wemo turn off *******************************
@asyncio.coroutine
def process_db_uc(log, ref_num, database, msg_header, msg_payload, message_types):
    """ Function to set state of wemo device to "off" """
    # Initialize result list
    out_msg_list = []

    # Map message header to usable tags
    msg_ref = msg_header[0]
    msg_dest_addr = msg_header[1]
    msg_dest_port = msg_header[2]
    msg_source_addr = msg_header[3]
    msg_source_port = msg_header[4]
    # Map message payload to usable tags
    msg_type = msg_payload[0]
    cmd_id = msg_payload[1]
    cmd_processed = msg_payload[2]

    # Execute update Query
    log.debug('Querying database to mark command with ID [%s] as complete '
              'with timestamp [%s]',
              cmd_id,
              cmd_processed)
    service.update_command(
        log,
        database,
        cmd_id,
        cmd_processed)

    # Send response indicating query was executed
    log.debug('Building response message header')
    out_msg = '%s,%s,%s,%s,%s,%s,%s' % (
        ref_num.new(),
        msg_source_addr,
        msg_source_port,
        msg_dest_addr,
        msg_dest_port,
        message_types['database_UC_ACK'],
        cmd_id)

    # Load message into output list
    log.debug('Loading completed msg: [%s]', out_msg)
    out_msg_list.append(copy.copy(out_msg))

    # Return response message
    return out_msg_list
