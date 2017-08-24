#!/usr/bin/env python
# -*- coding: utf-8 -*-


class parent(object):
    """docstring for parent"""
    def __init__(self, arg):
        super(parent, self).__init__()
        self.arg = arg

    def func(self):
        """TODO: Docstring for func.

        :f: TODO
        :returns: TODO

        """
        print("parent func")


class child(parent):
    """docstring for child"""
    def __init__(self, arg):
        self.arg = arg
        self.__func1()

    __VAR = "this is clss var"

    def func(self):
        """TODO: Docstring for func.
        :returns: TODO

        """
        print(child.__VAR)

    def __func1(self):
        print("func1")


def test():
    o = child("dfsdf")

    me = "this is me"
    print(me)

    if len(me) > 1:
        print(len(me))
    else:
        print("nothing")


def testStr():
    cur_size = 1
    max_size = 2
    print("current messages: %s, maximum size: %s" % (cur_size, max_size))


if __name__ == "__main__":
    testStr()
