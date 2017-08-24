#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import urlparse
import json
from pprint import pprint
import datetime
import time

import smsmode
import configHelper

test = configHelper.readMode('test')
# If it is a working day.
nightMode = configHelper.readMode('nightMode')
partNumber = ""
session = requests.Session()

# ==================== Step 1 : select your model ============================
def stepModelSel(url):
    print("========================= Step 1 : select your model =========================")
    print("------------------------- Step 1.1 select your model and submit -------------------------"), '\n'

    # Modify request headers
    headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, sdch, br",
                "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests":1,
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/52.0.2743.116 Chrome/52.0.2743.116 Safari/537.36"
            }

    session.headers = headers
    r = session.get(url,allow_redirects=True)
    print (r.url), '\n'

    return r.url

# ================== Step 2 : login submit ================================
def stepSignin(url, clientDict):
    print("========================= Step 2 : login submit =========================")

    redirectedLoginURL = url

    print (" -------------- Step 2.2 display iframe login widget -----------")
    iframeURL = "https://signin.apple.com/appleauth/auth/signin?widgetKey=40692a3a849499c31657eac1ec8123aa&language=CN-ZH"

    r = session.get(iframeURL, allow_redirects=True)

    print (" -------------- Step 2.3 OMG!!! LOGIN!!!!! --------------")
    fdsBrowserData = {
                "U":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/52.0.2743.116 Chrome/52.0.2743.116 Safari/537.36",
                "L":"en-US",
                "Z":"GMT+08:00",
                "V":"1.1",
                "F":"NOa44j1e3NlY5BSo9z4ofjb75PaK4Vpjt4U_98uszHVyVxFAk.lzXJJIneGffLMC7EZ3QHPBirTYKUowRslz8eibjVdxljQlpQJuYY9hte_1an92r5xj6KksmfTPdFdgmVxf7_OLgiPFMJhHFW_jftckkCoqAkCoq4ly_0x0uVMV0jftckcKyAd65hz7fwdGEM6uJ6o6e0T.5EwHXXTSHCSPmtd0wVYPIG_qvoPfybYb5EtCKoxw4EiCvTDfPbJROKjCJcJqOFTsrhsui65KQnK94CaJ6hO3f9p_nH1zDz.ICMpwoNQuyPBDjaY2ftckuyPB884akHGOg429OML3ogELKKyhk6Hb9LarUqUdHz16rgPtFSL1kaNidKgSve2U.6elV2pNA1RJtG.5vyfy6gzI2wHCSFQ_0pNA1OWX3NqhyA_r_LwwKdBvpZfWfUXtStKjE4PIDzp9hyr1BNlrAp5BNlan0Os5Apw.7V1"
            }

    loginURL = "https://signin.apple.com/appleauth/auth/signin"

    # Refresh the headers
    session.headers = {
                "Accept":"application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding":"gzip, deflate, br",
                "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4",
                "Connection":"keep-alive",
                "Content-Type":"application/json",
                # "Host":"signin.apple.com",
                # "Origin":"https://signin.apple.com",
                "Referer": "https://signin.apple.com/appleauth/auth/signin?widgetKey=40692a3a849499c31657eac1ec8123aa&language=CN-ZH",
                "X-Apple-App-Id":"942",
                "X-Apple-I-FD-Client-Info":fdsBrowserData,
                "X-Apple-Locale":"CN-ZH",
                "X-Apple-Widget-Key":"40692a3a849499c31657eac1ec8123aa",
                "X-Requested-With":"XMLHttpRequest",
            }
    # session.headers['Cookie'] = {"Cookie": getCookieStr(session.cookies)}
    payload = {"accountName":clientDict["appleId"],"password":clientDict["pwd"],"rememberMe":False}

    r = session.post(loginURL, json=payload)

    print (" -------------- Step 2.4 Submit main login form --------------")
    mainFormURL = "https://signin.apple.com/IDMSWebAuth/signin"

    headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4",
                "Connection": "keep-alive",
                "Cache-Control":"max-age=0",
                "Content-Type":"application/x-www-form-urlencoded",
                "Upgrade-Insecure-Requests":1,
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/52.0.2743.116 Chrome/52.0.2743.116 Safari/537.36"
            }

    rs = urlparse.urlparse(redirectedLoginURL)
    q = urlparse.parse_qs(rs.query)

    data = {
                "rememberMe": False,
                "appIdKey": q["appIdKey"],
                "language": q["language"],
                "path": q["path"],
                "oAuthToken": "",
                "rv": q["rv"]
            }

    r = session.post(mainFormURL, data=data, headers=headers)
    print 'main login form redirect '+ r.url, '\n'

    return r.url

