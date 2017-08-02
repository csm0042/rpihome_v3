#!/usr/bin/python3
""" int_to_wemo.py:
"""

# Im_port Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import copy
import datetime


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Internal Service Work Subtask - wemo get status *****************************
@asyncio.coroutine
def get_wemo_status(log, ref_num, wemo_gw, msg_header, msg_payload, message_types):
    """ Function to properly process wemo device status requests """
    # Initialize result list
    out_msg_list = []

    # Map message header to usable tags
    msg_ref = msg_header[0]
    msg_dest_addr = msg_header[1]
    msg_dest_port = msg_header[2]
    msg_source_addr = msg_header[3]
    msg_source_port = msg_header[4]
    dev_name = msg_payload[1]
    dev_addr = msg_payload[2]
    dev_status = msg_payload[3]
    dev_last_seen = msg_payload[4]

    # Execute Status Update
    log.debug('Requesting status for [%s] at [%s] with original status '
              '[%s] and update time [%s]',
              dev_name,
              dev_addr,
              dev_status,
              dev_last_seen)
    dev_status_new, dev_last_seen_new = wemo_gw.read_status(
        dev_name,
        dev_addr,
        dev_status,
        dev_last_seen)

    # Send response indicating query was executed
    log.debug('Building response message header')
    out_msg = '%s,%s,%s,%s,%s,%s,%s,%s,%s' % (
        ref_num.new(),
        msg_source_addr,
        msg_source_port,
        msg_dest_addr,
        msg_dest_port,
        message_types['wemo_gds_ack'],
        dev_name,
        str(dev_status_new),
        str(dev_last_seen_new)[:19])

    # Load message into output list
    log.debug('Loading completed msg: [%s]', out_msg)
    out_msg_list.append(copy.copy(out_msg))

    # Return response message
    return out_msg_list


# Internal Service Work Subtask - wemo turn on ********************************
@asyncio.coroutine
def set_wemo_state(log, ref_num, wemo_gw, msg_header, msg_payload, message_types):
    """ Function to set state of wemo device to "on" """
    # Initialize result list
    out_msg_list = []

    # Map message header to usable tags
    msg_ref = msg_header[0]
    msg_dest_addr = msg_header[1]
    msg_dest_port = msg_header[2]
    msg_source_addr = msg_header[3]
    msg_source_port = msg_header[4]
    dev_name = msg_payload[1]
    dev_addr = msg_payload[2]
    dev_cmd = msg_payload[3]
    dev_status = msg_payload[4]
    dev_last_seen = msg_payload[5]

    # Execute wemo on commands
    if dev_cmd == '1' or dev_cmd == 'on':
        log.debug('Commanding wemo device [%s] to "on"', dev_name)
        dev_status_new, dev_last_seen_new = wemo_gw.turn_on(
            dev_name,
            dev_addr,
            dev_status,
            dev_last_seen)

    # Execute wemo off commands
    elif dev_cmd == '0' or dev_cmd == 'off':
        log.debug('Commanding wemo device [%s] to "off"', dev_name)
        dev_status_new, dev_last_seen_new = wemo_gw.turn_off(
            dev_name,
            dev_addr,
            dev_status,
            dev_last_seen)

    # If command not valid, leave device un-changed
    else:
        log.warning('Invalid command [%s] for device [%s]',
                    dev_cmd,
                    dev_name)
        dev_status_new = copy.copy(dev_status)
        dev_last_seen_new = copy.copy(dev_last_seen)

    # Send response indicating command was executed
    log.debug('Building response message')
    out_msg = '%s,%s,%s,%s,%s,%s,%s,%s,%s' % (
        ref_num.new(),
        msg_source_addr,
        msg_source_port,
        msg_dest_addr,
        msg_dest_port,
        message_types['wemo_sds_ack'],
        dev_name,
        dev_status_new,
        dev_last_seen_new)

    # Load message into output list
    log.debug('Loading completed msg: [%s]', out_msg)
    out_msg_list.append(copy.copy(out_msg))

    # Return response message
    return out_msg_list
