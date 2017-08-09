#!/usr/bin/python3
""" interface_to_schedule.py:
"""

# Im_port Required Libraries (Standard, Third Party, Local) ********************
import copy
import env
from rpihome_v3.messages.message_ccs import CCSmessage
from rpihome_v3.messages.message_ccs_ack import CCSACKmessage



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
def process_sched_ccs(log, ref_num, schedule, msg, message_types):
    """
    """
    # Initialize result list
    out_msg_list = []

    # Map message into LSU message class
    message = CCSmessage(log=log)
    message.complete = msg

    # Check schedule for device
    log.debug('Checking schedule to determine desired state of device [%s]',
              message.dev_name)
    desired_cmd = schedule.check_schedule(name=message.dev_name)

    # Create ACK message (type 301) with desired device state per schedule
    if desired_cmd is True:
        log.debug('Device [%s] should be "on" according to schedule', message.dev_name)
        out_msg = CCSACKmessage(
            ref=ref_num.new(),
            dest_addr=message.source_addr,
            dest_port=message.source_port,
            source_addr=message.dest_addr,
            source_port=message.dest_port,
            msg_type=message_types['schedule_ccs_ack'],
            dev_name=message.dev_name,
            dev_cmd='on')
    else:
        log.debug('Device [%s] should be "off" according to schedule', message.dev_name)
        out_msg = CCSACKmessage(
            ref=ref_num.new(),
            dest_addr=message.source_addr,
            dest_port=message.source_port,
            source_addr=message.dest_addr,
            source_port=message.dest_port,
            msg_type=message_types['schedule_ccs_ack'],
            dev_name=message.dev_name,
            dev_cmd='off')

    # Load revised message into output list
    log.debug('Loading completed msg: %s', message.complete)
    out_msg_list.append(message.complete)

    # Return response message
    return out_msg_list
