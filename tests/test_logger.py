#!/usr/bin/python3
""" test_logger.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import logging
import sys
import unittest
if __name__ == "__main__":
    sys.path.append("..")
import rpihome_v3.helpers as helpers


# Define test class ***********************************************************
class TestLogger(unittest.TestCase):
    """ unittests for logger.py """

    def __init__(self, *args, **kwargs):
        logging.basicConfig(stream=sys.stdout)
        self.log = logging.getLogger(__name__)
        self.log.level = logging.DEBUG
        self.info_file = "c://python_logs//info.log"
        self.debug_file = "c://python_logs//debug.log"
        self.logger = helpers.setup_log_handlers(
            __file__, self.debug_file, self.info_file)
        super(TestLogger, self).__init__(*args, **kwargs)


    def setUp(self):
        super(TestLogger, self).setUp()


    def test_setup_log_handlers(self):
        """ tests to see if the correct number of log handlers
        have been created """
        self.assertEqual(len(self.logger.handlers), 3)


if __name__ == "__main__":
    unittest.main()
    