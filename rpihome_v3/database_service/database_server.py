#!/usr/bin/python3
""" database_server.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import copy
if __name__ == "__main__":
    import sys
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


# Socket Server for external comms ********************************************
@asyncio.coroutine
def handle_echo(reader, writer):
    """ Socket opened callback """
    data = yield from reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    log.debug('Received %r from %r' % (message, addr))
    msg_seg = message.split(",")

    # Process database status update requests
    if msg_seg[0] == "001":
        log.debug('Received message is a status update')
        database_service.insert_record(
            database,
            msg_seg[1],
            msg_seg[2],
            msg_seg[3],
            log)
        log.debug('Database updated')

    # Echo response to originating message sender
    log.debug('Sending response: %r' % message)
    writer.write(data)
    yield from writer.drain()

    # Close socket
    log.debug('Closing the socket after response')
    writer.close()


# Send to Wemo Service ********************************************************
@asyncio.coroutine
def send_to_wemo_service(host, port, message):
    """ function to send message to wemo service """
    log.debug('Calling "send_to_wemo_service" function')
    reader, writer = yield from asyncio.open_connection(host, port)
    log.debug('Connected to %s:%d', host, port)
    try:
        writer.write(message.encode())
        log.debug('Sent message: %s', message.encode())
        data = yield from asyncio.wait_for(reader.readline(), timeout=2.0)
        if data is not None:
            log.debug('Received ACK: %s', data.decode())

    except:
        log.warning('Could not connect to wemo service')
    finally:
        writer.close()
        log.debug('Closing send_to_wemo_service writer')


#  *********************************************
@asyncio.coroutine
def main_task():
    """ test """
    log.debug('Calling "database_server_task"')
    while True:
        try:
            yield from send_to_wemo_service(
                '127.0.0.1',
                28000,
                '001,fylt1,192.168.86.21,off,2017-07-13 12:00:00')
            # Wait a pre-determined time period, then re-run the task
            log.debug('Sleeping task for %s seconds', str(sleep))
            yield from asyncio.sleep(sleep)
        except KeyboardInterrupt:
            log.debug('Killing task')
            break      


# Main ************************************************************************
def main():
    log.debug('Starting main')

    loop = asyncio.get_event_loop()
    logic_task = asyncio.ensure_future(main_task())
    server = asyncio.start_server(handle_echo, host=address, port=port, loop=loop)
    server_task = loop.run_until_complete(server)
    

    # Serve requests until Ctrl+C is pressed
    print('Serving on {}'.format(server_task.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server_task.close()
    loop.run_until_complete(server_task.wait_closed())
    loop.close()



# Service *********************************************************************
log = database_service.configure_log('config.ini')
credentials = database_service.configure_credentials('config.ini', log)
database = database_service.configure_database('config.ini', credentials, log)
address, port = database_service.configure_server('config.ini', log)
devices = []
sleep = 5.0

main()
