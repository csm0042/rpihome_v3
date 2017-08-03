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
import rpihome_v3.helpers as helpers


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
        self.device = []
        self.wemo_list = []
        super(TestWemo, self).__init__(*args, **kwargs)


    def setUp(self):
        self.device.append(helpers.Device(
            'br1lt2', 'wemo_switch', '192.168.86.28', '', '', '', '', '', ''))
        self.device.append(helpers.Device(
            'bylt1', 'wemo_switch', '192.168.86.22', '', '', '', '', '', ''))
        self.device.append(helpers.Device(
            'test_dev', 'wemo_switch', '', '', '', '', '', '', ''))
        self.credentials = 'c://python_files//credentials//credentials.txt'
        super(TestWemo, self).setUp()


    def test_wemo_discover(self):
        """ tests the functionality of the wemo discovery function """
        async def go():
            self.wemo_device = await helpers.wemo_discover(
                self.device[0], self.logger)
            self.assertEqual(self.wemo_device.name, "br1lt2")
            self.wemo_device = await helpers.wemo_discover(
                self.device[1], self.logger)
            self.assertEqual(self.wemo_device.name, "bylt1")
            self.wemo_device = await helpers.wemo_discover(
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
            self.assertEqual(len(self.wemo_list), 1)
            self.wemo_device, self.wemo_list = await rpihome_v3.wemo_read_status(
                self.device[1], self.wemo_list, self.logger)
            self.assertEqual(self.wemo_device.status, "0")
            self.assertEqual(len(self.wemo_list), 2)
            self.wemo_device, self.wemo_list = await rpihome_v3.wemo_read_status(
                self.device[2], self.wemo_list, self.logger)
            self.assertEqual(self.wemo_device.status, 'offline')
            self.assertEqual(len(self.wemo_list), 2)
        self.loop.run_until_complete(go())
        self.loop.close()


    def test_wemo_set_on(self):
        """ tests the functionality of the wemo read-status function """
        async def go():
            logger.debug('*******Starting set on test*********')
            self.wemo_device, self.wemo_list = await rpihome_v3.wemo_set_on(
                self.device[0], self.wemo_list, self.logger)
            self.assertEqual(self.wemo_device.status, "1")
            self.wemo_device, self.wemo_list = await rpihome_v3.wemo_read_status(
                self.device[0], self.wemo_list, self.logger)
            self.assertEqual(self.wemo_device.status, "1")
        self.loop.run_until_complete(go())
        self.loop.close()


    def test_wemo_set_off(self):
        """ tests the functionality of the wemo read-status function """
        async def go():
            logger.debug('*******Starting set off test*********')
            self.wemo_device, self.wemo_list = await rpihome_v3.wemo_set_off(
                self.device[0], self.wemo_list, self.logger)
            self.assertEqual(self.wemo_device.status, "0")
            self.wemo_device, self.wemo_list = await rpihome_v3.wemo_read_status(
                self.device[0], self.wemo_list, self.logger)
            self.assertEqual(self.wemo_device.status, "0")
        self.loop.run_until_complete(go())
        self.loop.close()



if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout)
    logger = logging.getLogger(__name__)
    logger.level = logging.DEBUG
    unittest.main()
