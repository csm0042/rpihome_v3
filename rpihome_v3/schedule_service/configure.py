#!/usr/bin/python3
""" configure.py:
    Configuration helper functions used to set up this service
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import configparser
import datetime
import sys
if __name__ == "__main__":
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from rpihome_v3.helpers.log_support import setup_log_handlers
from rpihome_v3.schedule_service.schedule import Sched
from rpihome_v3.schedule_service.goog_cal import GoogleCalSync


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Config Function Def *********************************************************
class ConfigureService(object):
    def __init__(self, filename):
        self.filename = filename
        self.service_addresses = {}
        self.message_types = {}
        self.credentials = None
        self.schedule = None
        # Define connection to configuration file
        self.config_file = configparser.ConfigParser()
        self.cred_file = configparser.ConfigParser()
        # Configure logger
        self.log = self.get_logger()


    def get_logger(self):
        # Set up application logging
        self.config_file.read(self.filename)
        self.log = setup_log_handlers(
            __file__,
            self.config_file['LOG FILES']['schedule_debug_log_file'],
            self.config_file['LOG FILES']['schedule_info_log_file'])
        # Return configured objects to main program
        return self.log


    def get_servers(self):
        # Create dict with all services defined in INI file
        self.config_file.read(self.filename)        
        for option in self.config_file.options('SERVICES'):
            self.service_addresses[option] = self.config_file['SERVICES'][option]
        # Return dict of configured addresses and ports to main program
        return self.service_addresses


    def get_message_types(self):
        # Create dict with all services defined in INI file
        self.config_file.read(self.filename)        
        for option in self.config_file.options('MESSAGE TYPES'):
            self.message_types[option] = self.config_file['MESSAGE TYPES'][option]
        # Return dict of configured addresses and ports to main program
        return self.message_types


    def get_credentials(self):
        # Read credential info from file
        self.config_file.read(self.filename)        
        try:
            self.credentials = self.config_file['CREDENTIALS']['file']
            self.log.debug('Credentails file found')
        except:
            self.log.error('No credentials file found')
        # Return configured objects to main program
        return self.credentials


    def get_schedule(self):
        # Define connection to configuration file
        self.config_file.read(self.filename)
        self.cred_file.read(self.credentials)
        self.log.debug('Connections established to [%s] and [%s]',
                       self.config_file, self.cred_file)
        # Read credential info from file
        try:
            self.calId = self.cred_file['GOOGLE']['cal_id']
            self.log.debug('Setting calendar ID to: [%s]', self.calId)
            self.credentialDir = self.config_file['CALENDAR']['credential_dir']
            self.log.debug('Setting credential directory to: [%s]', self.credentialDir)
            self.clientSecretFile = self.config_file['CALENDAR']['client_secret_file']
            self.log.debug('Setting client secret file to: [%s]', self.clientSecretFile)
        except:
            self.calId = self.credentialDir = self.clientSecretFile = None
        # Create connection to calendar
        if self.calId is not None:
            self.schedule = GoogleCalSync(
                cal_id=self.calId,
                credential_dir=self.credentialDir,
                client_secret=self.clientSecretFile,
                log=self.log)
            self.log.debug('Created calendar object: [%s]', self.schedule)
        else:
            self.log.error('Error creating calendar object')
        # Return configured objects to main program
        return self.schedule