# ================== Step 3 : Registration Code ========================
def stepRCode(url):
    print("========================= Step 3 : Registration Code =========================")
    
    print ('---------- step 3.1 Request SMS JSON  ------------------')
    rCodeURL = url + "&ajaxSource=true&_eventId=context"
    print rCodeURL, '\n'

    session.headers = {
                "Accept":"application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding":"gzip, deflate, br",
                "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4",
                "Connection":"keep-alive",
                "Content-Type":"application/json",
                "X-Requested-With":"XMLHttpRequest",
            }

    print ("request URL: " + rCodeURL), '\n'
    r = session.get(rCodeURL)

    print '--------[SMS JSON RESULT]---' + r.text + '---------------'

    print ('---------- step 3.2 Send SMS & get RCode ------------'), '\n'
    rCode = ""
    # If smscode is already sended
    print (json.loads(r.text)), '\n'

    rcDict = json.loads(r.text)

    smsCode = rcDict['keyword']
    print 'SMS Code: ' + rcDict['keyword']
    global partNumber
    partNumber = rcDict['selectedPartNumber']
    p_ie = rcDict["p_ie"]
    flowExecutionKey = rcDict['_flowExecutionKey']
    firstTime = rcDict['firstTime']

    if firstTime:
        autosms = configHelper.readMode('autosms')
        if not test or autosms:
            CMPhoneNumber = configHelper.readCMPhoneNumber(test)
            # rCode = "new code"
            rCode = smsmode.getResrictionCode(CMPhoneNumber, smsCode)
        else:
            # Manually input rcode
            rCode = raw_input("please input registration code:")
        configHelper.writeRCode(rCode)
    else:
        # Last rCode is still available
        rCode = configHelper.readRCode()

    print rCode

    headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, sdch, br",
                "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4",
                "Connection": "keep-alive",
                "Content-Type":"application/x-www-form-urlencoded",
                # "Host":"reserve-cn.apple.com",
                # "Referer":"https://reserve.cdn-apple.com/CN/zh_CN/reserve/iPhone/availability?channel=1",
                "Upgrade-Insecure-Requests":1,
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/52.0.2743.116 Chrome/52.0.2743.116 Safari/537.36"
            }

    phoneNumber = configHelper.readPhoneNumber(test)
    data = {
                "phoneNumber":phoneNumber,
                "selectedCountryCode":86,
                "registrationCode":rCode,
                "submit":"",
                "_flowExecutionKey":flowExecutionKey,
                "_eventId":"next",
                "p_ie":p_ie,
                "dims":""
            }

    session.headers = headers
    print ("request URL: " + url), '\n'
    r = session.post(url, data=data)
    print (r.url), '\n'
    return r.url

