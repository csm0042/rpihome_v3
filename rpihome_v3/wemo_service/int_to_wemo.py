#!/usr/bin/python3
""" int_to_wemo.py:
"""

# Im_port Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import copy
import env
from rpihome_v3.messages.message_gds import GDSmessage
from rpihome_v3.messages.message_gds_ack import GDSACKmessage
from rpihome_v3.messages.message_sds import SDSmessage
from rpihome_v3.messages.message_sds_ack import SDSACKmessage
from rpihome_v3.messages.message_wwu import WWUmessage
from rpihome_v3.messages.message_wwu_ack import WWUACKmessage



# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# ACK wake-up message *********************************************************
@asyncio.coroutine
def check_wemo_service(log, ref_num, msg, message_types):
    """ function to ack wake-up requests to wemo service """
    # Initialize result list
    out_msg_list = []

    # Map message into wemo wake-up message class
    message = WWUmessage(log=log)
    message.complete = msg

    # Send response indicating query was executed
    log.debug('Building response message header')
    out_msg = WWUACKmessage(
        log=log,
        ref=ref_num.new(),
        dest_addr=message.source_addr,
        dest_port=message.source_port,
        source_addr=message.dest_addr,
        source_port=message.dest_port,
        msg_type=message_types['wemo_wu_ack'])

    # Load message into output list
    log.debug('Loading completed msg: [%s]', out_msg.complete)
    out_msg_list.append(out_msg.complete)

    # Return response message
    return out_msg_list


# Internal Service Work Subtask - wemo get status *****************************
@asyncio.coroutine
def get_wemo_status(log, ref_num, wemo_gw, msg, message_types):
    """ Function to properly process wemo device status requests """
    # Initialize result list
    out_msg_list = []

    # Map message into GDS message class
    message = GDSmessage(log=log)
    message.complete = msg    

    # Execute Status Update
    log.debug('Requesting status for [%s] at [%s] with original status '
              '[%s] and update time [%s]',
              message.dev_name,
              message.dev_addr,
              message.dev_status,
              message.dev_last_seen)
    dev_status_new, dev_last_seen_new = wemo_gw.read_status(
        message.dev_name,
        message.dev_addr,
        message.dev_status,
        message.dev_last_seen)

    # Send response indicating query was executed
    log.debug('Building response message header')
    out_msg = GDSACKmessage(
        log=log,
        ref=ref_num.new(),
        dest_addr=message.source_addr,
        dest_port=message.source_port,
        source_addr=message.dest_addr,
        source_port=message.dest_port,
        msg_type=message_types['wemo_gds_ack'],
        dev_name=message.dev_name,
        dev_status=str(dev_status_new),
        dev_last_seen=str(dev_last_seen_new)[:19])

    # Load message into output list
    log.debug('Loading completed msg: [%s]', out_msg.complete)
    out_msg_list.append(out_msg.complete)

    # Return response message
    return out_msg_list


# Internal Service Work Subtask - wemo turn on ********************************
@asyncio.coroutine
def set_wemo_state(log, ref_num, wemo_gw, msg, message_types):
    """ Function to set state of wemo device to "on" """
    # Initialize result list
    out_msg_list = []

    # Map message into CCS message class
    message = SDSmessage(log=log)
    message.complete = msg

    # Execute wemo on commands
    if message.dev_cmd == '1' or message.dev_cmd == 'on':
        log.debug('Commanding wemo device [%s] to "on"', message.dev_name)
        dev_status_new, dev_last_seen_new = wemo_gw.turn_on(
            message.dev_name,
            message.dev_addr,
            message.dev_status,
            message.dev_last_seen)

    # Execute wemo off commands
    elif message.dev_cmd == '0' or message.dev_cmd == 'off':
        log.debug('Commanding wemo device [%s] to "off"', message.dev_name)
        dev_status_new, dev_last_seen_new = wemo_gw.turn_off(
            message.dev_name,
            message.dev_addr,
            message.dev_status,
            message.dev_last_seen)

    # If command not valid, leave device un-changed
    else:
        log.warning('Invalid command [%s] for device [%s]',
                    message.dev_cmd,
                    message.dev_name)
        dev_status_new = copy.copy(message.dev_status)
        dev_last_seen_new = copy.copy(message.dev_last_seen)

    # Send response indicating command was executed
    log.debug('Building response message')
    out_msg = SDSACKmessage(
        log=log,
        ref=ref_num.new(),
        dest_addr=message.source_addr,
        dest_port=message.msg_source_port,
        source_addr=message.msg_dest_addr,
        source_port=message.msg_dest_port,
        msg_type=message_types['wemo_sds_ack'],
        dev_name=message.dev_name,
        dev_status=dev_status_new,
        dev_last_seen=dev_last_seen_new)

    # Load message into output list
    log.debug('Loading completed msg: [%s]', out_msg.complete)
    out_msg_list.append(out_msg.complete)

    # Return response message
    return out_msg_list
