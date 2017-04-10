#!/usr/bin/python3
""" configure.py:
    Configuration process for the RPiHome application.
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import os
import sys


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Defined named tuples for various object types *******************************



def check_motion(filepath, logger):
    found = False
    dir_contents = os.listdir(filepath)
    if len(dir_contents) > 0:
        found = True
        print('Screen-shot found')
    for file in dir_contents:
        try:
            os.remove(os.path.join(filepath, file))
        except:
            logger.debug('Oh crap, couldn\'t remove the requested file')
    return found
