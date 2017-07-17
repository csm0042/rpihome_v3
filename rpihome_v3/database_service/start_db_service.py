#!/usr/bin/python3
""" start_db_service.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import copy
import logging
import sys
if __name__ == "__main__":
    sys.path.append("..")
import database_service


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
log = database_service.configure_log('config.ini')
credentials = database_service.configure_credentials('config.ini', log)
database = database_service.configure_database('config.ini', credentials, log)
address, port = database_service.configure_server('config.ini', log)

ref_num_gen = database_service.RefNum()
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
        try:
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
                data_ack = yield from reader_out.read(200)
                ack = data_ack.decode()
                log.debug('Received: %r', ack)
                if ack.split(',')[0] == msg_seg_out[0]:
                    log.debug('Successful ACK received')
                else:
                    log.debug('Ack received does not match sent message')
                log.debug('Closing socket')
                writer_out.close()
            yield from asyncio.sleep(0.25)
        except KeyboardInterrupt:
            log.debug('Killing task')
            break


# Internal Service Work Task **************************************************
@asyncio.coroutine
def service_main():
    """ task to handle the work the service is intended to do """
    while True:
        try:
            if msg_in_que.qsize() > 0:
                log.debug('Extract next message from incoming queue and '
                          'process')
                next_msg = msg_in_que.get_nowait()

                next_msg_seg = next_msg.split(sep=',')
                msgHeader = next_msg_seg[:5]
                msgPayload = next_msg_seg[5:]
                
                # Log Device status updates to database
                if msgPayload[0] == '100':
                    log.debug('Message is a device status update. ' 
                              'Calling update query')
                    response_msg = yield from log_status_update(
                        msgHeader, msgPayload)
                    log.debug('Entering response messages into outgoing '
                              'msg queue')                    
                    try:
                        msg_out_que.put_nowait(response_msg)
                        log.debug('Response message [%s] successfully queued',
                        response_msg)
                    except:
                        log.debug('Response message [%s] was not successfully '
                                  'queued', response_msg)                    
                
                # Device command not yet processed query
                if msgPayload[0] == '102':
                    log.debug('Msg is a device pending cmd query.  '
                              'Calling query')
                    response_msg_list = yield from read_device_cmd(
                        msgHeader, msgPayload)
                    log.debug('Entering response messages into outgoing '
                              'msg queue')
                    for response_msg in response_msg_list:
                        try:
                            msg_out_que.put_nowait(response_msg)
                            log.debug('Response message [%s] successfully queued',
                            response_msg)
                        except:
                            log.debug('Response message [%s] was not successfully '
                                      'queued', response_msg)
                
                # Device command sent timestamp updates
                if msgPayload[0] == '104':
                    log.debug('Msg is a device pending cmd complete update.  '
                              'Calling query')                    
                    response_msg = yield from update_device_cmd(
                        msgHeader, msgPayload)     
                    log.debug('Entering response messages into outgoing '
                              'msg queue')                    
                    try:
                        msg_out_que.put_nowait(response_msg)
                        log.debug('Response message [%s] successfully queued',
                        response_msg)
                    except:
                        log.debug('Response message [%s] was not successfully '
                                  'queued', response_msg)                                                       

            yield from asyncio.sleep(0.25)
        except KeyboardInterrupt:
            log.debug('Killing task')
            break


# Internal Service Work Subtask - wemo get status *****************************
@asyncio.coroutine
def log_status_update(msgH, msgP):
    """ Function to insert status updates into device_log table 
    Msg Header format: 
    aaa,bbb.bbb.bbb.bbb.bbb,ccccc,ddd.ddd.ddd.ddd.eeeee
    where
    aaa = ref number
    bbb.bbb.bbb.bbb = destination IP address for message
    ccccc = destination port for message
    ddd.ddd.ddd.ddd = IP where message originated
    eeeee = port where message originated

    Msg Payload format:
    aaa,bbbb,ccc.ccc.ccc.ccc,dddd,eeee
    aaa = msg type (100 for status update, 101 for status update ACK)
    bbbb = device name
    ccc.ccc.ccc.ccc = device address
    dddd = device status to log
    eeee = timestamp associated with device status change
    """
    # Map message header to usable tags
    msgRef = msgH[0]
    msgDestAdd = msgH[1]
    msgDestPort = msgH[2]
    msgSourceAdd = msgH[3]
    msgSourcePort = msgH[4]
    # Map message payload to usable tags
    msgType = msgP[0]
    devName = msgP[1]
    devAdd = msgP[2]
    devStatus = msgP[3]
    devLastSeen = msgP[4]
    # Execute Insert Query
    log.debug('Logging status change to database for [%s].  New '
              'status is [%s] with a last seen time of [%s]',
              devName, devStatus, devLastSeen)
    database_service.insert_record(database, devName,
                                   devStatus, devLastSeen, log)
    # Send response indicating query was executed
    log.debug('Generating new ref number for response message')
    ref_num = ref_num_gen.new()
    log.debug('Building response message header')
    response_header = ref_num + ',' + msgSourceAdd + ',' + \
                      msgSourcePort + ',' + msgDestAdd + ',' + \
                      msgDestPort
    log.debug('Resulting header: [%s]', response_header)
    log.debug('Building response message payload')
    response_payload = '101,' + devName
    log.debug('Resulting payload: [%s]', response_payload)
    log.debug('Building complete response message')                    
    response_msg = response_header + ',' + response_payload
    log.debug('Complete response message: [%s]', response_msg)
    # Return response message
    return response_msg


# Internal Service Work Subtask - wemo turn on ********************************
@asyncio.coroutine
def read_device_cmd(msgH, msgP):
    """ Function to query database for any un-processed device commands 
    Msg Header format: 
    aaa,bbb.bbb.bbb.bbb.bbb,ccccc,ddd.ddd.ddd.ddd.eeeee
    where
    aaa = ref number
    bbb.bbb.bbb.bbb = destination IP address for message
    ccccc = destination port for message
    ddd.ddd.ddd.ddd = IP where message originated
    eeeee = port where message originated

    Msg Payload format:
    aaa
    aaa = msg type (102 for cmd query, 103 for cmd query ACK)
    """
    # Map message header to usable tags
    msgRef = msgH[0]
    msgDestAdd = msgH[1]
    msgDestPort = msgH[2]
    msgSourceAdd = msgH[3]
    msgSourcePort = msgH[4]
    # Execute select Query
    log.debug('Querying database for pending device commands')
    pending_cmd_list = database_service.query_command(database, log)
    # Send response message for each record returned by query
    response_msg_list = []
    if len(pending_cmd_list) <= 0:
        log.debug('No pending commands found')
    else:
        log.debug('Preparing response messages for pending commands')
        for pending_cmd in pending_cmd_list:
            log.debug('Generating new ref number for response message')
            ref_num = ref_num_gen.new()
            log.debug('Building response message header')
            response_header = ref_num + ',' + msgSourceAdd + ',' + \
                              msgSourcePort + ',' + msgDestAdd + ',' + \
                              msgDestPort
            log.debug('Resulting header: [%s]', response_header)
            log.debug('Building response message payload')
            response_payload = '103,' + pending_cmd
            log.debug('Resulting payload: [%s]', response_payload)
            log.debug('Building complete response message')                    
            response_msg = response_header + ',' + response_payload
            response_msg_list.append(copy.copy(response_msg))
            log.debug('Complete response message: [%s]', response_msg)
    # Return list of response messages from query
    return response_msg_list


# Internal Service Work Subtask - wemo turn off *******************************
@asyncio.coroutine
def update_device_cmd(msgH, msgP):
    """ Function to set state of wemo device to "off"
    Msg Header format: 
    aaa,bbb.bbb.bbb.bbb.bbb,ccccc,ddd.ddd.ddd.ddd.eeeee
    where
    aaa = ref number
    bbb.bbb.bbb.bbb = destination IP address for message
    ccccc = destination port for message
    ddd.ddd.ddd.ddd = IP where message originated
    eeeee = port where message originated

    Msg Payload format:
    aaa,bbbb,cccc
    aaa = msg type (104 for cmd update, 105 for cmd update ACK)
    bbbb = record ID
    cccc = processed timestamp
    """
    # Map message header to usable tags
    msgRef = msgH[0]
    msgDestAdd = msgH[1]
    msgDestPort = msgH[2]
    msgSourceAdd = msgH[3]
    msgSourcePort = msgH[4]
    # Map message payload to usable tags
    msgType = msgP[0]
    cmdId = msgP[1]
    cmdProcessed = msgP[2]
    # Execute update Query
    log.debug('Querying database to mark command with ID [%s] as complete with timestamp [%s]', cmdId, cmdProcessed)
    database_service.update_command(database, cmdId, cmdProcessed, log)
    # Send response indicating query was executed
    log.debug('Generating new ref number for response message')
    ref_num = ref_num_gen.new()
    log.debug('Building response message header')
    response_header = ref_num + ',' + msgSourceAdd + ',' + \
                      msgSourcePort + ',' + msgDestAdd + ',' + \
                      msgDestPort
    log.debug('Resulting header: [%s]', response_header)
    log.debug('Building response message payload')
    response_payload = '105,' + cmdId
    log.debug('Resulting payload: [%s]', response_payload)
    log.debug('Building complete response message')                    
    response_msg = response_header + ',' + response_payload
    log.debug('Complete response message: [%s]', response_msg)
    # Return response message
    return response_msg



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
    log.info('Database Persistance Service')
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
