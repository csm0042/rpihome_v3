#!/usr/bin/python3
""" sun.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import logging
import datetime
from math import cos, sin, acos, asin, tan
from math import degrees as deg, radians as rad


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Sun Class *******************************************************************
class Sun(object):
    def __init__(self, latitude, longitude, offset_hours, logger):
        # Configure logger
        self._logger = logger or logging.getLogger(__name__)
        # Create other class objects
        self._latitude = latitude
        self._longitude = longitude
        self._offset_hours = offset_hours
        self._when = None
        self._day = None
        self._t = None
        self._time = None
        self._timezone = None
        self._offset = None
        self._jday = None
        self._jcent = None
        self._manom = None
        self._mlong = None
        self._eccent = None
        self._mobliq = None
        self._obliq = None
        self._vary = None
        self._seqcent = None
        self._struelong = None
        self._sapplong = None
        self._declination = None
        self._eqtime = None
        self._hourangle = None
        self._solarnoon_t = None
        self._sunrise_t = None
        self._sunset_t = None
        self._sunrise_UTC_h = None
        self._sunrise_UTC_m = None
        self._sunrise_UTC_s = None
        self._sunrise_UTC = None
        self._solarnoon_UTC_h = None
        self._solarnoon_UTC_m = None
        self._solarnoon_UTC_s = None
        self._solarnoon_UTC = None
        self._sunset_UTC_m = None
        self._sunset_UTC_s = None
        self._sunset_UTC = None
        self._day = None
        self._hours = None
        self._h = None
        self._minutes = None
        self._m = None
        self._seconds = None
        self._s = None
        self.calc()
        self._last_calc = datetime.datetime.now()
        self._logger.debug('Init complete for Sun class for coordinates '
                           '%s by %s', self._latitude, self._longitude)


    def calc(self, when=None):
        """ Perform the actual calculations for sunrise, sunset and a number of
        related quantities.  The results are stored in the instance variables
        sunrise_t, sunset_t and solarnoon_t """
        self._when = when

        # If no time is passed to the function, assume current date/time
        if self._when is None:
            self._when = datetime.datetime.now()
            self._logger.debug(
                'No time passed into class.  Running with current system datetime')
        else:
            self._when = datetime.datetime.combine(self._when, datetime.time(12, 0))
            self._logger.debug('Calculating sun rise, noon, and set for %s', self._when)

        # datetime days are numbered in the Gregorian calendar while the calculations
        # from NOAA are distibuted as OpenOffice spreadsheets with days numbered from
        # 1/1/1900. The difference are those numbers taken for 18/12/2010
        self._day = self._when.toordinal() - (734124 - 40529)
        self._logger.debug('Calculated _day as %s', self._day)
        self._t = self._when.time()
        self._logger.debug('Calculated _t as %s', self._t)
        self._time = (self._t.hour + self._t.minute / 60.0 + self._t.second / 3600.0) / 24.0
        self._logger.debug('Calculated _time as %s', self._time)

        self._timezone = 0
        self._offset = self._when.utcoffset()
        self._logger.debug('Calculated _offset as %s', self._offset)
        if not self._offset is None:
            self._timezone = self._offset.seconds / 3600.0
            self._logger.debug('Calculated _timezone as %s', self._timezone)

        # calculate offset timedelta based on offset hours passed in
        self._offset = datetime.timedelta(hours=self._offset_hours)
        self._logger.debug('Calculated _offset as %s', self._offset)

        # Calculate julian day and century
        self._jday = self._day + 2415018.5 + self._time - self._timezone / 24
        self._logger.debug('Calculated _jday as %s', self._jday)
        self._jcent = (self._jday - 2451545) / 36525
        self._logger.debug('Calculated _jcent as %s', self._jcent)

        # More calcs
        self._manom = 357.52911 + self._jcent * (35999.05029 - 0.0001537 * self._jcent)
        self._mlong = 280.46646 + self._jcent * (36000.76983 + self._jcent * 0.0003032) % 360
        self._eccent = 0.016708634 - self._jcent * (0.000042037 + 0.0001537 * self._jcent)
        self._mobliq = 23 + (26 + (
            (21.448 - self._jcent * (
                46.815 + self._jcent * (
                    0.00059 - self._jcent * 0.001813)))) / 60) / 60
        self._obliq = self._mobliq + 0.00256 * cos(rad(125.04 - 1934.136 * self._jcent))
        self._vary = tan(rad(self._obliq / 2)) * tan(rad(self._obliq / 2))
        self._seqcent = sin(rad(self._manom)) * (
            1.914602 - self._jcent * (
                0.004817 + 0.000014 * self._jcent)) + sin(
                    rad(2 * self._manom)) * (
                        0.019993 - 0.000101 * self._jcent) + sin(
                            rad(3 * self._manom)) * 0.000289
        self._struelong = self._mlong + self._seqcent
        self._sapplong = self._struelong - 0.00569 - 0.00478 * sin(
            rad(125.04 - 1934.136 * self._jcent))
        self._declination = deg(asin(sin(rad(self._obliq)) * sin(rad(self._sapplong))))

        self._eqtime = (
            4 * deg(self._vary * sin(2 * rad(self._mlong)) - (
                2 * self._eccent * sin(rad(self._manom))) + (
                    4 * self._eccent * self._vary * sin(rad(self._manom)) * cos(
                        2 * rad(self._mlong))) - (
                            0.5 * self._vary * self._vary * sin(4 * rad(self._mlong))) - (
                                1.25 * self._eccent * self._eccent * sin(2 * rad(self._manom)))))

        self._hourangle = deg(
            acos(cos(rad(90.833)) / (
                cos(rad(self._latitude)) * cos(
                    rad(self._declination))) - (
                        tan(
                            rad(self._latitude)) * tan(
                                rad(self._declination)))))

        self._solarnoon_t = (720 - 4 * self._longitude - self._eqtime + self._timezone * 60) / 1440
        self._sunrise_t = self._solarnoon_t - self._hourangle * 4 / 1440
        self._sunset_t = self._solarnoon_t + self._hourangle * 4 / 1440

        # Convert to UTC then adjust based on time zone offset (sunrise)
        self._sunrise_UTC_h, self._sunrise_UTC_m, self._sunrise_UTC_s = (
            self.time_from_decimal_day(self._sunrise_t))
        if self._sunrise_UTC_h < 24:
            self._sunrise_UTC = datetime.time(
                self._sunrise_UTC_h, self._sunrise_UTC_m, self._sunrise_UTC_s)
            self._sunrise_adj = datetime.datetime.combine(
                datetime.date.today(), self._sunrise_UTC) + self._offset
        elif self._sunrise_UTC_h >= 24:
            self._sunrise_UTC = datetime.time(
                (self._sunrise_UTC_h-24), self._sunrise_UTC_m, self._sunrise_UTC_s)
            self._sunrise_adj = datetime.datetime.combine(
                (datetime.date.today()+ datetime.timedelta(days=1)),
                self._sunrise_UTC) + self._offset

        # Convert to UTC then adjust based on time zone offset (solarnoon)
        self._solarnoon_UTC_h, self._solarnoon_UTC_m, self._solarnoon_UTC_s = (
            self.time_from_decimal_day(self._solarnoon_t))
        if self._solarnoon_UTC_h < 24:
            self._solarnoon_UTC = datetime.time(
                self._solarnoon_UTC_h, self._solarnoon_UTC_m, self._solarnoon_UTC_s)
            self._solarnoon_adj = datetime.datetime.combine(
                datetime.date.today(), self._solarnoon_UTC) + self._offset
        elif self._solarnoon_UTC_h >= 24:
            self._solarnoon_UTC = datetime.time(
                (self._solarnoon_UTC_h-24), self._solarnoon_UTC_m, self._solarnoon_UTC_s)
            self._solarnoon_adj = datetime.datetime.combine(
                (datetime.date.today() + datetime.timedelta(days=1)),
                self._solarnoon_UTC) + self._offset

        # Convert to UTC then adjust based on time zone offset (sunset)
        self._sunset_UTC_h, self._sunset_UTC_m, self._sunset_UTC_s = (
            self.time_from_decimal_day(self._sunset_t))
        if self._sunset_UTC_h < 24:
            self._sunset_UTC = datetime.time(
                self._sunset_UTC_h, self._sunset_UTC_m, self._sunset_UTC_s)
            self._sunset_adj = datetime.datetime.combine(
                datetime.date.today(), self._sunset_UTC) + self._offset
        elif self._sunset_UTC_h >= 24:
            self._sunset_UTC = datetime.time(
                (self._sunset_UTC_h-24), self._sunset_UTC_m, self._sunset_UTC_s)
            self._sunset_adj = datetime.datetime.combine(
                (datetime.date.today()+ datetime.timedelta(days=1)),
                self._sunset_UTC) + self._offset


    def time_from_decimal_day(self, day):
        """ returns a datetime.time object
        day is a decimal day between 0.0 and 1.0, e.g. noon = 0.5 """
        self._day = day
        self._hours = 24.0 * self._day
        self._h = int(self._hours)
        self._minutes = (self._hours - self._h) * 60
        self._m = int(self._minutes)
        self._seconds = (self._minutes - self._m) * 60
        self._s = int(self._seconds)
        return self._h, self._m, self._s


    def should_rerun(self, when=None):
        """ checks input data vs. last run of class to determine if a new
        round of calculations is necessary """
        if when != None:
            if when > self._last_calc + datetime.timedelta(hours=1):
                return True
        elif when == None:
            if datetime.datetime.now() > self._last_calc + datetime.timedelta(hours=1):
                return True
        else:
            return False


    def sunrise(self, when=None):
        """ Returns the sunrise time for the datetime fed via input
        parameters or current day/time if none are given """
        if self.should_rerun(when) is True:
            self.calc(when)
        return self._sunrise_adj


    def solarnoon(self, when=None):
        """ Returns the solar noon time for the datetime fed via input
        parameters or current day/time if none are given """
        if self.should_rerun(when) is True:
            self.calc(when)
        return self._solarnoon_adj


    def sunset(self, when=None):
        """ Returns the sunset time for the datetime fed via input
        parameters or current day/time if none are given """
        if self.should_rerun(when) is True:
            self.calc(when)
        return self._sunset_adj
