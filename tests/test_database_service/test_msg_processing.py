#!/usr/bin/python3
""" test_msg_processing.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import configparser
import copy
import datetime
import logging
import sys
import unittest
if __name__ == "__main__":
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from rpihome_v3.helpers.ref_num import RefNum
from rpihome_v3.automation_service.configure import ConfigureService
from rpihome_v3.automation_service.msg_processing import create_heartbeat_msg



# Define test class ***********************************************************
class Test_message_processing_db(unittest.TestCase):
    """ unittests for Device Class, methods, and functions """

    def __init__(self, *args, **kwargs):
        # Configure logging
        logging.basicConfig(stream=sys.stdout)
        self.log = logging.getLogger(__name__)
        self.log.level = logging.DEBUG
        # Create tags for testing
        self.msg_in = str()
        self.msg_out = []
        self.ref_num = RefNum(self.log)
        self.ref_num_initial = int()
        self.temp_dt = datetime.datetime
        self.destinations = []
        # Create items that will come from config file
        self.parent_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.config_file = os.path.join(self.parent_path, 'config.ini')
        self.config = ConfigureService(self.config_file)
        self.service_addresses = self.config.get_servers()
        self.message_types = self.config.get_message_types()
        self.devices = self.config.get_devices()
        # Call parent class init
        super(Test_message_processing_db, self).__init__(*args, **kwargs)


    def setUp(self):
        # call parent class setup
        super(Test_message_processing_db, self).setUp()


    def test_init(self):
        """ test class __init__ and input variables """
        pass


    def test_create_heartbeat_msg(self):
        """ test correct outputs result from various inputs """
        self.destinations = [
            (self.service_addresses['database_addr'], self.service_addresses['database_port']),
            (self.service_addresses['motion_addr'], self.service_addresses['motion_port']),
            (self.service_addresses['nest_addr'], self.service_addresses['nest_port']),
            (self.service_addresses['occupancy_addr'], self.service_addresses['occupancy_port']),
            (self.service_addresses['schedule_addr'], self.service_addresses['schedule_port']),
            (self.service_addresses['wemo_addr'], self.service_addresses['wemo_port'])
        ]

        self.msg_out = create_heartbeat_msg(
            self.log,
            self.ref_num,
            self.destinations,
            self.service_addresses['database_addr'],
            self.service_addresses['database_port'],
            self.message_types)
        # check output
        self.assertEqual(len(self.msg_out), 6)
        self.msg_out_split = self.msg_out[0].split(",")



if __name__ == "__main__":
    unittest.main()
