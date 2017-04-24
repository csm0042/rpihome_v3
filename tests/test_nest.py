#!/usr/bin/python3
""" test_nest.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import logging
import sys
import unittest
if __name__ == "__main__": sys.path.append("..")
import rpihome_v3


# Define test class ***********************************************************
class TestNest(unittest.TestCase):
    """ unittests for logger.py """
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        self.device = []
        self.device.append(rpihome_v3.Device('test_dev', 'nest', 'address', '', '', '', '', '', ''))
        self.credentials = 'c://python_files//credentials//credentials.txt'
        self.logger = logging.getLogger(__name__)


    def test_connect_to_nest(self):
        """ tests the functionality of the nest connection function """
        async def go():
            self.nest_device = await rpihome_v3.connect_to_nest(
                self.device, self.credentials, self.logger)
        self.loop.run_until_complete(go())
        print(self.nest_device)
        self.assertNotEqual(self.nest_device, None)



if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout)
    logger = logging.getLogger(__name__)
    logger.level = logging.DEBUG
    unittest.main()
