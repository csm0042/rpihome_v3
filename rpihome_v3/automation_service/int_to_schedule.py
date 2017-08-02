#!/usr/bin/python3
""" interface_to_cal.py:
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


# Create CHECK COMMAND SCHEDULE messages **************************************
def create_sched_ccs(log, ref_num, devices, service_addresses, message_types):
    """ Check Command Schedule Message
        This function triggers an message for each device in the device table
        requesting that the scheduling service decide if they should be on or
        off based upon the device schedule.
    """
    # Initialize result list
    out_msg_list = []
    out_msg = str()
    # Create CCS messages for each device in the list
    for d in devices:
        if d.rule == 'schedule' or d.rule == 'dusk_to_dawn' or d.rule == '':
            out_msg = '%s,%s,%s,%s,%s,%s,%s' % (
                ref_num.new(),
                service_addresses['schedule_addr'],
                service_addresses['schedule_port'],
                service_addresses['automation_addr'],
                service_addresses['automation_port'],
                message_types['schedule_ccs'],
                d.name)
            # Load message into output list
            log.debug('Loading completed msg: [%s]', out_msg)
            out_msg_list.append(copy.copy(out_msg))
    # Return response message    
    return out_msg_list


# Process messages type 301 ***************************************************
def process_sched_ccs(log, ref_num, msg_header, msg_payload, service_addresses):
    """ Check Command Schedule
        This function takes any CCS messages and forwards them on to the
        schedule service.  The forwarded message is updated to contain the source
        info for the original service that initially sent the message so the
        response gets back to where the reqeust originated.
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

    # Build new message to forward to wemo service
    log.debug('Generating message to forward to schedule service')
    out_msg = '%s,%s,%s,%s,%s,%s,%s' % (
        ref_num.new(),
        service_addresses['schedule_addr'],
        service_addresses['schedule_port'],
        msg_source_addr,
        msg_source_port,
        msg_type,
        dev_name)

    # Load message into output list
    log.debug('Loading completed msg: [%s]', out_msg)
    out_msg_list.append(copy.copy(out_msg))

    # Return response message
    return out_msg_list


# Process messages type 301 ***************************************************
def process_sched_ccs_ack(log, ref_num, devices, msg_header, msg_payload,
                          service_addresses, message_types):
    """ Check Command Schedule ACK
        This function takes any CCS ACK messages received and issues the
        appropriate device commands via messages to the appropraite services
        so those commands are executed
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
    dev_cmd = msg_payload[2]

    # Search device table to find device name
    log.debug('Searching device table for [%s]', dev_name)
    dev_pointer = helpers.search_device_list(log, devices, dev_name)

    # Update values based on message content
    if dev_pointer is not None:
        log.debug('[%s] found in table at index [%s]', dev_name, dev_pointer)

        # Check for command change-of-state
        if devices[dev_pointer].cmd != dev_cmd:
            log.debug('New command detected [%s]', dev_cmd)
            # Snapshot command so we only issue command message once
            devices[dev_pointer].cmd = copy.copy(dev_cmd)

            # Issue messages to wemo servivce for wemo device commands
            if devices[dev_pointer].devtype == 'wemo_switch':
                # Build new message to forward to wemo service
                log.debug('Generating message to wemo service for wemo '
                          'device [%s]', dev_name)
                out_msg = '%s,%s,%s,%s,%s,%s,%s,%s' % (
                    ref_num.new(),
                    service_addresses['wemo_addr'],
                    service_addresses['wemo_port'],
                    service_addresses['automation_addr'],
                    service_addresses['automation_port'],
                    message_types['wemo_sds'],
                    dev_name,
                    devices[dev_pointer].address,
                    dev_cmd)
                # Load message into output list
                log.debug('Loading completed msg: [%s]', out_msg)
                out_msg_list.append(copy.copy(out_msg))

    # Return response message
    return out_msg_list
