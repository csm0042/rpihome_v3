#!/usr/bin/python3
""" test_device.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import configparser
import copy
import datetime
import logging
import sys
import unittest
if __name__ == "__main__":
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from rpihome_v3.helpers.ref_num import RefNum
from rpihome_v3.automation_service.configure import ConfigureService
from rpihome_v3.automation_service.msg_processing_db import process_log_status_update_msg
from rpihome_v3.automation_service.msg_processing_db import process_log_status_update_msg_ack
from rpihome_v3.automation_service.msg_processing_db import process_return_command_msg
from rpihome_v3.automation_service.msg_processing_db import process_return_command_msg_ack
from rpihome_v3.automation_service.msg_processing_db import process_update_command_msg
from rpihome_v3.automation_service.msg_processing_db import process_update_command_msg_ack


# Define test class ***********************************************************
class Test_message_processing_db(unittest.TestCase):
    """ unittests for Device Class, methods, and functions """

    def __init__(self, *args, **kwargs):
        # Configure logging
        logging.basicConfig(stream=sys.stdout)
        self.log = logging.getLogger(__name__)
        self.log.level = logging.DEBUG
        # Create tags for testing
        self.msg_in = str()
        self.msg_out = []
        self.ref_num = RefNum(self.log)
        self.ref_num_initial = int()
        self.temp_dt = datetime.datetime
        # Create items that will come from config file
        if __name__ == "__main__":
            self.config = ConfigureService('config.ini')
        else:
            self.config = ConfigureService('tests/test_automation_service/config.ini')
        self.service_addresses = self.config.get_servers()
        self.message_types = self.config.get_message_types()
        self.devices = self.config.get_devices()
        # Call parent class init
        super(Test_message_processing_db, self).__init__(*args, **kwargs)


    def setUp(self):
        # call parent class setup
        super(Test_message_processing_db, self).setUp()


    def test_init(self):
        """ test class __init__ and input variables """
        pass


    def test_process_log_status_update_msg(self):
        """ test correct outputs result from various inputs """
        self.msg_in = '101,127.2.2.1,27001,127.3.3.1,27002,102,device,192.168.86.1,on,2017-01-01 10:02:03'
        self.msg_out = process_log_status_update_msg(
            self.log,
            self.msg_in,
            self.service_addresses)
        # check output
        self.assertEqual(len(self.msg_out), 1)
        self.msg_out_split = self.msg_out[0].split(",")
        self.assertEqual(self.msg_out_split[0], '101')
        self.assertEqual(self.msg_out_split[1], '127.0.0.1')
        self.assertEqual(self.msg_out_split[2], '27011')
        self.assertEqual(self.msg_out_split[3], '127.3.3.1')
        self.assertEqual(self.msg_out_split[4], '27002')
        self.assertEqual(self.msg_out_split[5], '102')
        self.assertEqual(self.msg_out_split[6], 'device')
        self.assertEqual(self.msg_out_split[7], '192.168.86.1')
        self.assertEqual(self.msg_out_split[8], 'on')
        self.assertEqual(self.msg_out_split[9], '2017-01-01 10:02:03')


    def test_process_log_status_update_msg_ack(self):
        """ test correct outputs result from various inputs """
        self.msg_in = '101,127.2.2.1,27001,127.3.3.1,27002,102,device,192.168.86.1,on,2017-01-01 10:02:03'
        process_log_status_update_msg_ack(
            self.log,
            self.msg_in)
        # check output
        self.assertEqual(len(self.msg_out), 0)


    def test_process_return_command_msg(self):
        """ test correct outputs result from various inputs """
        self.msg_in = '101,127.2.2.1,27001,127.3.3.1,27002,104,device'
        self.msg_out = process_return_command_msg(
            self.log,
            self.msg_in,
            self.service_addresses)
        # check output
        self.assertEqual(len(self.msg_out), 1)
        self.msg_out_split = self.msg_out[0].split(",")
        self.assertEqual(self.msg_out_split[0], '101')
        self.assertEqual(self.msg_out_split[1], '127.0.0.1')
        self.assertEqual(self.msg_out_split[2], '27011')
        self.assertEqual(self.msg_out_split[3], '127.3.3.1')
        self.assertEqual(self.msg_out_split[4], '27002')
        self.assertEqual(self.msg_out_split[5], '104')
        self.assertEqual(self.msg_out_split[6], 'device')


    def test_return_command_msg_ack(self):
        """ test correct outputs result from various inputs """
        self.msg_in = '101,127.2.2.1,27001,127.3.3.1,27002,105,42,fylt2,on,2017-08-05 10:12:11,,'
        self.ref_num_initial = int(self.ref_num.source)
        self.msg_out = process_return_command_msg_ack(
            self.log,
            self.ref_num,
            self.devices,
            self.msg_in,
            self.service_addresses,
            self.message_types)
        # check output
        self.assertEqual(len(self.msg_out), 2)
        # First item in list should be an update command message
        self.msg_out_split = self.msg_out[0].split(",")
        self.assertEqual(self.msg_out_split[0], str(self.ref_num_initial + 1))
        self.assertEqual(self.msg_out_split[1], '127.0.0.1')
        self.assertEqual(self.msg_out_split[2], '27011')
        self.assertEqual(self.msg_out_split[3], '127.0.0.1')
        self.assertEqual(self.msg_out_split[4], '27001')
        self.assertEqual(self.msg_out_split[5], '106')
        self.assertEqual(self.msg_out_split[6], '42')
        self.assertEqual(
            self.msg_out_split[7][0:4],
            str(datetime.datetime.now().date())[0:4]
        )
        self.assertEqual(
            self.msg_out_split[7][5:7],
            str(datetime.datetime.now().date())[5:7]
        )
        self.assertEqual(
            self.msg_out_split[7][8:10],
            str(datetime.datetime.now().date())[8:10]
        )
        self.assertEqual(
            self.msg_out_split[7][11:13],
            str(datetime.datetime.now().time())[0:2]
        )
        self.assertEqual(
            self.msg_out_split[7][14:16],
            str(datetime.datetime.now().time())[3:5]
        )
        # Second item in list should be set device state message
        self.msg_out_split = self.msg_out[1].split(",")
        self.assertEqual(self.msg_out_split[0], str(self.ref_num_initial + 2))
        self.assertEqual(self.msg_out_split[1], '127.0.0.1')
        self.assertEqual(self.msg_out_split[2], '27061')
        self.assertEqual(self.msg_out_split[3], '127.0.0.1')
        self.assertEqual(self.msg_out_split[4], '27001')
        self.assertEqual(self.msg_out_split[5], '604')
        self.assertEqual(self.msg_out_split[6], 'fylt2')
        self.assertEqual(self.msg_out_split[7], '192.168.86.34')
        self.assertEqual(self.msg_out_split[8], 'on')
        self.assertEqual(self.msg_out_split[9], '')
        self.assertEqual(
            self.msg_out_split[10][0:4],
            str(datetime.datetime.now().date())[0:4]
        )
        self.assertEqual(
            self.msg_out_split[10][5:7],
            str(datetime.datetime.now().date())[5:7]
        )
        self.assertEqual(
            self.msg_out_split[10][8:10],
            str(datetime.datetime.now().date())[8:10]
        )
        self.assertEqual(
            self.msg_out_split[10][11:13],
            str(datetime.datetime.now().time())[0:2]
        )
        self.assertEqual(
            self.msg_out_split[10][14:16],
            str(datetime.datetime.now().time())[3:5]
        )


    def test_process_update_command_msg(self):
        """ test correct outputs result from various inputs """
        self.msg_in = '101,127.2.2.1,27001,127.3.3.1,27002,106,42,2017-08-05 10:12:11'
        self.ref_num_initial = int(self.ref_num.source)
        self.msg_out = process_update_command_msg(
            self.log,
            self.msg_in,
            self.service_addresses
        )
        # check output
        self.assertEqual(len(self.msg_out), 1)
        self.msg_out_split = self.msg_out[0].split(",")
        self.assertEqual(self.msg_out_split[0], '101')
        self.assertEqual(self.msg_out_split[1], '127.0.0.1')
        self.assertEqual(self.msg_out_split[2], '27011')
        self.assertEqual(self.msg_out_split[3], '127.3.3.1')
        self.assertEqual(self.msg_out_split[4], '27002')
        self.assertEqual(self.msg_out_split[5], '106')
        self.assertEqual(self.msg_out_split[6], '42')
        self.assertEqual(self.msg_out_split[7], '2017-08-05 10:12:11')


    def test_process_update_command_msg_ack(self):
        """ test correct outputs result from various inputs """
        self.msg_in = '101,127.2.2.1,27001,127.3.3.1,27002,106,42,2017-08-05 10:12:11'
        self.ref_num_initial = int(self.ref_num.source)
        self.msg_out = process_update_command_msg_ack(
            self.log,
            self.msg_in
        )
        # check output
        self.assertEqual(len(self.msg_out), 0)


if __name__ == "__main__":
    unittest.main()
