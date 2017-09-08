#!/usr/bin/python3
""" field_checkers.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import datetime
import logging
import re
import env
from rpihome_v3.helpers.ipv4_help import check_ipv4


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


DATE_REGEX = r'\b([0-9][0-9][0-9][0-9])-((0[0-9])|(1[0-2]))-(([0-2][0-9])|(3[0-1]))'
TIME_REGEX = r'\b(([0-1][0-9])|(2[0-3])):([0-5][0-9]):([0-5][0-9])(\.\d{1,6})?'
DATETIME_REGEX = r'\b([0-9][0-9][0-9][0-9])-((0[0-9])|(1[0-2]))-(([0-2][0-9])|(3[0-1]))' \
                 r' (([0-1][0-9])|(2[0-3])):([0-5][0-9]):([0-5][0-9])(\.\d{1,6})?'


# In Integer range checker ****************************************************
def in_int_range(log, value, low_limit, high_limit):
    if isinstance(value, str):
        try:
            if int(low_limit) <= int(value) <= int(high_limit):
                return True
            else:
                return False
        except Exception:
            return False
    if isinstance(value, int):
        if int(low_limit) <= value <= int(high_limit):
            return True
        else:
            return False


# Valid datetime checker ******************************************************
def is_valid_datetime(log, value, initial_value):
    # When a valid datetime is provided, return its string equivalent,
    # truncated to the seconds field
    if isinstance(value, datetime.datetime):
        log.debug('Input value matches datetime format: %s', value)
        result = (str(value))[:19]
    
    # If only the date portion is provided, merge it with the current time
    elif isinstance(value, datetime.date):
        log.debug('Input value matches date format: %s', value)
        result = (str(
            datetime.datetime.combine(
                value,
                datetime.datetime.now().time()
            )
        ))[:19]
    
    # If only the time portion is provided, merge it with the current date
    elif isinstance(value, datetime.time):
        log.debug('Input value matches time format: %s', value)
        result = (str(
            datetime.datetime.combine(
                datetime.datetime.now().date(),
                value
            )
        ))[:19]
    
    # If the input value is provided in string format,
    # determine what data it contains
    elif isinstance(value, str):
        if re.fullmatch(DATE_REGEX, value) is not None:
            log.debug('Date regex match on string input value: %s', value)
            # input value provided was a date in string format
            result = (str(
                datetime.datetime.combine(
                    datetime.date(
                        int(value[0:4]),
                        int(value[5:7]),
                        int(value[8:])
                    ),
                    datetime.datetime.now().time()
                )
            ))[:19]
        elif re.fullmatch(TIME_REGEX, value) is not None:
            # input value provided was a time in string format
            log.debug('Time regex match on string input value: %s', value)
            result = (str(
                datetime.datetime.combine(
                    datetime.datetime.now().date(),
                    datetime.time(
                        int(value[0:2]),
                        int(value[3:5]),
                        int(value[6:])
                    )
                )
            ))[:19]
        elif re.fullmatch(DATETIME_REGEX, value) is not None:
            # input value provided was a datetime in string format
            log.debug('Datetime regex match on string input value: %s', value)
            result = value[:19]
        else:
            # Invalid format for input value.  Return original value
            log.debug('No date or time format match for input value: %s', value)
            result = None
    else:
        # Invalid format for input value.  Return original value
        log.debug('Invalid type for input value: %s', value)
        result = None
    # Decide what value to reuturn
    if result is not None:
        return result
    else:
        return (str(initial_value))[:19]
