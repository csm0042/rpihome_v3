#!/usr/bin/python3
""" test_msg_processing_schedule.py:
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
from rpihome_v3.automation_service.msg_processing_schedule import create_get_device_scheduled_state_msg
from rpihome_v3.automation_service.msg_processing_schedule import process_get_device_scheduled_state_msg
from rpihome_v3.automation_service.msg_processing_schedule import process_get_device_scheduled_state_msg_ack


# Define test class ***********************************************************
class Test_message_processing_schedule(unittest.TestCase):
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
        self.last_ref_num = int()
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
        super(Test_message_processing_schedule, self).__init__(*args, **kwargs)


    def setUp(self):
        # call parent class setup
        super(Test_message_processing_schedule, self).setUp()


    def test_init(self):
        """ test class __init__ and input variables """
        pass


    def test_create_get_device_scheduled_state_msg(self):
        """ test correct outputs result from various inputs """
        self.last_ref_num = int(self.ref_num.source)
        # call function
        self.msg_out = create_get_device_scheduled_state_msg(
            self.log,
            self.ref_num,
            self.devices,
            self.service_addresses,
            self.message_types)
        
        # check for proper number of outgoing messages generated
        self.count = 0
        for d in self.devices:
            if d.dev_rule == "schedule" or d.dev_rule == "dusk_to_dawn" or d.dev_rule == "":
                self.count += 1
        self.assertEqual(len(self.msg_out), self.count)

        # Check message contents
        for i, j in enumerate(self.msg_out):
            self.msg_out_split = j.split(",")
            # check message addresses and ports
            self.assertNotEqual(self.msg_out_split[0], str(self.last_ref_num))
            self.last_ref_num = int(self.msg_out_split[0])
            self.assertEqual(self.msg_out_split[1], '127.0.0.1')
            self.assertEqual(self.msg_out_split[2], '27051')
            self.assertEqual(self.msg_out_split[3], '127.0.0.1')
            self.assertEqual(self.msg_out_split[4], '27001')
            # check message type number
            self.assertEqual(self.msg_out_split[5], '302')
            # check device name field
            self.ptr = 0
            for p, d in enumerate(self.devices):
                if self.msg_out_split[6] == d.dev_name:
                    self.assertEqual(self.msg_out_split[6], d.dev_name)
                    self.devices[p].dev_name = ""
        # Check that only remaining devices left in device list
        # are NOT the ones we are looking for
        self.count = 0
        for d in self.devices:
            if (d.dev_rule == "schedule" or d.dev_rule == "dusk_to_dawn" or d.dev_rule == "") and d.dev_name != "":
                self.count += 1
        self.assertEqual(self.count, 0)


    def test_process_get_device_scheduled_state_msg(self):
        """ test correct outputs result from various inputs """
        self.msg_in = "142,127.3.3.1,8900,127.0.0.1,27031,302,fylt1"
        # call function
        self.msg_out = process_get_device_scheduled_state_msg(
            self.log,
            self.msg_in,
            self.service_addresses)

        # check for proper number of outgoing messages generated
        self.assertEqual(len(self.msg_out), 1)
        # Check message contents
        self.msg_out_split = self.msg_out[0].split(",")
        self.assertEqual(self.msg_out_split[1], '127.0.0.1')
        self.assertEqual(self.msg_out_split[2], '27051')
        self.assertEqual(self.msg_out_split[3], '127.0.0.1')
        self.assertEqual(self.msg_out_split[4], '27031')
        self.assertEqual(self.msg_out_split[5], '302')
        self.assertEqual(self.msg_out_split[6], 'fylt1')


    def test_process_get_device_scheduled_state_msg_ack(self):
        """ test correct outputs result from various inputs """
        self.cmd_list = ['on', 'off']
        for cmd in self.cmd_list:
            self.msg_in = "143,127.0.0.1,27001,127.0.0.1,27051,303,fylt2," + cmd
            # call function
            self.msg_out = process_get_device_scheduled_state_msg_ack(
                self.log,
                self.ref_num,
                self.devices,
                self.msg_in,
                self.service_addresses,
                self.message_types)
            # check for proper number of outgoing messages generated
            self.assertEqual(len(self.msg_out), 1)
            # find device in device list
            for i, d in enumerate(self.devices):
                if d.dev_name == "fylt2":
                    self.ptr = i
                    break
            # Check message contents
            self.msg_out_split = self.msg_out[0].split(",")
            self.assertEqual(self.msg_out_split[1], self.service_addresses['wemo_addr'])
            self.assertEqual(self.msg_out_split[2], self.service_addresses['wemo_port'])
            self.assertEqual(self.msg_out_split[3], '127.0.0.1')
            self.assertEqual(self.msg_out_split[4], '27051')
            self.assertEqual(self.msg_out_split[5], self.message_types['set_device_state'])
            self.assertEqual(self.msg_out_split[6], 'fylt2')
            self.assertEqual(self.msg_out_split[7], self.devices[self.ptr].dev_addr)
            self.assertEqual(self.msg_out_split[8], cmd)
            self.assertEqual(self.msg_out_split[9], self.devices[self.ptr].dev_status)
            self.assertEqual(self.msg_out_split[10], self.devices[self.ptr].dev_last_seen)





if __name__ == "__main__":
    unittest.main()
