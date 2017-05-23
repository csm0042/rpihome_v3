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
        self.cal_object = rpihome_v3.GoogleCalSync(logger=self.logger)
        self.cal_object.update_schedule(
            cal_id='r68pvu542kle1jm7jj9hjdp9o0@group.calendar.google.com')


    def test_extract_name(self):
        """ test name extraction method """
        print("***** NAMES *************************************")
        for event in self.cal_object.events:
            print(self.cal_object.extract_name(event))


    def test_extract_start_date(self):
        """ test start date conversion method """
        print("***** START DATES *******************************")
        for event in self.cal_object.events:
            print(self.cal_object.extract_start_date(event))


    def test_extract_start_time(self):
        """ test start time conversion method """
        print("***** START TIMES *******************************")
        for event in self.cal_object.events:
            print(self.cal_object.extract_start_time(event))


    def test_extract_start(self):
        """ test start datetime conversion method """
        print("***** START DATETIMES ***************************")
        for event in self.cal_object.events:
            print(self.cal_object.extract_start(event))


    def test_extract_end_date(self):
        """ test end date conversion method """
        print("***** END DATES *******************************")
        for event in self.cal_object.events:
            print(self.cal_object.extract_end_date(event))


    def test_extract_end_time(self):
        """ test end time conversion method """
        print("***** END TIMES *******************************")
        for event in self.cal_object.events:
            print(self.cal_object.extract_end_time(event))


    def test_extract_end(self):
        """ test end datetime conversion method """
        print("***** END DATETIMES ***************************")
        for event in self.cal_object.events:
            print(self.cal_object.extract_end(event))


    def test_convert_data(self):
        """ test calendar data conversion method """
        print('***** CONVERTED CALENDAR **********************')
        self.cal_object.convert_data()
        for conv_event in self.cal_object.schedule:
            print(conv_event)

    def test_sched_by_name(self):
        """ test schedule pull by device name """
        print('***** SCHEDULE FOR br1lt2 **********************')
        print(self.cal_object.sched_by_name('br1lt2'))




if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout)
    logger = logging.getLogger(__name__)
    logger.level = logging.DEBUG
    unittest.main()
