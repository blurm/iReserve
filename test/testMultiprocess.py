#!/usr/bin/env python
# -*- coding: utf-8 -*-


import multiprocessing
import time


def func():
    ps = []
    for i in xrange(3):
        p = multiprocessing.Process(target=subfunc, args=(i, ))
        p.start()
        ps.append(p)
    # for p in ps:
        # p.join()

def subfunc(i):
    print("child process %d start" % i)
    time.sleep(3)
    print("child process %d end" % i)

if __name__ == "__main__":
    print("main process start")
    func()
    print("main process end")
