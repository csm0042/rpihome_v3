#!/usr/bin/python3
""" test_message_lsu.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import datetime
import logging
import sys
import unittest
if __name__ == "__main__":
    sys.path.append("..")
import rpihome_v3.helpers as helpers


# Define test class ***********************************************************
class TestLSUmessage(unittest.TestCase):
    """ unittests for Log Status Update Message Class """

    def __init__(self, *args, **kwargs):
        logging.basicConfig(stream=sys.stdout)
        self.log = logging.getLogger(__name__)
        self.log.level = logging.DEBUG        
        self.datetime = datetime.datetime
        self.datetime_str = str()
        super(TestLSUmessage, self).__init__(*args, **kwargs)


    def setUp(self):
        self.lsu = helpers.LSUmessage(log=self.log)
        super(TestLSUmessage, self).setUp()


    def test_init(self):
        self.datetime = datetime.datetime.now()
        self.datetime_str = (str(self.datetime))[:19]
        self.lsu = helpers.LSUmessage(
            log=self.log,
            ref='101',
            dest_addr='192.168.86.1',
            dest_port='17061',
            source_addr='192.168.5.4',
            source_port='12000',
            msg_type='601',
            dev_name='fylt1',
            dev_addr='192.168.86.23',
            dev_status='on',
            dev_last_seen=self.datetime)
        self.assertEqual(self.lsu.ref, '101')
        self.assertEqual(self.lsu.dest_addr, '192.168.86.1')
        self.assertEqual(self.lsu.dest_port, '17061')
        self.assertEqual(self.lsu.source_addr, '192.168.5.4')
        self.assertEqual(self.lsu.source_port, '12000')
        self.assertEqual(self.lsu.msg_type, '601')
        self.assertEqual(self.lsu.dev_name, 'fylt1')
        self.assertEqual(self.lsu.dev_addr, '192.168.86.23')
        self.assertEqual(self.lsu.dev_status, 'on')
        self.assertEqual(self.lsu.dev_last_seen, self.datetime_str)


    def test_ref_number_field(self):
        self.lsu.ref = 100
        self.assertEqual(self.lsu.ref, '100')
        self.lsu.ref = '202'
        self.assertEqual(self.lsu.ref, '202')


    def test_dest_addr_field(self):
        self.lsu.dest_addr = '192.168.1.1'
        self.assertEqual(self.lsu.dest_addr, '192.168.1.1')
        self.lsu.dest_addr = '192.168.2.x'
        self.assertEqual(self.lsu.dest_addr, '192.168.1.1')


    def test_dest_port_field(self):
        self.lsu.dest_port = 11000
        self.assertEqual(self.lsu.dest_port, '11000')
        self.lsu.dest_port = '12000'
        self.assertEqual(self.lsu.dest_port, '12000')
        self.lsu.dest_port = 100
        self.assertEqual(self.lsu.dest_port, '12000')
        self.lsu.dest_port = '101'        
        self.assertEqual(self.lsu.dest_port, '12000')
        self.lsu.dest_port = '100000'        
        self.assertEqual(self.lsu.dest_port, '12000')
        self.lsu.dest_port = 101000  
        self.assertEqual(self.lsu.dest_port, '12000')
        self.lsu.dest_port = 17061
        self.assertEqual(self.lsu.dest_port, '17061')


    def test_source_addr_field(self):
        self.lsu.source_addr = '192.168.1.1'
        self.assertEqual(self.lsu.source_addr, '192.168.1.1')
        self.lsu.source_addr = '192.168.2.x'
        self.assertEqual(self.lsu.source_addr, '192.168.1.1')


    def test_source_port_field(self):
        self.lsu.source_port = 11000
        self.assertEqual(self.lsu.source_port, '11000')
        self.lsu.source_port = '12000'
        self.assertEqual(self.lsu.source_port, '12000')
        self.lsu.source_port = 100
        self.assertEqual(self.lsu.source_port, '12000')
        self.lsu.source_port = '101'
        self.assertEqual(self.lsu.source_port, '12000')
        self.lsu.source_port = '100000'
        self.assertEqual(self.lsu.source_port, '12000')
        self.lsu.source_port = 101000
        self.assertEqual(self.lsu.source_port, '12000')
        self.lsu.source_port = 17061
        self.assertEqual(self.lsu.source_port, '17061')


    def test_message_type_field(self):
        self.lsu.msg_type = 101
        self.assertEqual(self.lsu.msg_type, '101')
        self.lsu.msg_type = '102'
        self.assertEqual(self.lsu.msg_type, '102')


    def test_device_name_field(self):
        self.lsu.dev_name = 101
        self.assertEqual(self.lsu.dev_name, '101')
        self.lsu.dev_name = 'fylt1'
        self.assertEqual(self.lsu.dev_name, 'fylt1')


    def test_dev_addr_field(self):
        self.lsu.dev_addr = '192.168.1.1'
        self.assertEqual(self.lsu.dev_addr, '192.168.1.1')
        self.lsu.dev_addr = '192.168.2.x'
        self.assertEqual(self.lsu.dev_addr, '192.168.1.1')        


    def test_device_status_field(self):
        self.lsu.dev_status = 0
        self.assertEqual(self.lsu.dev_status, '0')
        self.lsu.dev_status = 1
        self.assertEqual(self.lsu.dev_status, '1')
        self.lsu.dev_status = '0'
        self.assertEqual(self.lsu.dev_status, '0')
        self.lsu.dev_status = '1'
        self.assertEqual(self.lsu.dev_status, '1')
        self.lsu.dev_status = 'on'
        self.assertEqual(self.lsu.dev_status, 'on')
        self.lsu.dev_status = 'off'
        self.assertEqual(self.lsu.dev_status, 'off')
        self.lsu.dev_status = 'ON'
        self.assertEqual(self.lsu.dev_status, 'on')
        self.lsu.dev_status = 'OFF'
        self.assertEqual(self.lsu.dev_status, 'off')


    def test_device_last_seen_field(self):
        self.datetime = datetime.datetime.now()
        self.datetime_str = (str(self.datetime))[:19]
        self.lsu.dev_last_seen = self.datetime
        self.assertEqual(self.lsu.dev_last_seen, self.datetime_str)
        self.datetime = datetime.datetime.now().date()
        self.assertEqual(len(self.lsu.dev_last_seen), 19)
        self.datetime = datetime.datetime.now().time()
        self.assertEqual(len(self.lsu.dev_last_seen), 19)



if __name__ == "__main__":
    unittest.main()