#!/usr/bin/env python
# -*- coding: utf-8 -*-


import configHelper


class IReserve(object):

    """Base class for reservation"""

    def __init__(self):
        # If under test mode
        self.test = configHelper.readMode('test')
        # If it is a working day.
        self.nightMode = configHelper.readMode('nightMode')
        self.partNumber = ""
        print("IReserve init")

    def __del__(self):
        print("IReserve deleted")

    def reserve(self):
        pass
