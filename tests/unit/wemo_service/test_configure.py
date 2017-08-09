#!/usr/bin/python3
""" test_configure.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import datetime
import logging
import sys
import unittest
import env
from rpihome_v3.wemo_service.configure import configure_log
from rpihome_v3.wemo_service.configure import configure_servers
from rpihome_v3.wemo_service.configure import configure_message_types


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
class TestConfigure(unittest.TestCase):
    """ unittests for Log Status Update Message Class """

    def __init__(self, *args, **kwargs):
        logging.basicConfig(stream=sys.stdout)
        self.log = logging.getLogger(__name__)
        self.log.level = logging.DEBUG
        self.new_logger = None
        self.config_file = None
        self.servers = None
        self.message_types = None
        super(TestConfigure, self).__init__(*args, **kwargs)


    def setUp(self):
        super(TestConfigure, self).setUp()


    def test_init(self):
        """ test class __init__ and input variables """
        self.assertEqual(self.new_logger, None)
        self.assertEqual(self.config_file, None)
        self.assertEqual(self.servers, None)
        self.assertEqual(self.message_types, None)


    def test_configure_log(self):
        """ test """
        self.new_logger = configure_log('config.ini')
        self.assertIsInstance(self.new_logger, logging.Logger)


    def test_configure_servers(self):
        """ test """
        self.servers = configure_servers('config.ini', self.log)
        self.assertEqual(len(self.servers), 14)
        self.assertEqual(self.servers['automation_addr'], '127.0.0.1')
        self.assertEqual(self.servers['wemo_port'], '27061')


    def test_configure_message_types(self):
        """ test """
        self.message_types = configure_message_types('config.ini', self.log)
        self.assertEqual(self.message_types['database_lsu'], '100')
        self.assertEqual(self.message_types['database_lsu_ack'], '101')
        self.assertEqual(self.message_types['database_uc'], '104')
        self.assertEqual(self.message_types['database_uc_ack'], '105')
        self.assertEqual(self.message_types['wemo_gds'], '600')
        self.assertEqual(self.message_types['wemo_gds_ack'], '601')


if __name__ == "__main__":
    unittest.main()