#!/usr/bin/python3
""" test_logger.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import logging
import sys
import unittest
import rpihome_v3


# Define test class ***********************************************************
class TestLogger(unittest.TestCase):
    """ unittests for logger.py """
    def setUp(self):
        self.debug_file, self.info_file = rpihome_v3.setup_log_files(__file__)
        self.logger = rpihome_v3.file_logger.setup_log_handlers(
            __file__, self.debug_file, self.info_file)


    def test_setup_log_files(self):
        """ tests to see if the proper paths have been set for the log file
        storage location """
        self.assertEqual(self.debug_file, "c:/python_logs/file_logger_test_debug.log")
        self.assertEqual(self.info_file, "c:/python_logs/file_logger_test_info.log")


    def test_setup_log_handlers(self):
        """ tests to see if the correct number of log handlers
        have been created """
        self.assertEqual(len(self.logger.handlers), 3)


    def test_setup_logging(self):
        """ creates a logger configuration and verifies correct number
        of handlers exist """
        self.logger = rpihome_v3.setup_logging(__file__)
        self.assertEqual(len(self.logger.handlers), 3)



if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout)
    logger = logging.getLogger(__name__)
    logger.level = logging.DEBUG
    unittest.main()