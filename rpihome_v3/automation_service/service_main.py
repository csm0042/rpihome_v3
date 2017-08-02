#!/usr/bin/python3
""" service_main.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import copy
import datetime
import logging
import sys
import time
import automation_service as service


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Internal Service Work Task **************************************************
@asyncio.coroutine
def service_main_task(log, ref_num, devices, msg_in_que, msg_out_que,
                      service_addresses, message_types):
    """ task to handle the work the service is intended to do """
    # Initialize timestamp for periodic DB checks
    last_check = datetime.datetime.now()
    while True:
        # Initialize result list
        out_msg_list = []
        if msg_in_que.qsize() > 0:
            log.debug('Getting Incoming message from queue')
            next_msg = msg_in_que.get_nowait()
            log.debug('Splitting message into header / payload')
            next_msg_seg = next_msg.split(sep=',')

            # Split message into header and payload
            msg_header = next_msg_seg[:5]
            msg_payload = next_msg_seg[5:]

            # Map header and payload to usable tags
            msg_ref = msg_header[0]
            msg_dest_addr = msg_header[1]
            msg_dest_port = msg_header[2]
            msg_source_addr = msg_header[3]
            msg_source_port = msg_header[4]
            msg_type = msg_payload[0]

            # Process messages from database service
            if msg_source_addr == service_addresses['database_addr']:
                # Log Status Update messages (LSU)
                if msg_type == message_types['database_lsu']:
                    log.debug('Message is a Log Status Update (LSU) message')
                    out_msg_list = service.process_db_lsu(
                        log,
                        ref_num,
                        msg_header,
                        msg_payload,
                        service_addresses,
                        message_types)
                # Log Status Update ACK messages (LSUA)
                elif msg_type == message_types['database_lsu_ack']:
                    log.debug('Message is a Log Status Update ACK (LSUA) message')
                    service.process_db_lsu_ack(
                        log,
                        msg_header,
                        msg_payload)
                # Return Command messages (RC)
                elif msg_type == message_types['database_rc']:
                    log.debug('Message is a Return Command (RC) message')
                    out_msg_list = service.process_db_rc(
                        log,
                        ref_num,
                        msg_header,
                        service_addresses,
                        message_types)
                # Return Command ACK messages (RCA)
                elif msg_type == message_types['database_rc_ack']:
                    log.debug('Message is a Return Command ACK (RCA) message')
                    out_msg_list = service.process_db_rc_ack(
                        log,
                        ref_num,
                        devices,
                        msg_payload,
                        service_addresses,
                        message_types)
                # Update Command messages (UC)
                elif msg_type == message_types['database_uc']:
                    log.debug('Message is a Update Command (UC) message')
                    out_msg_list = service.process_db_uc(
                        log,
                        ref_num,
                        msg_header,
                        msg_payload,
                        service_addresses,
                        message_types)
                # Update Command ACK messages (UCA)
                elif msg_type == message_types['database_uc_ack']:
                    log.debug('Message is a Update Command ACK (UCA) message')
                    service.process_db_uc_ack(
                        log,
                        msg_header,
                        msg_payload)

            # Process messages from wemo service
            if msg_source_addr == service_addresses['wemo_addr']:
                # Get Device Status messages (GDS)
                if msg_type == message_types['wemo_gds']:
                    log.debug('Message is a Get Device Status (GDS) message')
                    out_msg_list = service.process_wemo_gds(
                        log,
                        ref_num,
                        msg_header,
                        msg_payload,
                        service_addresses)
                # Get Device Status ACK messages (GDSA)
                elif msg_type == message_types['wemo_gds_ack']:
                    log.debug('Message is a Get Device Status ACK (GDSA) message')
                    out_msg_list = service.process_wemo_gds_ack(
                        log,
                        devices,
                        msg_payload)
                # Set Device Status messages (SDS)
                elif msg_type == message_types['wemo_sds']:
                    log.debug('Message is a Set Device Status (SDS) message')
                    out_msg_list = service.process_wemo_sds(
                        log,
                        ref_num,
                        devices,
                        msg_header,
                        msg_payload,
                        service_addresses)
                # Set Device Status ACK messages (SDSA)
                elif msg_type == message_types['wemo_sds_ack']:
                    log.debug('Message is a Set Device Status ACK (SDSA) message')
                    out_msg_list = service.process_wemo_sds_ack(
                        log,
                        devices,
                        msg_payload)

            # Process messages from calendar/schedule service
            if msg_source_addr == service_addresses['schedule_addr']:
                # Check Command Schedule messages (CCS)
                if msg_type == message_types['schedule_ccs']:
                    log.debug('Message is a Check Command Schedule (CCS) message')
                    out_msg_list = service.process_sched_ccs(
                        log,
                        ref_num,
                        msg_header,
                        msg_payload,
                        service_addresses)
                # Check Command Schedule ACK messages (CCSA)
                if msg_type == message_types['schedule_ccs_ack']:
                    log.debug('Message is a Check Command Schedule ACK (CCSA) message')
                    out_msg_list = service.process_sched_ccs_ack(
                        log,
                        ref_num,
                        devices,
                        msg_header,
                        msg_payload,
                        service_addresses,
                        message_types)                        

            # Que up response messages in outgoing msg que
            if len(out_msg_list) > 0:
                log.debug('Queueing response message(s)')
                for out_msg in out_msg_list:
                    msg_out_que.put_nowait(out_msg)
                    log.debug('Message [%s] successfully queued',
                            out_msg)

        # Periodically check scheduled on/off commands for devices
        if datetime.datetime.now() >= (last_check + datetime.timedelta(minutes=1)):
            out_msg_list = service.create_sched_ccs(
                log,
                ref_num,
                devices,
                service_addresses,
                message_types)
            last_check = datetime.datetime.now()

            # Que up response messages in outgoing msg que
            if len(out_msg_list) > 0:
                log.debug('Queueing message(s)')
                for out_msg in out_msg_list:
                    msg_out_que.put_nowait(out_msg)
                    log.debug('Message [%s] successfully queued', out_msg)
        
        # Yield to other tasks for a while
        yield from asyncio.sleep(0.25)
