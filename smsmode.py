#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time
import re
from pygsm import GsmModem
import ireserve_error as errors


dev = "/dev/ttyUSB0"


def waiting_response(number, gsm, timeout=60):
    starttime = time.time()
    while True:
        # Check if it runs overtime
        runtime = round(time.time() - starttime)
        if runtime > timeout:
            raise errors.ISMSTimeoutError("recieving message timeout")

        print("Checking for message...")
        msg = gsm.next_message()

        if msg is not None:
                print("Got Message: %r" % (msg))
                print("=== 来自 === " + msg.sender + "===")
                if (msg.sender.find(str(number)) > -1):
                    print("=== " + msg.text + " ====")
                    match = re.search(r'\w*$', msg.text)
                    if match:
                        rcode = match.group()
                        print("=== " + rcode + " ====")
                        return rcode
                    else:
                        print ('match failed')

                    return "failed"

        time.sleep(2)


def sendSMS(gsm, number="18911771857", text="default text"):
    print ("-------" + text + "---------")
    gsm.send_sms(number, text)
    print('send to ', number, text)


def delete_all_sms(gsm):
    lines = gsm.fetch_all_messsages()
    CMGL_MATCHER = re.compile(r'^\+CMGL:.*?$')
    CMGL_NUM_MATCHER = re.compile(r'\+CMGL: (\d{1,2})')
    for line in lines:
        if CMGL_MATCHER.match(line):
            m = CMGL_NUM_MATCHER.match(line)
            num = m.group(1)
            gsm.query("AT+CMGD=%s" % num)


def clear_storage(gsm):

    '''
    Check if the storage is full
    Delete all messages if full
    '''

    out = gsm.query("AT+CPMS=SM")

    m = re.match(r'\+CPMS: (\d{1,2}),(\d{2})', out)
    cur_size = m.group(1)
    max_size = m.group(2)
    print("current messages: %s, maximum size: %s" % (cur_size, max_size))

    if cur_size == max_size:
        # clear the storage, delete all messages
        delete_all_sms(gsm)


def getResrictionCode(number, code):
    print('inside getResrictionCode')
    gsm = GsmModem(port=dev)
    sendSMS(gsm, number, code)
    print("clear storage before recieve message")
    clear_storage(gsm)
    rcode = waiting_response(number, gsm)
    return rcode


if __name__ == "__main__":
    # clear_storage()
    gsm = GsmModem(port=dev)
    delete_all_sms(gsm)
    # gsm.query("AT+CMGD=1")
