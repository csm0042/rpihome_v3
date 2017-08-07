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

    # Create CCS messages for each device in the list
    for d in devices:
        if d.rule == 'schedule' or d.rule == 'dusk_to_dawn' or d.rule == '':
            out_msg = helpers.CCSmessage(
                ref=ref_num.new(),
                dest_addr=service_addresses['schedule_addr'],
                dest_port=service_addresses['schedule_port'],
                source_addr=service_addresses['automation_addr'],
                source_port=service_addresses['automation_port'],
                msg_type=message_types['schedule_ccs'],
                msg_name=d.name)

            # Load message into output list
            log.debug('Loading completed msg: [%s]', out_msg.complete)
            out_msg_list.append(out_msg.complete)

    # Return response message
    return out_msg_list


# Process messages type 301 ***************************************************
def process_sched_ccs(log, ref_num, devices, msg, service_addresses, message_types):
    """ Check Command Schedule
        This function takes any CCS messages and forwards them on to the
        schedule service.  The forwarded message is updated to contain the source
        info for the original service that initially sent the message so the
        response gets back to where the reqeust originated.
    """
    # Initialize result list
    out_msg_list = []

    # Map message into CCS message class
    message = helpers.CCSmessage()
    message.complete = msg

    # Search device table to find device name
    log.debug('Searching device table for [%s]', message.dev_name)
    dev_pointer = helpers.search_device_list(log, devices, message.dev_name)
    log.debug('Match found at device table index: %s', dev_pointer)    

    # Modify CCS message to forward to wemo service
    if dev_pointer is not None:
        message.ref = ref_num.new()
        message.dest_addr = service_addresses['schedule_addr']
        message.dest_port = service_addresses['schedule_port']
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


# Process messages type 301 ***************************************************
def process_sched_ccs_ack(log, ref_num, devices, msg, service_addresses, message_types):
    """ Check Command Schedule ACK
        This function takes any CCS ACK messages received and issues the
        appropriate device commands via messages to the appropraite services
        so those commands are executed
    """
    # Initialize result list
    out_msg_list = []

    # Map message into LSU message class
    message = helpers.CCSACKmessage()
    message.complete = msg

    # Search device table to find device name
    log.debug('Searching device table for [%s]', message.dev_name)
    dev_pointer = helpers.search_device_list(log, devices, message.dev_name)
    log.debug('Match found at device table index: %s', dev_pointer)    

    # Update values based on message content
    if dev_pointer is not None:
        log.debug('[%s] found in table at index [%s]', message.dev_name, dev_pointer)

        # Check for command change-of-state
        if devices[dev_pointer].cmd != message.dev_cmd:
            log.debug('New command detected [%s]', message.dev_cmd)
            # Snapshot command so we only issue command message once
            devices[dev_pointer].cmd = copy.copy(message.dev_cmd)

            # Issue messages to wemo servivce for wemo device commands
            if devices[dev_pointer].devtype == 'wemo_switch':
                # Build new message to forward to wemo service
                log.debug('Generating message to wemo service')
                out_msg = helpers.SDSmessage(
                    ref=ref_num.new(),
                    dest_addr=service_addresses['schedule_addr'],
                    dest_port=service_addresses['schedule_port'],
                    source_addr=message.source_addr,
                    source_port=message.source_port,
                    msg_type=message_types['wemo_sds'],
                    dev_name=message.dev_name,
                    dev_addr=devices[dev_pointer].address,
                    dev_cmd=message.dev_cmd,
                    dev_status=devices[dev_pointer].status,
                    dev_last_seen=devices[dev_pointer].last_seen)

                # Load message into output list
                log.debug('Loading completed msg: [%s]', out_msg.complete)
                out_msg_list.append(out_msg.complete)

    else:
        log.debug('Device not in device list: %s', message.dev_name) 

    # Return response message
    return out_msg_list
