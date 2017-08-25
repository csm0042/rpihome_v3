#!/usr/bin/python3
""" start_service.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
from contextlib import suppress
import sys
import time
import env
from rpihome_v3.helpers.ref_num import RefNum
from rpihome_v3.helpers.message_handlers import MessageHandler
from rpihome_v3.schedule_service.configure import configure_log
from rpihome_v3.schedule_service.configure import configure_servers
from rpihome_v3.schedule_service.configure import configure_message_types
from rpihome_v3.schedule_service.configure import configure_credentials
from rpihome_v3.schedule_service.configure import configure_schedule
from rpihome_v3.schedule_service.service_main import service_main_task


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
CREDENTIALS = configure_credentials('config.ini', LOG)
SCHEDULE = configure_schedule('config.ini', CREDENTIALS, LOG)

REF_NUM = RefNum(log=LOG)
MSG_IN_QUEUE = asyncio.Queue()
MSG_OUT_QUEUE = asyncio.Queue()
LOOP = asyncio.get_event_loop()

COMM_HANDLER = MessageHandler(LOG)


# Main ************************************************************************
def main():
    """ Main application routine """
    LOG.debug('Starting main')

    # Create incoming message server
    try:
        LOG.debug('Creating incoming message listening server at [%s:%s]',
                  SERVICE_ADDRESSES['schedule_addr'],
                  SERVICE_ADDRESSES['schedule_port'])
        msg_in_server = asyncio.start_server(
            COMM_HANDLER.handle_msg_in,
            host=SERVICE_ADDRESSES['schedule_addr'],
            port=int(SERVICE_ADDRESSES['schedule_port']))
        LOG.debug('Wrapping servier in future task and scheduling for '
                  'execution')
        msg_in_task = LOOP.run_until_complete(msg_in_server)        
    except Exception:
        LOG.debug('Failed to create socket listening connection at %s:%s',
                  SERVICE_ADDRESSES['schedule_addr'],
                  SERVICE_ADDRESSES['schedule_port'])
        sys.exit()
    
    # Create main task for this service
    LOG.debug('Scheduling main task for execution')
    asyncio.ensure_future(
        service_main_task(
            LOG,
            REF_NUM,
            SCHEDULE,
            MSG_IN_QUEUE,
            MSG_OUT_QUEUE,
            MESSAGE_TYPES))

    # Create outgoing message task
    LOG.debug('Scheduling outgoing message task for execution')
    asyncio.ensure_future(COMM_HANDLER.handle_msg_out())

    # Serve requests until Ctrl+C is pressed
    LOG.info('Schedule Service')
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
