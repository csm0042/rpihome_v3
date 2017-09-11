#!/usr/bin/python3
""" test_msg_processing_wemo.py:
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
from rpihome_v3.automation_service.msg_processing_wemo import process_get_device_state_msg
from rpihome_v3.automation_service.msg_processing_wemo import process_get_device_state_msg_ack
from rpihome_v3.automation_service.msg_processing_wemo import process_set_device_state_msg
from rpihome_v3.automation_service.msg_processing_wemo import process_set_device_state_msg_ack


# Define test class ***********************************************************
class Test_message_processing_wemo(unittest.TestCase):
    """ unittests for Device Class, methods, and functions """

    def __init__(self, *args, **kwargs):
        super(Test_message_processing_wemo, self).__init__(*args, **kwargs)
        
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


    def setUp(self):
        super(Test_message_processing_wemo, self).setUp()


    def test_init(self):
        pass


    def test_process_get_device_state_msg(self):
        # Set up fake incoming message to test with
        self.msg_in = "142,127.0.2.1,22222,127.0.0.1,27001,602,fylt1,192.168.86.12,on,2017-07-01 12:11:12"
        # call function
        self.msg_out = process_get_device_state_msg(
            self.log,
            self.msg_in,
            self.service_addresses)

        # check for proper number of outgoing messages generated
        self.assertEqual(len(self.msg_out), 1)
        # Check message contents
        self.msg_out_split = self.msg_out[0].split(",")
        self.assertEqual(self.msg_out_split[0], "142")
        self.assertEqual(self.msg_out_split[1], '127.0.0.1')
        self.assertEqual(self.msg_out_split[2], '27061')
        self.assertEqual(self.msg_out_split[3], '127.0.0.1')
        self.assertEqual(self.msg_out_split[4], '27001')
        self.assertEqual(self.msg_out_split[5], '602')
        self.assertEqual(self.msg_out_split[6], 'fylt1')
        self.assertEqual(self.msg_out_split[7], '192.168.86.12')
        self.assertEqual(self.msg_out_split[8], 'on')
        self.assertEqual(self.msg_out_split[9], '2017-07-01 12:11:12')


    def test_process_get_device_state_msg_ack(self):
        # Capture initial values for comparison
        for i, d in enumerate(self.devices):
            if d.dev_type == "wemo_switch":
                self.org_status = copy.copy(d.dev_status)
                self.org_ts = copy.copy(d.dev_last_seen)
                # Set up fake incoming message to test with
                self.ts = str(datetime.datetime.now())[:19]
                self.rn = self.ref_num.new()
                self.msg_in = self.rn + ",127.0.0.1,27061,127.0.0.1,27001,603," \
                              + d.dev_name + ",on," \
                              + self.ts
                # call function
                self.msg_out = process_get_device_state_msg_ack(
                    self.log,
                    self.devices,
                    self.msg_in)

                # check for proper number of outgoing messages generated
                self.assertEqual(len(self.msg_out), 0)

                # find item in device list it matches
                for p, q in enumerate(self.devices):
                    if q.dev_name == d.dev_name:
                        self.ptr = p
                        break
                self.assertEqual(self.devices[self.ptr].dev_name, d.dev_name)
                self.assertEqual(self.devices[self.ptr].dev_status, "on")
                self.assertEqual(self.devices[self.ptr].dev_last_seen, self.ts)


    def test_process_set_device_state_msg(self):
        # Set up fake incoming message to test with
        for i, d in enumerate(self.devices):
            self.rn = self.ref_num.new()
            self.ts = str(datetime.datetime.now())[:19]
            self.msg_in = self.rn \
                          + ",127.0.2.1,22222,127.0.0.1,27001,604," \
                          + d.dev_name + "," + d.dev_addr + ",off," \
                          + d.dev_status + "," + self.ts
            # call function
            self.msg_out = process_set_device_state_msg(
                self.log,
                self.msg_in,
                self.service_addresses)
            # check for proper number of outgoing messages generated
            self.assertEqual(len(self.msg_out), 1)
            # Check message contents
            self.msg_out_split = self.msg_out[0].split(",")
            self.assertEqual(self.msg_out_split[0], self.rn)
            self.assertEqual(self.msg_out_split[1], '127.0.0.1')
            self.assertEqual(self.msg_out_split[2], '27061')
            self.assertEqual(self.msg_out_split[3], '127.0.0.1')
            self.assertEqual(self.msg_out_split[4], '27001')
            self.assertEqual(self.msg_out_split[5], '604')
            self.assertEqual(self.msg_out_split[6], d.dev_name)
            self.assertEqual(self.msg_out_split[7], d.dev_addr)
            self.assertEqual(self.msg_out_split[8], 'off')
            self.assertEqual(self.msg_out_split[9], d.dev_status)
            self.assertEqual(self.msg_out_split[10], self.ts)


    def test_process_set_device_state_msg_ack(self):
        # Capture initial values for comparison
        for i, d in enumerate(self.devices):
            if d.dev_type == "wemo_switch":
                self.org_status = copy.copy(d.dev_status)
                self.org_ts = copy.copy(d.dev_last_seen)
                # Set up fake incoming message to test with
                self.ts = str(datetime.datetime.now())[:19]
                self.rn = self.ref_num.new()
                self.msg_in = self.rn + ",127.0.0.1,27061,127.0.0.1,27001,605," \
                              + d.dev_name + ",on," \
                              + self.ts
                # call function
                self.msg_out = process_set_device_state_msg_ack(
                    self.log,
                    self.devices,
                    self.msg_in)

                # check for proper number of outgoing messages generated
                self.assertEqual(len(self.msg_out), 0)

                # find item in device list it matches
                for p, q in enumerate(self.devices):
                    if q.dev_name == d.dev_name:
                        self.ptr = p
                        break
                self.assertEqual(self.devices[self.ptr].dev_name, d.dev_name)
                self.assertEqual(self.devices[self.ptr].dev_status, "on")
                self.assertEqual(self.devices[self.ptr].dev_last_seen, self.ts)




if __name__ == "__main__":
    unittest.main()
