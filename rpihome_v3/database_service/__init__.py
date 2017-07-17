#!/usr/bin/python3
""" database_service module init
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
from .configure import *
from .database import *
from .log_support import *
from .persistance import *


class RefNum(object):
    def __init__(self):
        self.source = 100

    def new(self):
        self.source += 1
        if self.source > 999:
            self.source = 100
        return str(self.source)
