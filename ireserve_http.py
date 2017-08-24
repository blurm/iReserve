#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import urlparse
import json
import datetime
import time

import ireserve
import ireserve_error as errors
import smsmode
import configHelper
import myutil
import dao


class IReserveHTTP(ireserve.IReserve):

    """HTTP request reserving class"""
    signinWidgetURL = configHelper.readURL("signinWidgetURL")
    signinURL = configHelper.readURL("signinURL")
    mainFormURL = configHelper.readURL("mainFormURL")

    def __init__(self):
        super(IReserveHTTP, self).__init__()
        print("IReserveHTTP init")
        self.__session = requests.Session()
        self.__dao = dao.Dao(False)
        print("IReserveHTTP init")

    def __del__(self):
        self.__session.close()
        print("IReserveHTTP deleted")

    def reserve(self, url, clientDict, test):
        print ("IReserveHTTP reserve")
        self.__test = test
        url = self.__stepModelSel(url)
        url = self.__stepSignin(url, clientDict)
        url = self.__stepRCode(url, clientDict["appleId"])
        errorList = self.__stepTimeSlot(
                url, clientDict["govid"], clientDict["govidType"],
                clientDict["quantity"])
        return errorList

    def get_avail_rcode(self, url, clientDict, lock):
        print ("IReserveHTTP SMS udpate")
        url = self.__stepModelSel(url)
        url = self.__stepSignin(url, clientDict)
        with lock:
            rcode = self.__stepRCodeUpdate(url, clientDict["appleId"])
        return rcode

    def __getJSONHeaders(self):
        headers = {
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4",
                    "Connection": "keep-alive",
                    "Content-Type": "application/json",
                    "X-Requested-With": "XMLHttpRequest",
                 }
        return headers

    # ==================== Step 1 : select your model ========================
    def __stepModelSel(self, url):
        print("================= Step 1 : select your model =================")
        print("-------- Step 1.1 select your model and submit ---------"), '\n'

        # Modify request headers
        headers = myutil.getHTMLHeaders()
        self.__session.headers = headers
        r = self.__session.get(url, allow_redirects=True)
        print (r.url), '\n'

        return r.url

    # ================== Step 2 : login submit ================================
    def __stepSignin(self, url, clientDict):
        print("================ Step 2 : login submit =======================")

        redirectedLoginURL = url

        print (" ----------- Step 2.2 display iframe login widget -----------")

        r = self.__session.get(IReserveHTTP.signinWidgetURL,
                               allow_redirects=True)

        print (" -------------- Step 2.3 OMG!!! LOGIN!!!!! --------------")

        # Refresh the headers
        self.__session.headers = self.__getJSONHeaders()
        self.__session.headers.update({
                    "X-Apple-App-Id": "942",
                    "X-Apple-Locale": "CN-ZH",
                    "X-Apple-Widget-Key": "40692a3a849499c31657eac1ec8123aa",
                })

        payload = {"accountName": clientDict["appleId"],
                   "password": clientDict["pwd"], "rememberMe": False}

        r = self.__session.post(IReserveHTTP.signinURL, json=payload)

        print(" ------LOGIN JSON RESULT-----" + r.text)
        error_str = self.__json_errmsg(r.text, "serviceErrors")
        print(error_str)
        if len(error_str) > 0:
            raise errors.IReserveLoginError(error_str)

        print (" -------------- Step 2.4 Submit main login form -------------")

        self.__session.headers = myutil.getHTMLHeaders()
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
        r = self.__session.post(
                IReserveHTTP.mainFormURL,
                data=data)
        print('main login form redirect ' + r.url, '\n')

        return r.url

    # ================== Step 3 : Registration Code ========================
    def __stepRCode(self, url, appleId):
        print("================= Step 3 : Registration Code ================")

        print ('---------- step 3.1 Request SMS JSON  ------------------')
        rCodeURL = url + "&ajaxSource=true&_eventId=context"
        print(rCodeURL, '\n')

        self.__session.headers = self.__getJSONHeaders()
        print ("request URL: " + rCodeURL), '\n'
        r = self.__session.get(rCodeURL)

        print('--------[SMS JSON RESULT]---' + r.text + '---------------')
        if not r.text:
            raise errors.IReserveLoginFastError("登录太快了，请等几秒钟")
        print ('---------- step 3.2 Send SMS & get RCode ------------'), '\n'
        rCode = ""
        # If smscode is already sended
        print (json.loads(r.text)), '\n'

        rcDict = json.loads(r.text)

        smsCode = rcDict['keyword']
        print('SMS Code: ' + rcDict['keyword'])
        print(self.__test)

        p_ie = rcDict["p_ie"]
        flowExecutionKey = rcDict['_flowExecutionKey']
        firstTime = rcDict['firstTime']

        autosms = configHelper.readMode('autosms')
        if not self.__test or autosms:
            phoneNumber = configHelper.readPhoneNumber(False)
        else:
            phoneNumber = configHelper.readPhoneNumber(True)
        print("phone number: " + phoneNumber)

        if firstTime:
            if not self.__test or autosms:
                CMPhoneNumber = configHelper.readCMPhoneNumber(self.__test)
                # rCode = "new code"
                rCode = smsmode.getResrictionCode(CMPhoneNumber, smsCode)
            else:
                # Manually input rcode
                rCode = raw_input("please input registration code:")
            # configHelper.writeRCode(rCode, appleId)
            curTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.__dao.insertOrUpdateRCode(
                    rCode, phoneNumber, appleId, curTime)
        else:
            # Last rCode is still available
            # rCode = configHelper.readRCode()
            rCode = self.__dao.getRCode(phoneNumber, appleId)[0][1]

        print('registration code: ' + rCode)

        self.__session.headers = myutil.getHTMLHeaders()

        data = {
                    "phoneNumber": phoneNumber,
                    "selectedCountryCode": 86,
                    "registrationCode": rCode,
                    "submit": "",
                    "_flowExecutionKey": flowExecutionKey,
                    "_eventId": "next",
                    "p_ie": p_ie,
                    "dims": ""
                }
        print ("request URL: " + url), '\n'
        r = self.__session.post(url, data=data)
        print (r.url), '\n'
        return r.url

    def __stepRCodeUpdate(self, url, appleId):
        print("================= Step 3 : Registration Code ================")

        print ('---------- step 3.1 Request SMS JSON  ------------------')
        rCodeURL = url + "&ajaxSource=true&_eventId=context"
        print(rCodeURL, '\n')

        self.__session.headers = self.__getJSONHeaders()
        print ("request URL: " + rCodeURL), '\n'
        r = self.__session.get(rCodeURL)


        print('--------[SMS JSON RESULT]---' + r.text + '---------------')
        if not r.text:
            raise errors.IReserveLoginFastError("登录太快了，请等几秒钟")
        print ('---------- step 3.2 Send SMS & get RCode ------------'), '\n'
        rCode = ""
        # If smscode is already sended
        print (json.loads(r.text)), '\n'

        rcDict = json.loads(r.text)

        smsCode = rcDict['keyword']
        print('SMS Code: ' + rcDict['keyword'])

        firstTime = rcDict['firstTime']

        if firstTime:
            CMPhoneNumber = configHelper.readCMPhoneNumber(False)
            rCode = smsmode.getResrictionCode(CMPhoneNumber, smsCode)
            # configHelper.writeRCode(rCode, appleId)
            print('registration code: ' + rCode)
            return rCode

    # --------------- Step 4 : Select timeslot ------------------------
    def __stepTimeSlot(self, url, govid, govidType, quantity):
        print ("------------- Step 4.1 Select TimeSlots ---------------"), '\n'
        timeSlotURL = url + "&ajaxSource=true&_eventId=context&dims="
        print ("request URL:  " + timeSlotURL)
        self.__session.headers = self.__getJSONHeaders()
        r = self.__session.get(timeSlotURL)

        print('--------[timeslots JSON RESULT]---' + r.text + '-------', '\n')
        error_str = self.__json_errmsg(r.text, "errors")
        if len(error_str) > 0:
            raise errors.IReserveSMSError(error_str)

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
                hour += 12

            nightMode = configHelper.readMode("nightMode")
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

        print("-------------- Step 4.2 Submit Reserve ---------------"), '\n'
        data = {
                    "selectedStoreNumber": reserveDict['selectedStoreNumber'],
                    # "selectedPartNumber": partNumber,
                    "selectedContractType": "UNLOCKED",
                    "selectedQuantity": quantity,
                    "selectedTimeSlotId": selectedId,
                    "lastName": reserveDict["lastName"],
                    "firstName": reserveDict["firstName"],
                    "email": reserveDict["email"],
                    "selectedGovtIdType": govidType,
                    "govtId": govid,
                    "p_ie": reserveDict["p_ie"],
                    "_flowExecutionKey": reserveDict["_flowExecutionKey"],
                    "_eventId": "next",
                    "submit": "",
                }

        self.__session.headers = myutil.getHTMLHeaders()

        print (data), '\n'
        print ("request URL: " + url), '\n'

        sleeptime = configHelper.readConfig('submitTimeSleep')
        print ("current sleep time is : " + str(sleeptime))
        time.sleep(sleeptime)
        r = self.__session.post(url, data=data)

        r = self.__session.get(r.url)

        url = r.url + "&ajaxSource=true&_eventId=context&dims="
        print("request URL:  " + url), '\n'
        self.__session.headers = self.__getJSONHeaders()
        r = self.__session.get(url)
        print('--------[Sumit Error JSON RESULT]---' + r.text + '-----', '\n')
        error_str = self.__json_errmsg(r.text, "errors")
        if len(error_str) > 0:
            if error_str == "availabilityError":
                raise errors.IReserveAvailError(error_str)
            else:
                raise errors.IReserveReserveError(error_str)

    # --------------- Step 5 : Submit reservation ------------------------
    def __json_errmsg(self, jsonstr, errfield):
        print(jsonstr)
        jsonobj = json.loads(jsonstr)
        error_str = ""
        # If login failed
        if jsonobj.get(errfield):
            for error in jsonobj.get(errfield):
                if errfield == "serviceErrors":
                    error_str += error["message"]
                else:
                    error_str += error
        return error_str

    # TODO
    def __pp_json(json_thing, sort=True, indents=4):
        if type(json_thing) is str:
            print(json.dumps(json.loads(json_thing),
                  sort_keys=sort, indent=indents))
        else:
            print(json.dumps(json_thing, sort_keys=sort, indent=indents))
        return None

    def __getCookieStr(self, cookies):
        cookieStr = ''
        if cookies is not None:
            for k, v in cookies.items():
                cookieStr += k + '=' + v + ';'
            length = len(cookieStr)
            if length > 0:
                cookieStr = cookieStr[0:(length - 1)]
        return cookieStr
