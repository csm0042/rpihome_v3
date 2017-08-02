#!/usr/bin/python3
""" interface_to_wemo.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import copy
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


# Process GET DEVICE STATUS message *******************************************
def process_wemo_gds(log, ref_num, msg_header, msg_payload, service_addresses):
    """ Get Device Status
        This function takes any GDS messages and forwards them on to the
        wemo service.  The forwarded message is updated to contain the source
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
    # Map message payload to usable tags
    msg_type = msg_payload[0]
    dev_name = msg_payload[1]
    dev_addr = msg_payload[2]
    dev_status = msg_payload[3]
    dev_last_seen = msg_payload[4]

    # Build new message to forward to wemo service
    log.debug('Generating message to forward to wemo service')
    out_msg = '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (
        ref_num.new(),
        service_addresses['wemo_addr'],
        service_addresses['wemo_port'],
        msg_source_addr,
        msg_source_port,
        msg_type,
        dev_name,
        dev_addr,
        dev_status,
        dev_last_seen)

    # Load message into output list
    log.debug('Loading completed msg: [%s]', out_msg)
    out_msg_list.append(copy.copy(out_msg))

    # Return response message
    return out_msg_list


# Process messages type 201 ***************************************************
def process_wemo_gds_ack(log, devices, msg_payload):
    """ Get Device Status ACK
        This function takes a type 201 messages uses it to update the status
        of a device as currently defined in the device list.
    """
    # Initialize result list
    out_msg_list = []

    # Map message payload to usable tags
    msg_type = msg_payload[0]
    dev_name = msg_payload[1]
    dev_status = msg_payload[2]
    dev_last_seen = msg_payload[3]

    # Search device table to find device name
    log.debug('Searching device table for [%s]', dev_name)
    dev_pointer = helpers.search_device_list(log, devices, dev_name)

    # Update values based on message content
    if dev_pointer is not None:
        log.debug('Updating device [%s] status to [%s] and last seen to [%s]',
                  dev_name,
                  dev_status,
                  dev_last_seen)
        devices[dev_pointer].status = copy.copy(dev_status)
        devices[dev_pointer].last_seen = copy.copy(dev_last_seen)
    else:
        log.debug('Device [%s] not found in active device table. '
                  'No further action being taken', dev_name)

    # Return response message
    return out_msg_list


# Process messages type 202 ***************************************************
def process_wemo_sds(log, ref_num, devices, msg_header, msg_payload, service_addresses):
    """ Set Device Status
        This function takes any SDS messages and forwards them on to the
        wemo service.  The forwarded message is updated to contain the source
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
    dev_addr = msg_payload[2]
    dev_cmd = msg_payload[3]

    # Search device table to find device name
    log.debug('Searching device table for [%s]', dev_name)
    dev_pointer = helpers.search_device_list(log, devices, dev_name)

    # Update values based on message content
    if dev_pointer is not None:
        # Build new message to forward to wemo service
        log.debug('Generating SDS message to forward to wemo service')
        out_msg = '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (
            ref_num.new(),
            service_addresses['wemo_addr'],
            service_addresses['wemo_port'],
            msg_source_addr,
            msg_source_port,
            msg_type,
            dev_name,
            dev_addr,
            dev_cmd,
            devices[dev_pointer].status,
            devices[dev_pointer].last_seen)
        # Load message into output list
        log.debug('Loading completed msg: [%s]', out_msg)
        out_msg_list.append(copy.copy(out_msg))
    else:
        log.debug('Device [%s] not found in active device table. '
                  'No further action being taken', dev_name)

    # Return response message
    return out_msg_list


# Process messages type 203 ***************************************************
def process_wemo_sds_ack(log, devices, msg_payload):
    """ Set Device Status ACK
        This function takes a SDS ACK message and uses it to update the status
        of a device as currently defined in the device list.
    """
    # Initialize result list
    out_msg_list = []

    # Map message payload to usable tags
    msg_type = msg_payload[0]
    dev_name = msg_payload[1]
    dev_status = msg_payload[2]
    dev_last_seen = msg_payload[3]

    # Search device table to find device name
    log.debug('Searching device table for [%s]', dev_name)
    dev_pointer = helpers.search_device_list(log, devices, dev_name)

    # Update values based on message content
    if dev_pointer is not None:
        log.debug('Updating device [%s] status to [%s] and last seen to [%s]',
                  dev_name,
                  dev_status,
                  dev_last_seen)
        devices[dev_pointer].status = copy.copy(dev_status)
        devices[dev_pointer].last_seen = copy.copy(dev_last_seen)
    else:
        log.debug('Device [%s] not found in active device table. '
                  'No further action being taken', dev_name)

    # Return response message
    return out_msg_list
