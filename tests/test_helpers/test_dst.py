#!/usr/bin/python3
""" test_dst.py:
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
from rpihome_v3.helpers.dst import USdst


# Define test class ***********************************************************
class TestDst(unittest.TestCase):
    """ unittests for Device Class, methods, and functions """

    def __init__(self, *args, **kwargs):
        logging.basicConfig(stream=sys.stdout)
        self.log = logging.getLogger(__name__)
        self.log.level = logging.DEBUG
        self.dst_checker = USdst(log=self.log)
        self.dt = None
        super(TestDst, self).__init__(*args, **kwargs)


    def setUp(self):
        super(TestDst, self).setUp()


    def test_init(self):
        """ test class __init__ and input variables """
        pass


    def test_dt(self):
        """ test setting and getting datetime value """
        self.dt = datetime.datetime.now()
        self.dst_checker.dt = copy.copy(self.dt)
        self.assertEqual(self.dst_checker.dt, self.dt)


if __name__ == "__main__":
    unittest.main()
