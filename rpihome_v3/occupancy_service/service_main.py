#!/usr/bin/python3
""" service_main.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import datetime
import env


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
def service_main_task(log, ref_num, occupancy_monitor, msg_in_que, msg_out_que,
                      service_addresses, message_types):
    """ task to handle the work the service is intended to do """
    log.debug('Starting main task')
    # Initialize timestamp for periodic DB checks
    last_check = datetime.datetime.now()
    while True:
        # Initialize result list
        out_msg_list = []

        if msg_in_que.qsize() > 0:
            log.debug('Getting Incoming message from queue')
            next_msg = msg_in_que.get_nowait()
            log.debug('Message pulled from queue: [%s]', next_msg)

            # Determine message type
            next_msg_split = next_msg.split(',')
            if len(next_msg_split) >= 6:
                log.debug('Extracting source address and message type')
                msg_source_addr = next_msg_split[1]
                msg_type = next_msg_split[5]
                log.debug('Source Address: %s', msg_source_addr)
                log.debug('Message Type: %s', msg_type)


            # Register new devices to monitor
            if msg_type == message_types['occupancy_rod']:
                log.debug('Message is a request to register a device for '
                          'occupancy checking')
                out_msg_list = yield from occupancy_monitor.register(
                    next_msg,
                    message_types)


            # Que up response messages in outgoing msg que
            if len(out_msg_list) > 0:
                log.debug('Queueing response message(s)')
                for out_msg in out_msg_list:
                    msg_out_que.put_nowait(out_msg)
                    log.debug('Message [%s] successfully queued', out_msg)


        # Periodically check state of devices
        if datetime.datetime.now() >= (last_check + datetime.timedelta(seconds=1)):
            log.debug('Performing occupancy check')
            out_msg_list = occupancy_monitor.check_all()
            last_check = datetime.datetime.now()

            # Que up response messages in outgoing msg que
            if len(out_msg_list) > 0:
                log.debug('Queueing message(s)')
                for out_msg in out_msg_list:
                    msg_out_que.put_nowait(out_msg)
                    log.debug('Message [%s] successfully queued', out_msg)



        # Yield to other tasks for a while
        yield from asyncio.sleep(0.25)
