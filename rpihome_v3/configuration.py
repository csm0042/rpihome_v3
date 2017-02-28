#!/usr/bin/python3
""" configuration.py: Load application configuration values from INI file
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import configparser


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, rpihome Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Configuration helper functions **********************************************
config = configparser.ConfigParser()
config.read("config.ini")
