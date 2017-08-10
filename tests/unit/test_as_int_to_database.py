#!/usr/bin/python3
""" test_device.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import copy
import datetime
import logging
import sys
import unittest
import env
from rpihome_v3.helpers.log_support import setup_log_handlers
from rpihome_v3.automation_service.int_to_database import process_db_lsu
from rpihome_v3.automation_service.int_to_database import process_db_lsu_ack
from rpihome_v3.automation_service.int_to_database import process_db_rc
from rpihome_v3.automation_service.int_to_database import process_db_rc_ack
from rpihome_v3.automation_service.int_to_database import process_db_uc
from rpihome_v3.automation_service.int_to_database import process_db_uc_ack
from rpihome_v3.helpers.device import search_device_list
from rpihome_v3.messages.message_lsu import LSUmessage
from rpihome_v3.messages.message_lsu_ack import LSUACKmessage
from rpihome_v3.messages.message_rc import RCmessage
from rpihome_v3.messages.message_rc_ack import RCACKmessage
from rpihome_v3.messages.message_sds import SDSmessage
from rpihome_v3.messages.message_sds_ack import SDSACKmessage
from rpihome_v3.messages.message_uc import UCmessage
from rpihome_v3.messages.message_uc_ack import UCACKmessage


# Define test class ***********************************************************
class TestASIntToDatabase(unittest.TestCase):
    """ unittests for Device Class, methods, and functions """

    def __init__(self, *args, **kwargs):
        self.log = setup_log_handlers(
            __file__,
            'c:/python_files/logs/rpihome_v3/test_debug.log',
            'c:/python_files/logs/rpihome_v3/test_info.log'
        )
        self.lsu_message = LSUmessage(log=self.log)
        self.lsu_ack_message = LSUACKmessage(log=self.log)
        self.rc_message = RCmessage(log=self.log)
        self.rc_ack_message = RCACKmessage(log=self.log)
        self.sds_message = SDSmessage(log=self.log)
        self.sds_ack_message = SDSACKmessage(log=self.log)
        self.uc_message = UCmessage(log=self.log)
        self.uc_ack_message = UCACKmessage(log=self.log)
        self.dummy_msg_in = str()
        self.dummy_msg_out_list = []
        self.service_addr = {
            'automation_addr':'127.0.0.1',
            'automation_port':'27001',
            'database_addr':'127.0.0.1',
            'database_port':'27011'
        }
        super(TestASIntToDatabase, self).__init__(*args, **kwargs)


    def setUp(self):
        super(TestASIntToDatabase, self).setUp()


    def test_init(self):
        """ test class __init__ and input variables """
        pass


    def test_process_db_lsu(self):
        """ test """
        self.dummy_msg_in = '101,127.2.2.1,15000,192.168.86.12,16000,' \
                            '100,' \
                            'device01,192.168.86.13,??,2017-01-01 01:00:00'
        self.dummy_msg_out_list = process_db_lsu(
            self.log,
            self.dummy_msg_in,
            self.service_addr
        )
        self.lsu_message.complete = copy.copy(self.dummy_msg_out_list[0])
        self.assertEqual(len(self.dummy_msg_out_list), 1)
        self.assertEqual(self.lsu_message.ref, '101')
        self.assertEqual(self.lsu_message.dest_addr, '127.0.0.1')
        self.assertEqual(self.lsu_message.dest_port, '27011')
        self.assertEqual(self.lsu_message.source_addr, '192.168.86.12')
        self.assertEqual(self.lsu_message.source_port, '16000')
        self.assertEqual(self.lsu_message.msg_type, '100')
        self.assertEqual(self.lsu_message.dev_name, 'device01')
        self.assertEqual(self.lsu_message.dev_addr, '192.168.86.13')
        self.assertEqual(self.lsu_message.dev_status, '??')
        self.assertEqual(self.lsu_message.dev_last_seen, '2017-01-01 01:00:00')


if __name__ == "__main__":
    unittest.main()
