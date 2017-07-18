#!/usr/bin/python3
""" ref_num.py: Message reference number class
"""

# Import Required Libraries (Standard, Third Party, Local) ********************


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The Maue-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Class definition ************************************************************
class RefNum(object):
    def __init__(self):
        self.source = 100

    def new(self):
        self.source += 1
        if self.source > 999:
            self.source = 100
        return str(self.source)
