#!/usr/bin/python3
""" goog_cal.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
#from __future__ import print_function
import httplib2
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import asyncio
import datetime
import logging
import sys
import typing


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Main event loop function ****************************************************
async def update_schedule(credentials, loop, logger):
    """ queries google calendar and returns list of items for current week """
    while True:
        try:
            logger.debug('Starting 5-second sleep to simulate schedule lookup')
            await asyncio.sleep(5)
            schedule = (1, 2, 3, 4, 5)
            if loop is False:
                logger.debug('Breaking out of update schedule loop')
                break
            logger.debug(
                'Sleeping update_schedule task for 60 seconds before running again')
            await asyncio.sleep(60)
        except KeyboardInterrupt:
            logging.debug('Stopping update_schedule process loop')
            break
    return schedule


# Class Definitions ***********************************************************
class GoogleCalSync(object):
    """ Class and methods necessary to read items from a google calendar
    """
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.home_dir = str()
        self.credential_dir = str()
        self.store = str()
        self.credentials = str()
        self.path = str()
        self.CLIENT_SECRET_FILE = str()
        self.SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
        self.CLIENT_SECRET_FILE = 'client_secret.json'
        self.APPLICATION_NAME = 'Google Calendar Read via Google Sheets API'


    def get_credentials(self):
        """ Gets valid user credentials from storage. If nothing has been
        stored, or if the stored credentials are invalid, the OAuth2
        flow is completed to obtain the new credentials.
        Returns: Credentials, the obtained credential.
        """
        # Define credentail file
        self.home_dir = os.path.expanduser('~')
        self.logger.debug('Using home directory: %s', self.home_dir)

        self.credential_dir = os.path.join(self.home_dir, '.credentials')
        self.logger.debug('Using Credential directory: %s', self.credential_dir)

        # If credential directory does not exist, create it
        if not os.path.exists(self.credential_dir):
            self.logger.debug("Creating directory: %s", self.credential_dir)
            os.makedirs(self.credential_dir)
        self.credential_path = os.path.join(
            self.credential_dir, 'calendar-python-auth.json')
        self.logger.debug('Using credential file: %s', self.credential_path)

        self.store = Storage(self.credential_path)
        self.logger.debug("Setting store to: %s", self.store)

        self.credentials = self.store.get()
        self.logger.debug("Getting credentials from store")

        if not self.credentials or self.credentials.invalid:
            self.logger.debug("Credentials not in store")
            #self.path = os.path.dirname(sys.argv[0])
            #self.logger.debug("System path is: %s", self.path)
            #self.CLIENT_SECRET_FILE = os.path.join(self.path, "client_secret.json")
            #self.logger.debug("Looking for json file at: %s", self.CLIENT_SECRET_FILE)
            self.flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            self.flow.user_agent = self.APPLICATION_NAME
            self.credentials = tools.run_flow(self.flow, self.store, None)
            self.logger.debug('Storing credentials to ' + self.credential_path)
        self.logger.debug("Returning credentials to main program")
        return self.credentials


    def read_data(self, cal_id=None):
        """ Returns all events for the next 14 days using the google calendar API
        """
        self.credentials = self.get_credentials()
        self.http = self.credentials.authorize(httplib2.Http())
        self.service = discovery.build('calendar', 'v3', http=self.http)

        self.now = datetime.datetime.utcnow().isoformat() + 'Z'
        self.result = self.service.events().list(
            calendarId=cal_id,
            timeMin=self.now,
            maxResults=100,
            singleEvents=True,
            orderBy="startTime"
            ).execute()
        self.events = self.result.get('items', [])

        if not self.events:
            self.logger.debug("No upcoming events found")
            return None
        else:
            self.logger.debug('Returning event list: %s', self.events)
            return self.events
