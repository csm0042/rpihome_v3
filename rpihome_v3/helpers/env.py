#!/usr/bin/python3
""" env.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import sys
import os

# append module root directory to sys.path ************************************
print(os.path.abspath(__file__))
print(os.path.dirname(os.path.abspath(__file__)))
print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(
    # Gets us to rpihome_v3
    os.path.dirname(
        # Gets us to rpihome_v3\rpihome_v3
        os.path.dirname(
            # Gets us to rpihome_v3\rpihome_v3\helpers
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )
    )
)
