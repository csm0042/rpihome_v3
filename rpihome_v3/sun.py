#!/usr/bin/python3
""" sunrise.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import logging
import datetime
from math import cos, sin, acos, asin, tan
from math import degrees as deg, radians as rad
import rpihome_v3


# Update automation device status *********************************************
async def update_sun(when, offset, latitude, longitude, srise, sset, loop, logger):
    """ test """
    sleep = 3600
    while True:
        try:
            # Calculate sun rise/set times for today's date
            srise, snoon, sset = calc_sun_rise_and_set(
                when, offset, latitude, longitude, logger)
            logger.debug('Sunrise time set to [%s]', srise)
            logger.debug('Sunset time set to [%s]', sset)

            # Do not loop when status flag is false
            if loop is False:
                logger.debug('Breaking out of update_device_status loop')
                break
            # Otherwise wait a pre-determined time period, then re-run the task
            logger.debug(
                'Sleeping sun rise/set calculation task for '
                '%s seconds before running again', str(sleep))
            await asyncio.sleep(sleep)
        except KeyboardInterrupt:
            logging.debug(
                'Stopping sun rise/set status process loop')
            break
            break


# Perform sunrise/set calculations ********************************************
def calc_sun_rise_and_set(when, offset_hours, latitude, longitude, logger=None):
    """ Perform the actual calculations for sunrise, sunset and a number of
    related quantities.  The results are stored in the instance variables
    sunrise_t, sunset_t and solarnoon_t """

    # Configure logger
    logger = logger or logging.getLogger(__name__)

    # If no time is passed to the function, assume current date/time
    if when is None:
        when = datetime.datetime.now()
    else:
        when = datetime.datetime.combine(when, datetime.time(12, 0))

    # datetime days are numbered in the Gregorian calendar while the calculations
    # from NOAA are distibuted as OpenOffice spreadsheets with days numbered from
    # 1/1/1900. The difference are those numbers taken for 18/12/2010
    day = when.toordinal() - (734124 - 40529)
    t = when.time()
    time = (t.hour + t.minute / 60.0 + t.second / 3600.0) / 24.0

    timezone = 0
    offset = when.utcoffset()
    if not offset is None:
        timezone = offset.seconds / 3600.0

    # calculate offset timedelta based on offset hours passed in
    offset = datetime.timedelta(hours=offset_hours)

    # Calculate julian day and century
    jday = day + 2415018.5 + time - timezone / 24
    jcent = (jday - 2451545) / 36525

    # More calcs
    manom = 357.52911 + jcent * (35999.05029 - 0.0001537 * jcent)
    mlong = 280.46646 + jcent * (36000.76983 + jcent * 0.0003032) % 360
    eccent = 0.016708634 - jcent * (0.000042037 + 0.0001537 * jcent)
    mobliq = 23 + (26 + (
        (21.448 - jcent * (46.815 + jcent * (0.00059 - jcent * 0.001813)))) / 60) / 60
    obliq = mobliq + 0.00256 * cos(rad(125.04 - 1934.136 * jcent))
    vary = tan(rad(obliq / 2)) * tan(rad(obliq / 2))
    seqcent = sin(rad(manom)) * (1.914602 - jcent * (0.004817 + 0.000014 * jcent)) + sin(
        rad(2 * manom)) * (0.019993 - 0.000101 * jcent) + sin(rad(3 * manom)) * 0.000289
    struelong = mlong + seqcent
    sapplong = struelong - 0.00569 - 0.00478 * sin(rad(125.04 - 1934.136 * jcent))
    declination = deg(asin(sin(rad(obliq)) * sin(rad(sapplong))))

    eqtime = 4 * deg(vary * sin(2 * rad(mlong)) - (
        2 * eccent * sin(rad(manom))) + (
            4 * eccent * vary * sin(rad(manom)) * cos(2 * rad(mlong))) - (
                0.5 * vary * vary * sin(4 * rad(mlong))) - (
                    1.25 * eccent * eccent * sin(2 * rad(manom))))

    hourangle = deg(acos(cos(rad(90.833)) / (cos(rad(latitude)) * cos(rad(declination))) - (
        tan(rad(latitude)) * tan(rad(declination)))))

    solarnoon_t = (720 - 4 * longitude - eqtime + timezone * 60) / 1440
    sunrise_t = solarnoon_t - hourangle * 4 / 1440
    sunset_t = solarnoon_t + hourangle * 4 / 1440

    # Convert to UTC then adjust based on time zone offset (sunrise)
    sunrise_UTC_h, sunrise_UTC_m, sunrise_UTC_s = time_from_decimal_day(
        sunrise_t)
    if sunrise_UTC_h < 24:
        sunrise_UTC = datetime.time(
            sunrise_UTC_h, sunrise_UTC_m, sunrise_UTC_s)
        sunrise_adj = datetime.datetime.combine(
            datetime.date.today(), sunrise_UTC) + offset
    elif sunrise_UTC_h >= 24:
        sunrise_UTC = time(
            (sunrise_UTC_h-24), sunrise_UTC_m, sunrise_UTC_s)
        sunrise_adj = datetime.datetime.combine(
            (datetime.date.today()+ datetime.timedelta(days=1)),
            sunrise_UTC) + offset

    # Convert to UTC then adjust based on time zone offset (solarnoon)
    solarnoon_UTC_h, solarnoon_UTC_m, solarnoon_UTC_s = time_from_decimal_day(
        solarnoon_t)
    if solarnoon_UTC_h < 24:
        solarnoon_UTC = datetime.time(
            solarnoon_UTC_h, solarnoon_UTC_m, solarnoon_UTC_s)
        solarnoon_adj = datetime.datetime.combine(
            datetime.date.today(), solarnoon_UTC) + offset
    elif solarnoon_UTC_h >= 24:
        solarnoon_UTC = datetime.time(
            (solarnoon_UTC_h-24), solarnoon_UTC_m, solarnoon_UTC_s)
        solarnoon_adj = datetime.datetime.combine(
            (datetime.date.today() + datetime.timedelta(days=1)),
            solarnoon_UTC) + offset

    # Convert to UTC then adjust based on time zone offset (sunset)
    sunset_UTC_h, sunset_UTC_m, sunset_UTC_s = time_from_decimal_day(
        sunset_t)
    if sunset_UTC_h < 24:
        sunset_UTC = datetime.time(
            sunset_UTC_h, sunset_UTC_m, sunset_UTC_s)
        sunset_adj = datetime.datetime.combine(
            date.today(), sunset_UTC) + offset
    elif sunset_UTC_h >= 24:
        sunset_UTC = datetime.time(
            (sunset_UTC_h-24), sunset_UTC_m, sunset_UTC_s)
        sunset_adj = datetime.datetime.combine(
            (datetime.date.today()+ datetime.timedelta(days=1)),
            sunset_UTC) + offset

    # Return results adjusted by time-zone to main program
    return sunrise_adj.time(), solarnoon_adj.time(), sunset_adj.time()


# Date format converter helper function ***************************************
def time_from_decimal_day(day):
    """ returns a datetime.time object
    day is a decimal day between 0.0 and 1.0, e.g. noon = 0.5 """
    hours = 24.0 * day
    h = int(hours)
    minutes = (hours - h) * 60
    m = int(minutes)
    seconds = (minutes - m) * 60
    s = int(seconds)
    return h, m, s
