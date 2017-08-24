#!/usr/bin/env python
# -*- coding: utf-8 -*-

import myutil
import configHelper


def func():
    print("中文异常")
    raise Exception("中文")

IReserve = myutil.get_class(configHelper.readEngine())
ir = IReserve()
time.sleep(1)
# errorList = ir.reserve(url, clientInfo, self.__test)