# --------------- Step 4 : Select timeslot ------------------------
def stepTimeSlot(url, govid, govidType):
    print (" ------------------ Step 4.1 Select TimeSlots --------------------"), '\n'
    timeSlotURL = url + "&ajaxSource=true&_eventId=context&dims="
    print ("request URL:  " + timeSlotURL)
    session.headers = {
                "Accept":"application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding":"gzip, deflate, br",
                "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4",
                "Connection":"keep-alive",
                "Content-Type":"application/json",
                "X-Requested-With":"XMLHttpRequest",
            }
    r = session.get(timeSlotURL)
    exportHTTPInfo(session, r)
    print '--------[timeslots JSON RESULT]---' + r.text + '---------------', '\n'

    reserveDict = json.loads(r.text)

    # Finde the right time
    # get current hour
    timeslots = reserveDict["timeslots"]

    curHour = datetime.datetime.now().hour
    selectedId = ""
    selectedTime = ""
    # for timeslot in timeslots:
    for i, option in enumerate(timeslots):
        text = option['formattedTime']
        curId = option['timeSlotId']
        # Format : 下午 1:30 - 下午 2:00
        arr = text.split(" ")
        hour = int(arr[1].split(":")[0])
        # format hour to 24 hours
        if arr[0] == u"下午" and hour < 12:
            hour += 12;

        if nightMode and curHour < 18:
            if hour >= 20:
                selectedId = curId
                selectedTime = text
                break
        else:
            if hour >= curHour + 2:
                selectedId = curId
                selectedTime = text
                break

        if i == len(timeslots) - 1:
            selectedId = curId
            selectedTime = text

    print (selectedId)
    print (selectedTime), '\n'
    # print (timeslots)

    print ("-------------- Step 4.2 Submit Reserve -----------------------"), '\n'
    data = {
                "selectedStoreNumber":reserveDict['selectedStoreNumber'],
                "selectedPartNumber":partNumber,
                "selectedContractType":"UNLOCKED",
                "selectedQuantity":"2",
                "selectedTimeSlotId":selectedId,
                "lastName":reserveDict["lastName"],
                "firstName":reserveDict["firstName"],
                "email":reserveDict["email"],
                "selectedGovtIdType":govidType,
                "govtId":govid,
                "p_ie":reserveDict["p_ie"],
                "_flowExecutionKey":reserveDict["_flowExecutionKey"],
                "_eventId":"next",
                "submit":"",
            }

    headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, sdch, br",
                "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4",
                "Connection": "keep-alive",
                "Content-Type":"application/x-www-form-urlencoded",
                # "Host":"reserve-cn.apple.com",
                # "Referer":"https://reserve.cdn-apple.com/CN/zh_CN/reserve/iPhone/availability?channel=1",
                "Upgrade-Insecure-Requests":1,
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/52.0.2743.116 Chrome/52.0.2743.116 Safari/537.36"
            }
    
    print (data), '\n'
    session.headers = headers
    print ("request URL: " + url), '\n'

    sleeptime = configHelper.readConfig('submitTimeSleep')
    print ("current time sleep is : " + str(sleeptime))
    time.sleep(sleeptime)
    r = session.post(url, data=data)

    r = session.get(r.url)

    url = r.url + "&ajaxSource=true&_eventId=context&dims="
    print ("request URL:  " + url ), '\n'
    session.headers = {
                "Accept":"application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding":"gzip, deflate, br",
                "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4",
                "Connection":"keep-alive",
                "Content-Type":"application/json",
                # "Host":"signin.apple.com",
                # "Origin":"https://signin.apple.com",
                "X-Requested-With":"XMLHttpRequest",
            }
    r = session.get(url)
    print '--------[Sumit Error JSON RESULT]---' + r.text + '---------------', '\n'
    rcDict = json.loads(r.text)
    return rcDict.get("errors", "")

# --------------- Step 5 : Submit reservation ------------------------
def format(d, tab=0):
    s = ['{\n']
    for k,v in d.items():
        if isinstance(v, dict):
            v = format(v, tab+1)
        else:
            v = repr(v)

        s.append('%s%r: %s,\n' % ('  '*tab, k, v))
    s.append('}')
    return ''.join(s)

def exportHTTPInfo(session, r=None, fileName=None):
    print ("-------------- http code : %s -----------------" % r.status_code)
    print ("-------------- request headers -----------------")
    print (format(session.headers,tab=1))

    if (r is not None):
        # print ("-------------- history url -----------------")
        # if r.history:
            # print "Request was redirected"
            # for resp in r.history:
                # print resp.status_code, resp.url
            # print "Final destination:"
            # print r.status_code, r.url
        # else:
            # print "Request was not redirected"
        print ("-------------- response headers -----------------")
        print (format(r.headers,tab=1))
        print ("-------------- cookies -----------------")
        print (format(session.cookies,tab=1))
        if fileName is not None:
            f = open(fileName + ".html", 'w')
            f.write(r.text.encode('utf-8'))
            f.close()
    print ('---------------- Final URL ----------------------')
    print (r.url)

def getCookieStr(cookies):
    cookieStr = ''
    if cookies is not None:
        for k, v in cookies.items():
            cookieStr += k + '=' + v + ';';
        length = len(cookieStr)
        if length > 0:
            cookieStr = cookieStr[0:(length-1)]
    return cookieStr


def doIt(url, clientDict, test):
    url = stepModelSel(url)
    url = stepSignin(url,clientDict)
    url = stepRCode(url)
    errorList = stepTimeSlot(url, clientDict["govid"], clientDict["govidType"])
    return errorList
