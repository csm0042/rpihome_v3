#!/usr/bin/python3
""" service_manager.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import logging
import sys
if __name__ == "__main__":
    sys.path.append("..")
import wemo_service


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
logger = wemo_service.configure_log('config.ini')
address, port = wemo_service.configure_server('config.ini', logger)
wemo_gw = wemo_service.WemoAPI(logger)
msg_in_que = asyncio.Queue()
msg_out_que = asyncio.Queue()
loop = asyncio.get_event_loop()

test_msg = '042,127.0.0.1,27001,payload'
msg_out_que.put_nowait(test_msg)


# Message in and out routines *************************************************
@asyncio.coroutine
def handle_msg_in(reader, writer):
    """ Callback used to send ACK messages back to acknowledge messages 
    received """
    logger.debug('Yielding to reader.read()')
    data_in = yield from reader.read(100)
    logger.debug('Decoding read data')
    message = data_in.decode()
    logger.debug('Extracting address from socket connection')
    addr = writer.get_extra_info('peername')
    logger.debug('Received %r from %r' % (message, addr))

    # Coping incoming message to message buffer
    logger.debug('Loading message into incoming msg buffer')
    msg_in_que.put_nowait(message)
    logger.debug('Resulting buffer length: %s', str(msg_in_que.qsize()))

    # Acknowledge receipt of message
    logger.debug("ACK'ing message: %r", message)
    logger.debug('Splitting message into constituent parts')
    msg_seg = message.split(',')
    logger.debug('Extracted msg sequence number: [%s]', msg_seg[0])
    ack_to_send = msg_seg[0].encode()
    logger.debug('Sending response msg: [%s]', ack_to_send)
    writer.write(ack_to_send)
    yield from writer.drain()
    logger.debug('Closing the socket after sending ACK')
    writer.close()


@asyncio.coroutine
def handle_msg_out():
    """ task to handle outgoing messages """
    while True:
        try:
            if msg_out_que.qsize() > 0:
                logger.debug('Pulling next outgoing message from queue')
                msg_to_send = msg_out_que.get_nowait()
                logger.debug('Extracting msg destination address and port')
                msg_seg_out = msg_to_send.split(',')
                logger.debug(
                    'Opening outgoing connection to %s:%s',
                    msg_seg_out[1], msg_seg_out[2])
                reader_out, writer_out = yield from asyncio.open_connection(
                    msg_seg_out[1], int(msg_seg_out[2]), loop=loop)
                logger.debug('Sending message: [%s]', msg_to_send)
                writer_out.write(msg_to_send.encode())

                logger.debug('Waiting for ack')
                data_ack = yield from reader_out.read(100)
                ack = data_ack.decode()
                logger.debug('Received: %r', ack)
                if ack.split(',')[0] == msg_seg_out[0]:
                    logger.debug('Successful ACK received')
                else:
                    logger.debug('Ack received does not match sent message')
                logger.debug('Closing socket')
                writer_out.close()
            yield from asyncio.sleep(0.25)
        except KeyboardInterrupt:
            logger.debug('Killing task')
            break


# Service Routine *************************************************************
@asyncio.coroutine
def service_main():
    """ task to handle the work the service is intended to do """
    while True:
        try:
            if msg_in_que.qsize() > 0:
                logger.debug('Extract next message from incoming queue and process')
                next_msg = msg_in_que.get_nowait()

                
                logger.debug('Move outgoing message [%s] to outgoing msg queue',msg_to_send)
                msg_out_que.put_nowait(msg_to_send)
            yield from asyncio.sleep(0.25)
        except KeyboardInterrupt:
            logger.debug('Killing task')
            break


# Main ************************************************************************
def main():
    """ Main application routine """
    logger.debug('Starting main')

    logger.debug('Creating incoming message listening server at [%s:%s]', address, port)
    msg_in_server = asyncio.start_server(handle_msg_in, host=address, port=int(port))

    logger.debug('Wrapping servier in future task and scheduling for execution')
    msg_in_task = loop.run_until_complete(msg_in_server)

    logger.debug('Scheduling main task for execution')
    main_task = asyncio.ensure_future(service_main())

    logger.debug('Scheduling outgoing message task for execution')
    msg_out_task = asyncio.ensure_future(handle_msg_out())

    # Serve requests until Ctrl+C is pressed
    print('Wemo Gateway Service')
    print('Serving on {}'.format(msg_in_task.sockets[0].getsockname()))
    print('Press CTRL+C to exit')
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        # Close the server
        msg_in_task.close()
        main_task.close()
        msg_out_task.close()
        loop.run_until_complete(msg_in_task.wait_closed())
        loop.close()


# Call Main *******************************************************************
if __name__ == "__main__":
    main()
