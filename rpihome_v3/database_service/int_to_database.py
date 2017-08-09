#!/usr/bin/python3
""" interface_to_database.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import copy
import env
from rpihome_v3.messages.message_lsu import LSUmessage
from rpihome_v3.messages.message_lsu_ack import LSUACKmessage
from rpihome_v3.messages.message_rc import RCmessage
from rpihome_v3.messages.message_rc_ack import RCACKmessage
from rpihome_v3.messages.message_uc import UCmessage
from rpihome_v3.messages.message_uc_ack import UCACKmessage
from rpihome_v3.database_service.persistance import insert_record
from rpihome_v3.database_service.persistance import query_command
from rpihome_v3.database_service.persistance import update_command


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
def process_db_lsu(log, ref_num, database, msg, message_types):
    """ Function to insert status updates into device_log table """
    # Initialize result list
    out_msg_list = []

    # Map message header & payload to usable tags
    message = LSUmessage(log=log)
    message.complete = msg

    # Execute Insert Query
    log.debug('Logging status change to database for [%s].  New '
              'status is [%s] with a last seen time of [%s]',
              message.dev_name,
              message.dev_status,
              message.dev_last_seen)
    insert_record(
        log,
        database,
        message.dev_name,
        message.dev_status,
        message.dev_last_seen)

    # Send response indicating query was executed
    log.debug('Building LSU ACK message')
    out_msg = LSUACKmessage(
        log=log,
        ref=ref_num.new(),
        dest_addr=message.source_addr,
        dest_port=message.source_port,
        source_addr=message.dest_addr,
        source_port=message.dest_port,
        msg_type=message_types['database_LSU_ACK'],
        dev_name=message.dev_name)

    # Load message into output list
    log.debug('Loading completed msg: [%s]', out_msg.complete)
    out_msg_list.append(out_msg.complete)

    # Return response message
    return out_msg_list


# Internal Service Work Subtask - wemo turn on ********************************
@asyncio.coroutine
def process_db_rc(log, ref_num, database, msg, message_types):
    """ Function to query database for any un-processed device commands """
    # Initialize result list
    out_msg_list = []
    result_list = []

    # Map message header & payload to usable tags
    message = RCmessage(log=log)
    message.complete = msg

    # Execute select Query
    log.debug('Querying database for pending device commands')
    result_list = query_command(
        log,
        database)

    # Send response message for each record returned by query
    if len(result_list) > 0:
        log.debug('Preparing response messages for pending commands')
        for pending_cmd in result_list:           
            # Create message RC ACK message to automation service
            out_msg = RCACKmessage(
                log=log,
                ref=ref_num.new(),
                dest_addr=message.source_addr,
                dest_port=message.source_port,
                source_addr=message.dest_addr,
                source_port=message.dest_port,
                msg_type=message_types['database_rc_ack'],
                dev_id=copy.copy(pending_cmd[0]),
                dev_name=copy.copy(pending_cmd[1]),
                dev_cmd=copy.copy(pending_cmd[2]),
                dev_timestamp=copy.copy(pending_cmd[3]),
                dev_processed=copy.copy(pending_cmd[4]))

            # Load message into output list
            log.debug('Loading completed msg: [%s]', out_msg.complete)
            out_msg_list.append(out_msg.complete)
    else:
        log.debug('No pending commands found')

    # Return list of response messages from query
    return out_msg_list


# Internal Service Work Subtask - wemo turn off *******************************
@asyncio.coroutine
def process_db_uc(log, ref_num, database, msg, message_types):
    """ Function to set state of wemo device to "off" """
    # Initialize result list
    out_msg_list = []

    # Map message header & payload to usable tags
    message = UCmessage(log=log)
    message.complete = msg

    # Execute update Query
    log.debug('Querying database to mark command with ID [%s] as complete '
              'with timestamp [%s]',
              message.dev_id,
              message.dev_processed)
    update_command(
        log,
        database,
        message.dev_id,
        message.dev_processed)

    # Send response indicating query was executed
    log.debug('Building response message header')
    out_msg = UCACKmessage(
        log=log,
        ref=ref_num.new(),
        dest_addr=message.source_addr,
        dest_port=message.source_port,
        source_addr=message.dest_addr,
        source_port=message.dest_port,
        msg_type=message_types['database_uc_ack'],
        dev_id=message.dev_id)

    # Load message into output list
    log.debug('Loading completed msg: [%s]', out_msg.complete)
    out_msg_list.append(out_msg.complete)

    # Return response message
    return out_msg_list
