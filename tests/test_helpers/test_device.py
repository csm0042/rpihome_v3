#!/usr/bin/python3
""" test_device.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import copy
import datetime
import logging
import sys
import unittest
if __name__ == "__main__":
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from rpihome_v3.helpers.device import search_device_list
from rpihome_v3.helpers.device import Device


# Define test class ***********************************************************
class TestDevice(unittest.TestCase):
    """ unittests for Device Class, methods, and functions """

    def __init__(self, *args, **kwargs):
        logging.basicConfig(stream=sys.stdout)
        self.log = logging.getLogger(__name__)
        self.log.level = logging.DEBUG
        self.device = Device(log=self.log)
        self.device_list = []
        self.datetime = datetime.datetime
        self.datetime_str = str()
        super(TestDevice, self).__init__(*args, **kwargs)


    def setUp(self):
        super(TestDevice, self).setUp()


    def test_init(self):
        """ test class __init__ and input variables """
        self.datetime = datetime.datetime.now()
        self.datetime_str = (str(self.datetime))[:19]
        self.device.dev_name = 'device01'
        self.device.dev_type = 'wemo_switch'
        self.device.dev_addr = '192.168.86.12'
        self.device.dev_cmd = 'on'
        self.device.dev_status = 'off'
        self.device.dev_last_seen = self.datetime
        self.device.dev_rule = 'dusk to dawn'
        self.assertEqual(self.device.dev_name, 'device01')
        self.assertEqual(self.device.dev_type, 'wemo_switch')
        self.assertEqual(self.device.dev_addr, '192.168.86.12')
        self.assertEqual(self.device.dev_cmd, 'on')
        self.assertEqual(self.device.dev_status, 'off')
        self.assertEqual(self.device.dev_last_seen, self.datetime_str)


    def test_dev_name(self):
        """ test setting and getting message reference number field """
        self.device.dev_name = 'new_device'
        self.assertEqual(self.device.dev_name, 'new_device')
        self.device.dev_name = 1001
        self.assertEqual(self.device.dev_name, '1001')


    def test_dev_type(self):
        """ test setting and getting message type field """
        self.device.dev_type = 101
        self.assertEqual(self.device.dev_type, '101')
        self.device.dev_type = 'wemo_insight'
        self.assertEqual(self.device.dev_type, 'wemo_insight')


    def test_dev_addr(self):
        """ test setting and getting device address field """
        self.device.dev_addr = '192.168.1.1'
        self.assertEqual(self.device.dev_addr, '192.168.1.1')
        self.device.dev_addr = '192.168.2.x'
        self.assertEqual(self.device.dev_addr, '192.168.1.1')
        self.device.dev_addr = '192.168.86.13'
        self.assertEqual(self.device.dev_addr, '192.168.86.13')


    def test_dev_cmd(self):
        """ test setting and getting message type field """
        self.device.dev_cmd = 0
        self.assertEqual(self.device.dev_cmd, '0')
        self.device.dev_cmd = 1
        self.assertEqual(self.device.dev_cmd, '1')
        self.device.dev_cmd = '0'
        self.assertEqual(self.device.dev_cmd, '0')
        self.device.dev_cmd = '1'
        self.assertEqual(self.device.dev_cmd, '1')
        self.device.dev_cmd = 'on'
        self.assertEqual(self.device.dev_cmd, 'on')
        self.device.dev_cmd = 'off'
        self.assertEqual(self.device.dev_cmd, 'off')
        self.device.dev_cmd = 'ON'
        self.assertEqual(self.device.dev_cmd, 'on')
        self.device.dev_cmd = 'OFF'
        self.assertEqual(self.device.dev_cmd, 'off')


    def test_device_status_field(self):
        """ test setting and getting device status field """
        self.device.dev_status = 0
        self.assertEqual(self.device.dev_status, '0')
        self.device.dev_status = 1
        self.assertEqual(self.device.dev_status, '1')
        self.device.dev_status = '0'
        self.assertEqual(self.device.dev_status, '0')
        self.device.dev_status = '1'
        self.assertEqual(self.device.dev_status, '1')
        self.device.dev_status = 'on'
        self.assertEqual(self.device.dev_status, 'on')
        self.device.dev_status = 'off'
        self.assertEqual(self.device.dev_status, 'off')
        self.device.dev_status = 'ON'
        self.assertEqual(self.device.dev_status, 'on')
        self.device.dev_status = 'OFF'
        self.assertEqual(self.device.dev_status, 'off')


    def test_device_last_seen_field(self):
        """ test setting and getting device last seen field """
        self.datetime = datetime.datetime.now()
        self.datetime_str = (str(self.datetime))[:19]
        self.device.dev_last_seen = self.datetime
        self.assertEqual(self.device.dev_last_seen, self.datetime_str)
        self.datetime = datetime.datetime.now().date()
        self.assertEqual(len(self.device.dev_last_seen), 19)
        self.datetime = datetime.datetime.now().time()
        self.assertEqual(len(self.device.dev_last_seen), 19)


    def test_search_device_list(self):
        self.device.dev_name = 'name@index0'
        self.device_list.append(copy.copy(self.device))
        self.device.dev_name = 'name@index1'
        self.device_list.append(copy.copy(self.device))
        self.device.dev_name = 'name@index2'
        self.device_list.append(copy.copy(self.device))
        self.device.dev_name = 'name@index3'
        self.device_list.append(copy.copy(self.device))
        self.assertEqual(
            search_device_list(self.log, self.device_list, 'name@index3'), 3)
        self.assertEqual(
            search_device_list(self.log, self.device_list, 'name@index2'), 2)
        self.assertEqual(
            search_device_list(self.log, self.device_list, 'name@index1'), 1)
        self.assertEqual(
            search_device_list(self.log, self.device_list, 'name@index0'), 0)
        self.assertEqual(
            search_device_list(self.log, self.device_list, 'name@index9'), None)



if __name__ == "__main__":
    unittest.main()
