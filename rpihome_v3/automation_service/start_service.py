#!/usr/bin/python3
""" start_service.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import copy
import logging
import sys
import time
if __name__ == "__main__":
    sys.path.append("..")
import automation_service as service
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


# Application wide objects ****************************************************
log = service.configure_log('config.ini')
address, port = service.configure_server('config.ini', log)
db_add, db_port = service.configure_db_connection('config.ini', log)
wemo_add, wemo_port = service.configure_wemo_connection('config.ini', log)
cur_lat, cur_long = service.configure_location('config.ini', log)
devices = service.configure_devices('config.ini', log)

rNumGen = helpers.RefNum()
msg_in_que = asyncio.Queue()
msg_out_que = asyncio.Queue()
loop = asyncio.get_event_loop()


# Incoming message handler ****************************************************
@asyncio.coroutine
def handle_msg_in(reader, writer):
    """ Callback used to send ACK messages back to acknowledge messages
    received """
    log.debug('Yielding to reader.read()')
    data_in = yield from reader.read(200)
    log.debug('Decoding read data')
    message = data_in.decode()
    log.debug('Extracting address from socket connection')
    addr = writer.get_extra_info('peername')
    log.debug('Received %r from %r' % (message, addr))

    # Coping incoming message to message buffer
    log.debug('Loading message into incoming msg buffer')
    msg_in_que.put_nowait(message)
    log.debug('Resulting buffer length: %s', str(msg_in_que.qsize()))

    # Acknowledge receipt of message
    log.debug("ACK'ing message: %r", message)
    log.debug('Splitting message into constituent parts')
    msg_seg = message.split(',')
    log.debug('Extracted msg sequence number: [%s]', msg_seg[0])
    ack_to_send = msg_seg[0].encode()
    log.debug('Sending response msg: [%s]', ack_to_send)
    writer.write(ack_to_send)
    yield from writer.drain()
    log.debug('Closing the socket after sending ACK')
    writer.close()


# Outgoing message handler ****************************************************
@asyncio.coroutine
def handle_msg_out():
    """ task to handle outgoing messages """
    while True:
        if msg_out_que.qsize() > 0:
            log.debug('Pulling next outgoing message from queue')
            msg_to_send = msg_out_que.get_nowait()
            log.debug('Extracting msg destination address and port')
            msg_seg_out = msg_to_send.split(',')
            log.debug('Opening outgoing connection to %s:%s',
                msg_seg_out[1], msg_seg_out[2])
            try:
                reader_out, writer_out = yield from asyncio.open_connection(
                    msg_seg_out[1], int(msg_seg_out[2]), loop=loop)
                log.debug('Sending message: [%s]', msg_to_send)
                writer_out.write(msg_to_send.encode())

                log.debug('Waiting for ack')
                data_ack = yield from reader_out.read(200)
                ack = data_ack.decode()
                log.debug('Received: %r', ack)
                if ack.split(',')[0] == msg_seg_out[0]:
                    log.debug('Successful ACK received')
                else:
                    log.debug('Ack received does not match sent message')
                log.debug('Closing socket')
                writer_out.close()
            except:
                log.warning('Could not open socket connection to target')
        # Yield to other tasks for a while
        yield from asyncio.sleep(0.25)


# Main ************************************************************************
def main():
    """ Main application routine """
    log.debug('Starting main')
    try:
        log.debug('Creating incoming message listening server at [%s:%s]', \
            address, port)
        msg_in_server = asyncio.start_server(
            handle_msg_in, host=address, port=int(port))
        log.debug('Wrapping servier in future task and scheduling for '
                  'execution')
        msg_in_task = loop.run_until_complete(msg_in_server)        
    except:
        log.debug('Failed to create socket listening connection at %s:%s', \
            address, port)
        sys.exit()

    log.debug('Scheduling main task for execution')
    asyncio.ensure_future(
        service.service_main_task(
            msg_in_que, msg_out_que, rNumGen, devices, log,
            address, port, 
            db_add, db_port,
            wemo_add, wemo_port))

    log.debug('Scheduling outgoing message task for execution')
    asyncio.ensure_future(handle_msg_out())

    # Serve requests until Ctrl+C is pressed
    log.info('Automation Service')
    log.info('Serving on {}'.format(msg_in_task.sockets[0].getsockname()))
    log.info('Press CTRL+C to exit')
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        # Close the server
        msg_in_task.close()
        loop.run_until_complete(msg_in_task.wait_closed())
        loop.close()


# Call Main *******************************************************************
if __name__ == "__main__":
    main()