#!/usr/bin/python3
""" interface_to_schedule.py:
"""

# Im_port Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import copy
if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from rpihome_v3.messages.heartbeat import HeartbeatMessage
from rpihome_v3.messages.heartbeat_ack import HeartbeatMessageACK
from rpihome_v3.messages.get_device_scheduled_state import GetDeviceScheduledStateMessage
from rpihome_v3.messages.get_device_scheduled_state_ack import GetDeviceScheduledStateMessageACK


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


def create_heartbeat_msg(log, ref_num, destinations, source_addr, source_port, message_types):
    """ function to create one or more heartbeat messages """
    # Initialize result list
    out_msg_list = []

    # Generate a heartbeat message for each destination given
    for entry in destinations:
        out_msg = HeartbeatMessage(
            log=log,
            ref=ref_num.new(),
            dest_addr=entry[0],
            dest_port=entry[1],
            source_addr=source_addr,
            source_port=source_port,
            msg_type=message_types['heartbeat']
        )
        # Load message into output list
        log.debug('Loading completed msg: %s', out_msg.complete)
        out_msg_list.append(out_msg.complete)

    # Return response message
    return out_msg_list


def process_heartbeat_msg(log, ref_num, msg, message_types):
    """ function to ack wake-up requests to wemo service """
    # Initialize result list
    out_msg_list = []

    # Map message into wemo wake-up message class
    message = HeartbeatMessage(log=log)
    message.complete = msg

    # Send response indicating query was executed
    log.debug('Building response message header')
    out_msg = HeartbeatMessageACK(
        log=log,
        ref=ref_num.new(),
        dest_addr=message.source_addr,
        dest_port=message.source_port,
        source_addr=message.dest_addr,
        source_port=message.dest_port,
        msg_type=message_types['heartbeat_ack'])

    # Load message into output list
    log.debug('Loading completed msg: [%s]', out_msg.complete)
    out_msg_list.append(out_msg.complete)

    # Return response message
    return out_msg_list


# Process messages type 100 ***************************************************
def process_get_device_scheduled_state_msg(log, ref_num, schedule, msg, message_types):
    """
    """
    # Initialize result list
    out_msg_list = []

    # Map message into LSU message class
    message = GetDeviceScheduledStateMessage(log=log)
    message.complete = msg

    # Check schedule for device
    log.debug('Checking schedule to determine desired state of device [%s]',
              message.dev_name)
    desired_cmd = schedule.check_schedule(name=message.dev_name)

    # Create ACK message (type 301) with desired device state per schedule
    if desired_cmd is True:
        log.debug('Device [%s] should be "on" according to schedule', message.dev_name)
        out_msg = GetDeviceScheduledStateMessageACK(
            ref=ref_num.new(),
            dest_addr=message.source_addr,
            dest_port=message.source_port,
            source_addr=message.dest_addr,
            source_port=message.dest_port,
            msg_type=message_types['get_device_scheduled_state_ack'],
            dev_name=message.dev_name,
            dev_cmd='on')
    else:
        log.debug('Device [%s] should be "off" according to schedule', message.dev_name)
        out_msg = GetDeviceScheduledStateMessageACK(
            ref=ref_num.new(),
            dest_addr=message.source_addr,
            dest_port=message.source_port,
            source_addr=message.dest_addr,
            source_port=message.dest_port,
            msg_type=message_types['get_device_scheduled_state_ack'],
            dev_name=message.dev_name,
            dev_cmd='off')

    # Load revised message into output list
    log.debug('Loading completed msg: %s', out_msg.complete)
    out_msg_list.append(out_msg.complete)

    # Return response message
    return out_msg_list
