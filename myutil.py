#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configHelper


def getHTMLHeaders():
    headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;\
                        q=0.9,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, sdch, br",
                "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": 1,
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/\
                    537.36 (KHTML, like Gecko) Ubuntu Chromium/\
                    52.0.2743.116 Chrome/52.0.2743.116 Safari/537.36"
            }
    return headers


def exportHTTPInfo(session, r=None, fileName=None):
    print("----------- http code : %s -----------------" % r.status_code)
    print("-------------- request headers -----------------")
    print(format_dict(session.headers, tab=1))

    if (r is not None):
        print ("-------------- response headers -----------------")
        print (format_dict(r.headers, tab=1))
        print ("-------------- cookies -----------------")
        print (format_dict(session.cookies, tab=1))
        if fileName is not None:
            f = open(fileName + ".html", 'w')
            f.write(r.text.encode('utf-8'))
            f.close()
    print ('---------------- Final URL ----------------------')
    print (r.url)


def get_class(name):
    parts = name.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m


def format_dict(d, tab=0):
    s = ['{\n']
    for k, v in d.items():
        if isinstance(v, dict):
            v = format_dict(v, tab + 1)
        else:
            v = repr(v)

        s.append('%s%r: %s,\n' % ('  ' * tab, k, v))
    s.append('}')
    return ''.join(s)


def test():
    IReserve = get_class(configHelper.readEngine())
    ir = IReserve()
    ir.reserve()


if __name__ == "__main__":
    test()
