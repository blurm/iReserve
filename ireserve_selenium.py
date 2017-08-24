#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import datetime

import ireserve
import smsmode
import configHelper

# ------------ Global Var --------------------
# Goverment ID number
# govidnumber = "140202198208040104"
# govidnumber = "140202198810090011"
# lastName
# lastName = u"马"
# firstName
# firstName = u"嘉骐"
# email
# email = "blurm@126.com"
# CMPhoneNumber = "18911771857"


class IReserveSelenium(ireserve.IReserve):

    """HTTP request reserving class"""
    # signinWidgetURL = configHelper.readURL("signinWidgetURL")
    # signinURL = configHelper.readURL("signinURL")
    # mainFormURL = configHelper.readURL("mainFormURL")

    def __init__(self):
        # self.__session = requests.Session()
        print("IReserveSelenium init")

    def __del__(self):
        # self.__session.close()
        print("IReserveSelenium deleted")

    def reserve(self, url, clientDict, test):
        nightMode = configHelper.readMode("nightMode")
        CMPhoneNumber = configHelper.readCMPhoneNumber(test)

        # driver = webdriver.PhantomJS(executable_path='/usr/bin/phantomjs')
        driver = webdriver.Chrome()

        print("============== Step 1 : select your model ==================")
        driver.get(url)
        print driver.title
        print("================== Step 2 : login submit ===================")
        driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
        try:
            eAppId = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "appleId")))
            eAppId.send_keys(clientDict["appleId"])

            ePwd = driver.find_element_by_id("pwd")
            ePwd.send_keys(clientDict["pwd"])

            eSubmit = driver.find_element_by_id("sign-in")
            eSubmit.click()

            print("================ Step 3 : Registration Code ==============")
            # ----------- Send SMS to get registration code ----------------
            # wait until page refreshed
            # WebDriverWait(driver, 10).until(EC.title_contains("SMS"))

            # smsCode = driver.find_element_by_tag_name("strong");
            # print smsCode

            phoneNumber = configHelper.readPhoneNumber(test)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "phoneNumber"))) \
                    .send_keys(phoneNumber)
            # driver.find_element_by_xpath("//input[@id='phoneNumber']").send_keys(Keys.F12)

            print driver.title
            smsCode = driver.find_element_by_xpath("//div/p/strong").text
            print ("smscode : " + smsCode)
            autosms = configHelper.readMode('autosms')

            if len(smsCode) > 1:
                if not test or autosms:
                    CMPhoneNumber = configHelper.readCMPhoneNumber(test)
                    # rCode = "new code"
                    rCode = smsmode.getResrictionCode(CMPhoneNumber, smsCode)
                else:
                    # Manually input rcode
                    if len(smsCode) < 1:
                        time.sleep(15)
                    else:
                        time.sleep(30)

                configHelper.writeRCode(rCode, clientDict["appleId"])
            else:
                # Last rCode is still available
                rCode = configHelper.readRCode()

            print rCode
            driver.find_element_by_id("registrationcode").send_keys(rCode)


            # if not test or autosms:

                # # if smscode is empty, means last code is still available
                # # need to retrieve it from file
                # if len(smsCode) < 1:
                    # rCode = configHelper.readRCode()
                # else:
                    # # Send SMS and get code
                    # rCode = smsmode.getResrictionCode(CMPhoneNumber, smsCode)
                    # configHelper.writeRCode(rCode)

                # print rCode
                # driver.find_element_by_id("registrationcode").send_keys(rCode)
            # else:
                # if len(smsCode) < 1:
                    # time.sleep(15)
                # else:
                    # time.sleep(30)

            driver.find_element_by_name("submit").click()

            print (" --------- Step 4.1 Select TimeSlots ----------"), '\n'
            # --------- Select timeSlot and reserve --------------------------
            # eTimeSlot = driver.find_element_by_id("time")
            # Don't use find_by_id, there might be multiple elements
            # with same id
            # which will cause error
            # time.sleep(1)
            WebDriverWait(driver, 10).until(EC.title_contains(u"选择时间"))
            print driver.title
            time.sleep(2)
            # eTimeSlot = driver.find_element_by_xpath(
            #         "//div[contains(@class, 'select-store')]/select")
            # quantity = clientDict["quantity"]
            # eQuantity = WebDriverWait(driver, 10).until(
            #         EC.presence_of_element_located((By.ID, "quantity")))
            # time.sleep(1)
            eTimeSlot = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div[contains(@class, 'select-store')]/select[contains(@name, 'selectedTimeSlotId')]")))
            allOptions = eTimeSlot.find_elements_by_tag_name("option")

            # get current hour
            now = datetime.datetime.now()
            curHour = now.hour
            print 'length: ' + str(len(allOptions))
            for i, option in enumerate(allOptions):
                # first option is invalid
                if i == 0:
                    continue
                text = option.get_attribute("text")
                print str(i) + " : " + text

                # Format : 下午 1:30 - 下午 2:00
                arr = text.split(" ")
                hour = int(arr[1].split(":")[0])
                # format hour to 24 hours
                if arr[0] == u"下午" and hour < 12:
                    hour += 12;

                if nightMode and curHour < 18:
                    if hour >= 20:
                        option.click()
                        break
                else:
                    if hour >= curHour + 2:
                        option.click()
                        break

                if i == len(allOptions) - 1:
                    option.click()

            # select:quantity
            # eQuatity = driver.find_element_by_id("quantity")
            # allOptions = eQuatity.find_elements_by_tag_name("option")

            # text:lastName
            # eLastName = WebDriverWait(driver, 10).until(
                    # EC.presence_of_element_located((By.ID, "lastName")))

            # eLastName.clear()
            # eLastName.send_keys(lastName)

            # # text:firstName
            # driver.find_element_by_id("firstName").clear()
            # driver.find_element_by_id("firstName").send_keys(firstName)

            # # text:email
            # driver.find_element_by_id("email").clear()
            # driver.find_element_by_id("email").send_keys(email)

            # select:govid
            # time.sleep(1)
            eGovid = driver.find_element_by_id("govid")
            allOptions = eGovid.find_elements_by_tag_name("option")

            for i, option in enumerate(allOptions):
                if i == 1:
                    # time.sleep(1)
                    option.click()

            # text:govidnumber
            govidnumber = clientDict["govid"]
            driver.find_element_by_id("govidnumber").send_keys(govidnumber)
            print govidnumber

            # button - name:submit
            # if not test:
            driver.find_element_by_name("submit").click()

            time.sleep(90)
            print driver.title

            error = ""
            eError = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH,
                            "//div[contains(@class, 'error-copy')]/h2/span")))
            if eError is not None:
                error = eError.text
                print (eError.text)

            resultList = [error]
            return resultList
        finally:
            driver.close()
