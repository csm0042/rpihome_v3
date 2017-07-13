#!/usr/bin/python3
""" database_server.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
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
    data = yield from reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print('Received %r from %r' % (message, addr))

    print('Send: %r' % message)
    writer.write(data)
    yield from writer.drain()

    print('Close the client socket')
    writer.close()


# Service *********************************************************************
logger = database_service.configure_logger('config.ini')
credentials = database_service.configure_credentials('config.ini', logger)
database = database_service.configure_database('config.ini', credentials, logger)
address, port = database_service.configure_server('config.ini', logger)

loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, address, port, loop=loop)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()