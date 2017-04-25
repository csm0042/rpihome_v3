#!/usr/bin/python3
""" test_wemo.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import logging
import sys
import unittest
if __name__ == "__main__": sys.path.append("..")
import rpihome_v3


# Define test class ***********************************************************
class TestWemo(unittest.TestCase):
    """ unittests for logger.py """
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        self.device = []
        self.wemo_list = []
        self.device.append(rpihome_v3.Device(
            'fylt1', 'wemo_switch', '192.168.86.21', '', '', '', '', '', ''))
        self.device.append(rpihome_v3.Device(
            'bylt1', 'wemo_switch', '192.168.86.22', '', '', '', '', '', ''))
        self.device.append(rpihome_v3.Device(
            'test_dev', 'wemo_switch', '', '', '', '', '', '', ''))
        self.credentials = 'c://python_files//credentials//credentials.txt'
        self.logger = logging.getLogger(__name__)


    def test_wemo_discover(self):
        """ tests the functionality of the wemo discovery function """
        async def go():
            self.wemo_device = await rpihome_v3.wemo_discover(
                self.device[0], self.logger)
            self.assertEqual(self.wemo_device.name, "fylt1")
            self.wemo_device = await rpihome_v3.wemo_discover(
                self.device[1], self.logger)
            self.assertEqual(self.wemo_device.name, "bylt1")
            self.wemo_device = await rpihome_v3.wemo_discover(
                self.device[2], self.logger)
            self.assertEqual(self.wemo_device, None)
        self.loop.run_until_complete(go())
        self.loop.close()


    def test_wemo_read_status(self):
        """ tests the functionality of the wemo read-status function """
        async def go():
            self.wemo_device, self.wemo_list = await rpihome_v3.wemo_read_status(
                self.device[0], self.wemo_list, self.logger)
            self.assertEqual(self.wemo_device.status, "0")
            self.wemo_device, self.wemo_list = await rpihome_v3.wemo_read_status(
                self.device[1], self.wemo_list, self.logger)
            self.assertEqual(self.wemo_device.status, "0")
            self.wemo_device, self.wemo_list = await rpihome_v3.wemo_read_status(
                self.device[2], self.wemo_list, self.logger)
            self.assertEqual(self.wemo_device.status, 'offline')
        self.loop.run_until_complete(go())
        self.loop.close()



if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout)
    logger = logging.getLogger(__name__)
    logger.level = logging.DEBUG
    unittest.main()
