#!/usr/bin/python3
""" env.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import sys
import os

# append module root directory to sys.path ************************************
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )
        )
    )
)
