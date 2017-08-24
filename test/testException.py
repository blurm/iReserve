#!/usr/bin/env python
# -*- coding: utf-8 -*-


import traceback

class IReserveException(BaseException):
    pass


def myExcep():
    """TODO: Docstring for myExcep.
    :returns: TODO

    """
    raise IReserveException("手机号无效")
try:
    myExcep()
except IReserveException as e:
    print(e)
    raise e
    traceback.print_exc()
finally:
    print("finally")
    traceback.print_exc()
