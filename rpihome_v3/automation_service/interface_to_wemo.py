#!/usr/bin/python3
""" interface_to_wemo.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import copy


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Process messages from wemo service ******************************************
def process_wemo_messages(rNumGen, msgHeader, msgPayload, log):
    """ This function performs the custom operations required when a message
        is received from the wemo service """
    # Initialize result list
    response_msg_list = []        
    # Message type 101 - wemo status update
    if msgPayload[0] == '101':
        # Need to write this code yet #################################
        pass
    # Message type 103 - wemo set on ACK
    elif msgPayload[0] == '103':
        # Need to write this code yet #################################        
        pass
    # Message type 105 - wemo set off ACK
    elif msgPayload[0] == '105':
        # Need to write this code yet #################################        
        pass
    # Return response message
    return response_msg_list  