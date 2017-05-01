#!/usr/bin/python3
""" test_sun.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import datetime
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
class TestSun(unittest.TestCase):
    """ unittests for logger.py """
    def setUp(self):
        self.logger = logging.getLogger(__name__)
        self.sunrise_local, self.solarnoon_local, self.sunset_local = (
            rpihome_v3.calc_sun_rise_and_set(
                when=datetime.datetime.now(),
                offset_hours=-5,
                latitude=38.566,
                longitude=-90.409,
                logger=self.logger))


    def test_sunrise(self):
        """ tests the functionality of the sunrise/sunset calc function """
        self.logger.debug('Sunrise: %s', self.sunrise_local)
        self.assertGreater(self.sunrise_local, datetime.time(4, 0))


    def test_solarnoon(self):
        """ tests the functionality of the sunrise/sunset calc function """
        self.logger.debug('Solarnoon: %s', self.solarnoon_local)
        self.assertGreater(self.solarnoon_local, datetime.time(4, 0))
        self.assertLess(self.solarnoon_local, datetime.time(16, 0))


    def test_sunset(self):
        """ tests the functionality of the sunrise/sunset calc function """
        self.logger.debug('Sunset: %s', self.sunset_local)
        self.assertGreater(self.sunset_local, datetime.time(16, 0))
        self.assertLess(self.sunset_local, datetime.time(22, 0))


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout)
    logger = logging.getLogger(__name__)
    logger.level = logging.DEBUG
    unittest.main()
