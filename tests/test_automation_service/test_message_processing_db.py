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
        logging.basicConfig(stream=sys.stdout)
        self.log = logging.getLogger(__name__)
        self.log.level = logging.DEBUG
        self.msg_in = str()
        self.msg_out = []
        # Create items that will come from config file
        self.config_file = configparser.ConfigParser()
        self.service_addresses = {}
        # Call parent class init
        super(Test_message_processing_db, self).__init__(*args, **kwargs)


    def setUp(self):
        self.msg_out = []
        self.service_addresses = {}
        self.config_file.read('tests/test_automation_service/config.ini')
        for option in self.config_file.options('SERVICES'):
            self.service_addresses[option] = self.config_file['SERVICES'][option]
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
               




if __name__ == "__main__":
    unittest.main()
