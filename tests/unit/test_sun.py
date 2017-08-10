#!/usr/bin/python3
""" test_sun.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import datetime
import logging
import sys
import unittest
import env
from rpihome_v3.helpers.sun import Sun


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

    def __init__(self, *args, **kwargs):
        logging.basicConfig(stream=sys.stdout)
        self.log = logging.getLogger(__name__)
        self.log.level = logging.DEBUG
        super(TestSun, self).__init__(*args, **kwargs)


    def setUp(self):
        self.log = logging.getLogger(__name__)
        self.sun = Sun(38.566, -90.409, -5, self.log)
        super(TestSun, self).setUp()


    def test_sunrise(self):
        """ tests the functionality of the sunrise/sunset calc function """
        self.log.debug('Sunrise: %s', self.sun.sunrise())
        self.assertGreater(self.sun.sunrise().time(), datetime.time(4, 0))


    def test_solarnoon(self):
        """ tests the functionality of the sunrise/sunset calc function """
        self.log.debug('Solarnoon: %s', self.sun.solarnoon())
        self.assertGreater(self.sun.solarnoon().time(), datetime.time(4, 0))
        self.assertLess(self.sun.solarnoon().time(), datetime.time(16, 0))


    def test_sunset(self):
        """ tests the functionality of the sunrise/sunset calc function """
        self.log.debug('Sunset: %s', self.sun.sunset())
        self.assertGreater(self.sun.sunset().time(), datetime.time(16, 0))
        self.assertLess(self.sun.sunset().time(), datetime.time(22, 0))


if __name__ == "__main__":
    unittest.main()
