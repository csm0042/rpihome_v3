#!/usr/bin/python3
""" interface_to_schedule.py:
"""

# Im_port Required Libraries (Standard, Third Party, Local) ********************
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


# Process messages type 100 ***************************************************
def process_sched_ccs(log, ref_num, calendar, msg_header, msg_payload,
                      message_types):
    """ 
    """
    # Initialize result list
    out_msgList = []
    
    # Map header and payload to usable tags
    msg_ref = msg_header[0]
    msg_dest_addr = msg_header[1]
    msg_dest_port = msg_header[2]
    msg_source_addr = msg_header[3]
    msg_source_port = msg_header[4]
    msg_type = msg_payload[0]
    dev_name = msg_payload[1]

    # Check schedule for device
    log.debug('Checking schedule to determine desired state of device [%s]',
              dev_name)
    desired_cmd = calendar.check_schedule(name=dev_name)
    
    # Create ACK message (type 301) with desired device state per schedule
    if desired_cmd is True:
        log.debug('Device [%s] should be "on" according to schedule', dev_name)
        out_msg = '%s,%s,%s,%s,%s,%s,%s,%s' % (
            ref_num.new(),
            msg_source_addr,
            msg_source_port,
            msg_dest_addr,
            msg_dest_port,
            message_types['schedule_CCS_ACK'],
            dev_name,
            'on')
    else:
        log.debug('Device [%s] should be "off" according to schedule', dev_name)
        out_msg = '%s,%s,%s,%s,%s,%s,%s,%s' % (
            ref_num.new(),
            msg_source_addr,
            msg_source_port,
            msg_dest_addr,
            msg_dest_port,
            message_types['schedule_CCS_ACK'],
            dev_name,
            'off')
    
    # Append response message (type 301) to outgoing msg queue
    log.debug('Returning message: [%s]', out_msg)
    out_msgList.append(copy.copy(out_msg))
    
    # Return response message
    return out_msgList
