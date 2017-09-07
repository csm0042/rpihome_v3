#!/usr/bin/python3
""" test_message_ccs.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import copy
import datetime
import logging
import sys
import unittest
import env
from rpihome_v3.messages.field_checkers import in_int_range
from rpihome_v3.messages.field_checkers import is_valid_datetime


# Define test class ***********************************************************
class TestFieldCheckers(unittest.TestCase):
    """ unittests for field checkers for messages """

    def __init__(self, *args, **kwargs):
        logging.basicConfig(stream=sys.stdout)
        self.log = logging.getLogger(__name__)
        self.log.level = logging.DEBUG
        self.dt = datetime.datetime
        self.dt_initial = datetime.datetime
        super(TestFieldCheckers, self).__init__(*args, **kwargs)


    def setUp(self):
        super(TestFieldCheckers, self).setUp()


    def test_init(self):
        """ test class __init__ and input variables """
        pass


    def test_in_int_range(self):
        """ test function which checks whether an input value is within a
            range of integers """
        self.assertEqual(in_int_range(self.log, 202, 100, 999), True)
        self.assertEqual(in_int_range(self.log, 202, 1000, 9999), False)
        self.assertEqual(in_int_range(self.log, -1, 0, 999), False)
        self.assertEqual(in_int_range(self.log, 202, 100, 199), False)


    def test_is_valid_datetime1(self):
        """ test Valid input (datetime) and valid initial (datetime) value """
        self.dt = datetime.datetime.combine(
            datetime.date(2017, 1, 1),
            datetime.time(9, 3, 0)
        )
        self.dt_initial = datetime.datetime.combine(
            datetime.date(2017, 1, 1),
            datetime.time(9, 3, 0)
        )
        self.assertEqual(
            is_valid_datetime(
                self.log,
                self.dt,
                self.dt_initial
            ),
            '2017-01-01 09:03:00'
        )

    def test_is_valid_datetime2(self):
        """ test Valid input (datetime.date) and valid initial (datetime) value """
        self.dt = datetime.date(2017, 2, 1)
        self.dt_initial = datetime.datetime.combine(
            datetime.date(2017, 1, 1),
            datetime.time(9, 3, 0)
        )
        self.assertEqual(
            is_valid_datetime(
                self.log,
                self.dt,
                self.dt_initial
            )[0:10],
            '2017-02-01'
        )

    def test_is_valid_datetime3(self):
        """ test Valid input (datetime.time) and valid initial (datetime) value """
        self.dt = datetime.time(10, 12, 1)
        self.dt_initial = datetime.datetime.combine(
            datetime.date(2017, 1, 1),
            datetime.time(9, 3, 0)
        )
        self.assertEqual(
            is_valid_datetime(
                self.log,
                self.dt,
                self.dt_initial
            ),
            str(datetime.datetime.combine(datetime.date(2017, 9, 7), datetime.time(10, 12, 1)))[:19]
        )

    def test_is_valid_datetime4(self):
        """ test Valid input (datetime string) and valid initial (datetime) value """
        self.dt = '2017-01-01 09:03:00'
        self.dt_initial = datetime.datetime.combine(
            datetime.date(2017, 1, 1),
            datetime.time(9, 4, 0)
        )
        self.assertEqual(
            is_valid_datetime(
                self.log,
                self.dt,
                self.dt_initial
            ),
            str(datetime.datetime.combine(datetime.date(2017, 1, 1), datetime.time(9, 3, 0)))[:19]
        )

    def test_is_valid_datetime5(self):
        """ test Valid input (datetime.date string) and valid initial (datetime) value """
        self.dt = '2017-02-01'
        self.dt_initial = datetime.datetime.combine(
            datetime.date(2017, 1, 1),
            datetime.time(9, 3, 0)
        )
        self.assertEqual(
            is_valid_datetime(
                self.log,
                self.dt,
                self.dt_initial
            )[0:10],
            '2017-02-01'
        )

    def test_is_valid_datetime6(self):
        """ test Valid input (datetime.time string) and valid initial (datetime) value """
        self.dt = '10:12:01'
        self.dt_initial = datetime.datetime.combine(
            datetime.date(2017, 1, 1),
            datetime.time(9, 3, 0)
        )
        self.assertEqual(
            is_valid_datetime(
                self.log,
                self.dt,
                self.dt_initial
            ),
            '2017-09-07 10:12:01'
        )

    def test_is_valid_datetime7(self):
        """ test various invalid datetime.datetime string formats """
        self.dt = '2017-13-01 09:03:00'
        self.dt_initial = datetime.datetime.combine(
            datetime.date(2017, 1, 1),
            datetime.time(9, 4, 0)
        )
        self.assertEqual(
            is_valid_datetime(
                self.log,
                self.dt,
                self.dt_initial
            ),
            '2017-01-01 09:04:00'
        )

    def test_is_valid_datetime8(self):
        """ test various invalid datetime.datetime string formats """
        self.dt = '2017-12-32 09:03:00'
        self.dt_initial = datetime.datetime.combine(
            datetime.date(2017, 1, 1),
            datetime.time(9, 4, 0)
        )
        self.assertEqual(
            is_valid_datetime(
                self.log,
                self.dt,
                self.dt_initial
            ),
            '2017-01-01 09:04:00'
        )

    def test_is_valid_datetime9(self):
        """ test various invalid datetime.datetime string formats """
        self.dt = '2017-12-31 24:03:00'
        self.dt_initial = datetime.datetime.combine(
            datetime.date(2017, 1, 1),
            datetime.time(9, 4, 0)
        )
        self.assertEqual(
            is_valid_datetime(
                self.log,
                self.dt,
                self.dt_initial
            ),
            '2017-01-01 09:04:00'
        )

    def test_is_valid_datetime10(self):
        """ test various invalid datetime.datetime string formats """
        self.dt = '2017-12-31 23:60:00'
        self.dt_initial = datetime.datetime.combine(
            datetime.date(2017, 1, 1),
            datetime.time(9, 4, 0)
        )
        self.assertEqual(
            is_valid_datetime(
                self.log,
                self.dt,
                self.dt_initial
            ),
            '2017-01-01 09:04:00'
        )

    def test_is_valid_datetime11(self):
        """ test various invalid datetime.datetime string formats """
        self.dt = '2017-12-31 23:59:60'
        self.dt_initial = datetime.datetime.combine(
            datetime.date(2017, 1, 1),
            datetime.time(9, 4, 0)
        )
        self.assertEqual(
            is_valid_datetime(
                self.log,
                self.dt,
                self.dt_initial
            ),
            '2017-01-01 09:04:00'
        )

    def test_is_valid_datetime12(self):
        """ test various invalid datetime.datetime string formats """
        self.dt = '2017-12-31 23:59:59'
        self.dt_initial = datetime.datetime.combine(
            datetime.date(2017, 1, 1),
            datetime.time(9, 4, 0)
        )
        self.assertEqual(
            is_valid_datetime(
                self.log,
                self.dt,
                self.dt_initial
            ),
            '2017-12-31 23:59:59'
        )

    def test_is_valid_datetime13(self):
        """ test various invalid datetime.datetime string formats """
        self.dt = '2017-12-31 00:00:00'
        self.dt_initial = datetime.datetime.combine(
            datetime.date(2017, 1, 1),
            datetime.time(9, 4, 0)
        )
        self.assertEqual(
            is_valid_datetime(
                self.log,
                self.dt,
                self.dt_initial
            ),
            '2017-12-31 00:00:00'
        )



if __name__ == "__main__":
    unittest.main()
