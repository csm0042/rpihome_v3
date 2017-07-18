#!/usr/bin/python3
""" service_manager.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import copy
import logging
import sys
if __name__ == "__main__":
    sys.path.append("..")
import helpers
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
log = wemo_service.configure_log('config.ini')
address, port = wemo_service.configure_server('config.ini', log)

rNumGen = helpers.RefNum()
wemoGw = wemo_service.WemoAPI(log)

msg_in_que = asyncio.Queue()
msg_out_que = asyncio.Queue()
loop = asyncio.get_event_loop()




# Incoming message handler ****************************************************
@asyncio.coroutine
def handle_msg_in(reader, writer):
    """ Callback used to send ACK messages back to acknowledge messages 
    received """
    log.debug('Yielding to reader.read()')
    data_in = yield from reader.read(100)
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



# Internal Service Work Task **************************************************
@asyncio.coroutine
def service_main():
    """ task to handle the work the service is intended to do """
    while True:
        if msg_in_que.qsize() > 0:
            log.debug('Getting Incoming message from queue')
            next_msg = msg_in_que.get_nowait()
            log.debug('Splitting message into header / payload')
            next_msg_seg = next_msg.split(sep=',')
            msgHeader = next_msg_seg[:5]
            msgPayload = next_msg_seg[5:]
            
            # Wemo Device Status Queries
            if msgPayload[0] == '100':
                log.debug('Message is a device status update request')                
                response_msg_list = yield from wemo_service.get_wemo_status(
                    rNumGen, wemoGw, log, msgHeader, msgPayload)
                log.debug('Queueing response message(s)')
                for response_msg in response_msg_list:
                    msg_out_que.put_nowait(response_msg)
                    log.debug('Response message [%s] successfully queued',
                                response_msg)
            # Wemo Device on commands
            if msgPayload[0] == '102':
                log.debug('Message is a device set "on" command')
                response_msg = yield from wemo_service.set_wemo_on(
                    rNumGen, wemoGw, log, msgHeader, msgPayload)
                log.debug('Queueing response message(s)')
                for response_msg in response_msg_list:
                    msg_out_que.put_nowait(response_msg)
                    log.debug('Response message [%s] successfully queued',
                                response_msg)
            # Wemo Device off commands
            if msgPayload[0] == '104':
                log.debug('Message is a device set "off" command')
                response_msg = yield from wemo_service.set_wemo_off(
                    rNumGen, wemoGw, log, msgHeader, msgPayload)
                log.debug('Queueing response message(s)')
                for response_msg in response_msg_list:
                    msg_out_que.put_nowait(response_msg)
                    log.debug('Response message [%s] successfully queued',
                                response_msg)                                      
        # Yield to other tasks for a while
        yield from asyncio.sleep(0.25)


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
            reader_out, writer_out = yield from asyncio.open_connection(
                msg_seg_out[1], int(msg_seg_out[2]), loop=loop)
            log.debug('Sending message: [%s]', msg_to_send)
            writer_out.write(msg_to_send.encode())

            log.debug('Waiting for ack')
            data_ack = yield from reader_out.read(100)
            ack = data_ack.decode()
            log.debug('Received: %r', ack)
            if ack.split(',')[0] == msg_seg_out[0]:
                log.debug('Successful ACK received')
            else:
                log.debug('Ack received does not match sent message')
            log.debug('Closing socket')
            writer_out.close()
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
    asyncio.ensure_future(service_main())

    log.debug('Scheduling outgoing message task for execution')
    asyncio.ensure_future(handle_msg_out())

    # Serve requests until Ctrl+C is pressed
    log.info('Wemo Gateway Service')
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
