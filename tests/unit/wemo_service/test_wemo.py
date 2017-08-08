#!/usr/bin/python3
""" test_wemo.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import logging
import sys
import unittest
if __name__ == "__main__":
    sys.path.append("..")
import env
from rpihome_v3.helpers import Device
from rpihome_v3.wemo_service import WemoAPI 


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Define test class ***********************************************************
class TestWemo(unittest.TestCase):
    """ unittests for logger.py """

    def __init__(self, *args, **kwargs):
        logging.basicConfig(stream=sys.stdout)
        self.log = logging.getLogger(__name__)
        self.log.level = logging.DEBUG
        self.loop = asyncio.new_event_loop()
        self.device_list = []
        self.wemo_gw = WemoAPI(log=self.log)
        self.wemo_device = None
        self.wemo_list = []
        self.new_status = str()
        self.new_ls = str()
        super(TestWemo, self).__init__(*args, **kwargs)


    def setUp(self):
        self.device_list.append(
            Device(
                log=self.log,
                dev_name='br1lt2',
                dev_type='wemo_switch',
                dev_addr='192.168.86.28'
            )
        )
        self.device_list.append(
            Device(
                log=self.log,
                dev_name='bylt1',
                dev_type='wemo_switch',
                dev_addr='192.168.86.22'
            )
        )
        self.device_list.append(
            Device(
                log=self.log,
                dev_name='test_dev',
                dev_type='wemo_switch'
            )
        )
        self.credentials = 'c://python_files//credentials//credentials.txt'
        super(TestWemo, self).setUp()


    def test_discover(self):
        """ tests the functionality of the wemo discovery function """
        self.wemo_device = self.wemo_gw.discover(
            self.device_list[0].dev_name,
            self.device_list[0].dev_addr
        )
        self.assertEqual(self.wemo_device.name, "br1lt2")
        self.wemo_device = self.wemo_gw.discover(
            self.device_list[1].dev_name,
            self.device_list[1].dev_addr
        )
        self.assertEqual(self.wemo_device.name, "bylt1")
        self.wemo_device = self.wemo_gw.discover(
            self.device_list[2].dev_name,
            self.device_list[2].dev_addr
        )
        self.assertEqual(self.wemo_device, None)


    def test_wemo_read_status(self):
        """ tests the functionality of the wemo read-status function """
        # First device in test device list
        self.new_status, self.new_ls = self.wemo_gw.read_status(
            self.device_list[0].dev_name,
            self.device_list[0].dev_addr,
            self.device_list[0].dev_status,
            self.device_list[0].dev_last_seen
        )
        self.assertEqual(self.new_status, "0")
        # Second device in test device list
        self.new_status, self.new_ls = self.wemo_gw.read_status(
            self.device_list[1].dev_name,
            self.device_list[1].dev_addr,
            self.device_list[1].dev_status,
            self.device_list[1].dev_last_seen
        )
        self.assertEqual(self.new_status, "1")
        # Third device in test device list
        self.new_status, self.new_ls = self.wemo_gw.read_status(
            self.device_list[2].dev_name,
            self.device_list[2].dev_addr,
            self.device_list[2].dev_status,
            self.device_list[2].dev_last_seen
        )
        self.assertEqual(self.new_status, "offline")


if __name__ == "__main__":
    unittest.main()
