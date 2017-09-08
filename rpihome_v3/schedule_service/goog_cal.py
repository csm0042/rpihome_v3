#!/usr/bin/python3
""" goog_cal.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
#from __future__ import print_function
import copy
import datetime
import logging
import os
import sys
import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from rpihome_v3.schedule_service.schedule import Sched


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Class Definitions ***********************************************************
class GoogleCalSync(object):
    """ Class and methods necessary to read items from a google calendar  """
    def __init__(self, cal_id=None, credential_dir=None, client_secret=None, log=None):
        # Configure logger
        self.log = log or logging.getLogger(__name__)
        self.log.debug('Logger configured')
        # Import calendar ID
        self.log.debug('Configuring for calendar ID: [%s]', cal_id)
        self.cal_id = cal_id
        # Define crediential storage directory
        if credential_dir is not None:
            self.log.debug('Configuring for credential directory: [%s]', credential_dir)
            self.credential_dir = credential_dir
        else:
            self.home_dir = os.path.expanduser('~')
            self.log.debug('Using home directory: %s', self.home_dir)
            self.credential_dir = os.path.join(self.home_dir, '.credentials')
            self.log.debug('Using Credential directory: %s', self.credential_dir)
            # If credential directory does not exist, create it
            if not os.path.exists(self.credential_dir):
                self.log.debug("Creating directory: %s", self.credential_dir)
                os.makedirs(self.credential_dir)
        # Define credential file and store
        self.credential_file = os.path.join(self.credential_dir, 'calendar-python-auth.json')
        self.log.debug('Using credential file: %s', self.credential_file)
        self.store = Storage(self.credential_file)
        self.log.debug("Setting store to: %s", self.store)
        # Define client secret file and credentail objects
        if client_secret is not None:
            self.CLIENT_SECRET_FILE = client_secret
        else:
            self.CLIENT_SECRET_FILE = 'client_secret.json'
        self.SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
        self.APPLICATION_NAME = 'Google Calendar Read via Google Sheets API'
        self.credentials = None
        self.flow = None
        # Define Schedule objects
        self.http = None
        self.service = None
        self.now = None
        self.result = None
        self.events = None
        self.schedule = []
        self.result_list = []
        self._last_run = datetime.datetime.now() + datetime.timedelta(hours=-2)
        self.update_schedule()


    def get_credentials(self):
        """ Gets valid user credentials from storage. If nothing has been
        stored, or if the stored credentials are invalid, the OAuth2
        flow is completed to obtain the new credentials.
        Returns: Credentials, the obtained credential.  """
        # Get credentials from store
        self.credentials = self.store.get()
        self.log.debug("Getting credentials from store")
        if not self.credentials or self.credentials.invalid:
            self.log.debug("Credentials not in store")
            self.flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            self.flow.user_agent = self.APPLICATION_NAME
            self.credentials = tools.run_flow(self.flow, self.store, None)
            self.log.debug('Storing credentials to ' + self.credential_dir)

        self.log.debug("Returning credentials to main program")
        return self.credentials


    def read_data(self):
        """ Returns all events for the next 14 days using the
        google calendar API """
        self.credentials = self.get_credentials()
        self.http = self.credentials.authorize(httplib2.Http())
        self.service = discovery.build('calendar', 'v3', http=self.http)
        self.now = datetime.datetime.utcnow().isoformat() + 'Z'
        # Perform call to Google calendar API
        self.result = self.service.events().list(
            calendarId=self.cal_id,
            timeMin=self.now,
            maxResults=100,
            singleEvents=True,
            orderBy="startTime"
            ).execute()
        self.events = self.result.get('items', [])
        # Check if read operation returned any data
        if not self.events:
            self.log.debug("No upcoming events found")
            return False
        else:
            self.log.debug('Events found')
            return True


    def convert_data(self):
        """ converts event list raw format to a structured format useful for
        comparisons between time/dates """
        self.schedule = []
        # Cycle through raw event list and convert to a usable format
        for event in self.events:
            self.schedule.append(Sched(
                log=self.log,
                name=self.extract_name(event),
                start=self.extract_start(event),
                end=self.extract_end(event)))


    def update_schedule(self):
        """ Triggers a re-read of the data from google and updates the
        internal schedule snap-shot as long as the read was successful.
        If the read was not successful, it leaves the last batch of valid
        data in place to continue using until the next update """
        if self.cal_id != None:
            if self.read_data() is True:
                self.convert_data()
                self._last_run = datetime.datetime.now()


    def extract_name(self, event):
        """ extract name/summary from calendar data returned from API """
        return str(event['summary']).lower()


    def extract_start_date(self, event):
        """ extract event start date from calendar data returned from API """
        return datetime.date(
            int(str(event['start'].get('dateTime'))[0:4]),
            int(str(event['start'].get('dateTime'))[5:7]),
            int(str(event['start'].get('dateTime'))[8:10]))


    def extract_start_time(self, event):
        """ extract event start time from calendar data returned from API """
        return datetime.time(
            int(str(event['start'].get('dateTime'))[11:13]),
            int(str(event['start'].get('dateTime'))[14:16]),
            0)


    def extract_start(self, event):
        """ extract event start datetime from calendar data returned from API """
        return datetime.datetime.combine(
            self.extract_start_date(event),
            self.extract_start_time(event))


    def extract_end_date(self, event):
        """ extract event end date from calendar data returned from API """
        return datetime.date(
            int(str(event['end'].get('dateTime'))[0:4]),
            int(str(event['end'].get('dateTime'))[5:7]),
            int(str(event['end'].get('dateTime'))[8:10]))


    def extract_end_time(self, event):
        """ extract event end time from calendar data returned from API """
        return datetime.time(
            int(str(event['end'].get('dateTime'))[11:13]),
            int(str(event['end'].get('dateTime'))[14:16]),
            0)


    def extract_end(self, event):
        """ extract event end datetime from calendar data returned from API """
        return datetime.datetime.combine(
            self.extract_end_date(event),
            self.extract_end_time(event))


    def should_rerun(self, when=None):
        """ checks input data vs. last run of class to determine if a new
        round of calculations is necessary """
        if when is not None:
            if when > self._last_run + datetime.timedelta(hours=1):
                return True
        elif when is None:
            if datetime.datetime.now() > self._last_run + datetime.timedelta(hours=1):
                return True
        else:
            return False


    def sched_by_name(self, name=None):
        """ returns on/off schedule info for a specific device """
        # Check if calandar data currently in memory is current and perform
        # update if it is stale
        if self.should_rerun(datetime.datetime.now()) is True:
            self.update_schedule()
        # Obtain schedule info for named device
        self.result_list = []
        if name is not None:
            for sched in self.schedule:
                if sched.name == name:
                    self.result_list.append(copy.copy(sched))
        # Return results to main program
        return self.result_list


    def sched_by_date(self, date=None):
        """ returns on/off schedule info for all devices with assignments for
            a specific device """
        # Check if calandar data currently in memory is current and perform
        # update if it is stale
        if self.should_rerun(datetime.datetime.now()) is True:
            self.update_schedule()
        # Obtain schedule info for devices with assignments for this date
        self.result_list = []
        if date is not None:
            for sched in self.schedule:
                if sched.start.date() <= date <= sched.end.date():
                    self.result_list.append(copy.copy(sched))
        # Return results to main program
        return self.result_list


    def check_schedule(self, name=None):
        """ returns true if the device should be on, false if the device should
            be off """
        # Rerun schedule update if data is stale
        if self.should_rerun(datetime.datetime.now()) is True:
            self.update_schedule()
        # Check device schedule and prior state command
        if name is not None:
            newCmd = False
            for record in self.schedule:
                if record.name == name:
                    if record.start <= datetime.datetime.now():
                        if record.end >= datetime.datetime.now():
                            newCmd = True
        # Return results to main program
        return newCmd



if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout)
    log = logging.getLogger(__name__)
    log.level = logging.DEBUG
    cal = GoogleCalSync(
        cal_id='r68pvu542kle1jm7jj9hjdp9o0@group.calendar.google.com',
        credential_dir='C://python_files//credentials',
        client_secret='C://python_files//credentials//client_secret.json',
        log=log)
    print(cal.check_schedule(name='test_dev'))
