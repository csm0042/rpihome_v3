#!/usr/bin/python3
""" start_service.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
from contextlib import suppress
import sys
import env
from rpihome_v3.helpers.ref_num import RefNum
from rpihome_v3.automation_service.configure import configure_log
from rpihome_v3.automation_service.configure import configure_servers
from rpihome_v3.automation_service.configure import configure_message_types
from rpihome_v3.automation_service.configure import configure_location
from rpihome_v3.automation_service.configure import configure_devices
from rpihome_v3.automation_service.service_main import service_main_task



# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Application wide objects ****************************************************
LOG = configure_log('config.ini')
SERVICE_ADDRESSES = configure_servers('config.ini', LOG)
MESSAGE_TYPES = configure_message_types('config.ini', LOG)
CUR_LAT, CUR_LONG = configure_location('config.ini', LOG)
DEVICES = configure_devices('config.ini', LOG)

REF_NUM = RefNum(log=LOG)
MSG_IN_QUEUE = asyncio.Queue()
MSG_OUT_QUEUE = asyncio.Queue()
LOOP = asyncio.get_event_loop()


# Incoming message handler ****************************************************
@asyncio.coroutine
def handle_msg_in(reader, writer):
    """ Callback used to send ACK messages back to acknowledge messages
    received """
    # Set up socket pair
    LOG.debug('Yielding to reader.read()')
    data_in = yield from reader.read(200)
    LOG.debug('Decoding read data')
    message = data_in.decode()
    LOG.debug('Extracting address from socket connection')
    addr = writer.get_extra_info('peername')
    LOG.debug('Received %r from %r', message, addr)

    # Coping incoming message to message buffer
    LOG.debug('Loading message into incoming msg buffer')
    MSG_IN_QUEUE.put_nowait(message)
    LOG.debug('Resulting buffer length: %s', str(MSG_IN_QUEUE.qsize()))

    # Acknowledge receipt of message
    LOG.debug("ACK'ing message: %r", message)
    LOG.debug('Splitting message into constituent parts')
    msg_seg = message.split(',')
    LOG.debug('Extracted msg sequence number: [%s]', msg_seg[0])
    ack_to_send = msg_seg[0].encode()
    LOG.debug('Sending response msg: [%s]', ack_to_send)
    writer.write(ack_to_send)
    yield from writer.drain()
    LOG.debug('Closing the socket after sending ACK')
    writer.close()


# Outgoing message handler ****************************************************
@asyncio.coroutine
def handle_msg_out():
    """ task to handle outgoing messages """
    while True:
        if MSG_OUT_QUEUE.qsize() > 0:
            LOG.debug('Pulling next outgoing message from queue')
            msg_to_send = MSG_OUT_QUEUE.get_nowait()
            LOG.debug('Extracting msg destination address and port')
            msg_seg_out = msg_to_send.split(',')
            LOG.debug('Opening outgoing connection to %s:%s',
                      msg_seg_out[1], msg_seg_out[2])
            try:
                reader_out, writer_out = yield from asyncio.open_connection(
                    msg_seg_out[1], int(msg_seg_out[2]), loop=LOOP)
                LOG.debug('Sending message: [%s]', msg_to_send)
                writer_out.write(msg_to_send.encode())

                LOG.debug('Waiting for ack')
                data_ack = yield from reader_out.read(200)
                ack = data_ack.decode()
                LOG.debug('Received: %r', ack)
                if ack.split(',')[0] == msg_seg_out[0]:
                    LOG.debug('Successful ACK received')
                else:
                    LOG.debug('Ack received does not match sent message')
                LOG.debug('Closing socket')
                writer_out.close()
            except Exception:
                LOG.warning('Could not open socket connection to target')
        # Yield to other tasks for a while
        yield from asyncio.sleep(0.25)


# Main ************************************************************************
def main():
    """ Main application routine """
    LOG.debug('Starting main')

    # Create incoming message server
    try:
        LOG.debug('Creating incoming message listening server at [%s:%s]',
                  SERVICE_ADDRESSES['automation_addr'],
                  SERVICE_ADDRESSES['automation_port'])
        msg_in_server = asyncio.start_server(
            handle_msg_in,
            host=SERVICE_ADDRESSES['automation_addr'],
            port=int(SERVICE_ADDRESSES['automation_port']))
        LOG.debug('Wrapping servier in future task and scheduling for '
                  'execution')
        msg_in_task = LOOP.run_until_complete(msg_in_server)
    except Exception:
        LOG.debug('Failed to create socket listening connection at %s:%s',
                  SERVICE_ADDRESSES['automation_addr'],
                  SERVICE_ADDRESSES['automation_port'])
        sys.exit()

    # Create main task for this service
    LOG.debug('Scheduling main task for execution')
    asyncio.ensure_future(
        service_main_task(
            LOG,
            REF_NUM,
            DEVICES,
            MSG_IN_QUEUE,
            MSG_OUT_QUEUE,
            SERVICE_ADDRESSES,
            MESSAGE_TYPES))

    # Create outgoing message task
    LOG.debug('Scheduling outgoing message task for execution')
    asyncio.ensure_future(handle_msg_out())

    # Serve requests until Ctrl+C is pressed
    LOG.info('Automation Service')
    LOG.info('Serving on {}'.format(msg_in_task.sockets[0].getsockname()))
    LOG.info('Press CTRL+C to exit')
    try:
        LOOP.run_forever()
    except asyncio.CancelledError:
        LOG.info('All tasks have been cancelled')
    except KeyboardInterrupt:
        pass
    finally:
        LOG.info('Shutting down incoming message server')
        msg_in_server.close()
        LOG.info('Finding all running tasks to shut down')
        pending = asyncio.Task.all_tasks()
        LOG.info('[%s] Task still running.  Closing them now', str(len(pending)))
        for i, task in enumerate(pending):
            with suppress(asyncio.CancelledError):
                LOG.info('Waiting for task [%s] to shut down', i)
                task.cancel()
                LOOP.run_until_complete(task)
        LOG.info('Shutdown complete.  Terminating execution LOOP')

    # Terminate the execution LOOP
    LOOP.close()


# Call Main *******************************************************************
if __name__ == "__main__":
    main()
