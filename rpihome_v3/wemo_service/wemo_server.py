#!/usr/bin/python3
""" wemo_server.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
if __name__ == "__main__":
    import sys
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


# Socket Server for external comms ********************************************
@asyncio.coroutine
def handle_echo(reader, writer):
    data = yield from reader.read()
    message = data.decode()
    addr = writer.get_extra_info('peername')
    log.debug('Received %r from %r' % (message, addr))

    # Acknowledge receipt of message
    log.debug("ACK'ing message: %r", message)
    writer.write(data)
    yield from writer.drain()

    log.debug('Closing the socket after response')
    writer.close()
    
    # Break up message for decoding purposes
    msg_seg = message.split(",")

    # Process device status requests
    if msg_seg[0] == "001":
        log.debug('Received message is a status request')
        status, last_seen = wemo_gw.read_status(msg_seg[1], msg_seg[2], msg_seg[3], msg_seg[4])
        log.debug('Updated status: %s/%s', status, last_seen)
        reply_msg = msg_seg[0] + ',' + msg_seg[1] + ',' + status + ',' + last_seen
        log.debug('Sending response message: %s', reply_msg)



# Main ************************************************************************
def main():
    log.debug('Starting main')

    loop = asyncio.get_event_loop()
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
log = wemo_service.configure_log('config.ini')
address, port = wemo_service.configure_server('config.ini', log)
wemo_gw = wemo_service.WemoAPI(log)

main()
