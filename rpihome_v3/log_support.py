#!/usr/bin/python3
""" logging.py: Log file setup helper functions
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import logging
import logging.handlers
import os
import sys


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The Maue-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Logging helper functions ****************************************************
def setup_log_files(name):
    """ Function to decide where to store log files (folder in root) and
    create that folder if necessary """
    file_drive, file_path = os.path.splitdrive(name)
    log_path = os.path.join(file_drive, "/python_logs")
    full_path, file_name = os.path.split(name)
    file_name, file_ext = os.path.splitext(file_name)
    if not os.path.isdir(log_path):
        os.mkdir(log_path)
    debug_logfile = (log_path + "/" +  file_name + "_debug.log")
    info_logfile = (log_path + "/" + file_name + "_info.log")
    return debug_logfile, info_logfile


def setup_log_handlers(name, debug_logfile, info_logfile):
    """ Function to configure root logger with three handlers, one to stream
    info and up messages, plus two additional file handlers for debug and info
    messages """
    root = logging.getLogger(name)
    root.setLevel(logging.DEBUG)
    root.handlers = []
    # Create desired handlers
    debug_handler = logging.FileHandler(debug_logfile)
    info_handler = logging.FileHandler(info_logfile)
    console_handler = logging.StreamHandler(sys.stdout)
    # Set logging levels for each handler
    debug_handler.setLevel(logging.DEBUG)
    info_handler.setLevel(logging.INFO)
    console_handler.setLevel(logging.INFO)
    # Create individual formats for each handler
    debug_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')
    info_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')
    # Set formatting options for each handler
    debug_handler.setFormatter(debug_formatter)
    info_handler.setFormatter(info_formatter)
    console_handler.setFormatter(console_formatter)
    # Add handlers to root logger
    root.addHandler(debug_handler)
    root.addHandler(info_handler)
    root.addHandler(console_handler)
    root.debug("logging configured with 3 handlers")
    return root


def setup_logging(name):
    """ For those lazy people who want to be able to call a single function and get the full
    logging setup done in a single statement (aka: me)"""
    debug_file, info_file = setup_log_files(name)
    root_logger = setup_log_handlers(name, debug_file, info_file)
    return root_logger