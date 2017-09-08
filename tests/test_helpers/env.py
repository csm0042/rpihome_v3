#!/usr/bin/python3
""" env.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import sys
import os

# append module root directory to sys.path ************************************
sys.path.append(
    # Gets us to rpihome_v3
    os.path.dirname(
        # Gets us to rpihome_v3\tests
        os.path.dirname(
            # Gets us to rpihome_v3\tests\unit
            os.path.dirname(
                # Gets us to rpihome_v3\tests\unit\helpers
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )
        )
    )
)
