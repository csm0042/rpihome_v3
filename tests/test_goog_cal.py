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
import rpihome_v3


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
class TestGoogCal(unittest.TestCase):
    """ unittests for logger.py """
    def setUp(self):
        self.logger = logging.getLogger(__name__)


    def test_read_data(self):
        """ test for credentials and data read """
        self.cal_object = rpihome_v3.GoogleCalSync(logger=self.logger)
        self.cal_object.read_data(
            cal_id='r68pvu542kle1jm7jj9hjdp9o0@group.calendar.google.com')
        for event in self.cal_object.events:
            print(
                'Device [%s]  On for [%s]' %
                (str(event['summary']),
                 str(event['start'].get('dateTime')))
                )


    def test_extract_start_time(self):
        """ test start time extraction """
        self.cal_object = rpihome_v3.GoogleCalSync(logger=self.logger)
        self.cal_object.read_data(
            cal_id='r68pvu542kle1jm7jj9hjdp9o0@group.calendar.google.com')
        for event in self.cal_object.events:
            print(self.cal_object.extract_start_time(event))





if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout)
    logger = logging.getLogger(__name__)
    logger.level = logging.DEBUG
    unittest.main()
