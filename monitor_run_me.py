#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import signal
import traceback
import sys
import imp
import datetime
import requests
import logging

import configHelper
import dao
import myutil

# If it's under test mode
test = configHelper.readMode('test')

logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('iphoneStock.log')
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

fh.setFormatter(formatter)

logger.addHandler(fh)

d = dao.Dao(test)


def signal_handler(signal, frame):
    print(' - Stop Monitoring')
    sys.exit(0)

# Handle Ctrl+C in terminal
signal.signal(signal.SIGINT, signal_handler)
print('Apple Store Monitoring \n')


def getModelName(k):

    # Incase of a new version, update models here.
    model_mapping = {
        "MNH22CH/A": "iPhone 7 Jet Black - 128 GB",
        "MNH72CH/A": "iPhone 7 Jet Black - 256 GB",
        "MNGQ2CH/A": "iPhone 7 Black - 32 GB",
        "MNGX2CH/A": "iPhone 7 Black - 128 GB",
        "MNH32CH/A": "iPhone 7 Black - 256 GB",
        "MNGT2CH/A": "iPhone 7 Gold - 32 GB",
        "MNH02CH/A": "iPhone 7 Gold - 128 GB",
        "MNH52CH/A": "iPhone 7 Gold - 256 GB",
        "MNGW2CH/A": "iPhone 7 Rose Gold - 32 GB",
        "MNH12CH/A": "iPhone 7 Rose Gold - 128 GB",
        "MNH62CH/A": "iPhone 7 Rose Gold - 256 GB",
        "MNGR2CH/A": "iPhone 7 Silver - 32 GB",
        "MNGY2CH/A": "iPhone 7 Silver - 128 GB",
        "MNH42CH/A": "iPhone 7 Silver - 256 GB",
        "MNFU2CH/A": "iPhone 7 Plus Jet Black - 128 GB",
        "MNG02CH/A": "iPhone 7 Plus Jet Black - 256 GB",
        "MNRJ2CH/A": "iPhone 7 Plus Black - 32 GB",
        "MNFP2CH/A": "iPhone 7 Plus Black - 128 GB",
        "MNFV2CH/A": "iPhone 7 Plus Black - 256 GB",
        "MNRM2CH/A": "iPhone 7 Plus Rose Gold - 32 GB",
        "MNFT2CH/A": "iPhone 7 Plus Rose Gold- 128 GB",
        "MNFY2CH/A": "iPhone 7 Plus Rose Gold - 256 GB",
        "MNRL2CH/A": "iPhone 7 Plus Gold - 32 GB",
        "MNFR2CH/A": "iPhone 7 Plus Gold - 128 GB",
        "MNFX2CH/A": "iPhone 7 Plus Gold - 256 GB",
        "MNRK2CH/A": "iPhone 7 Plus Silver - 32 GB",
        "MNFQ2CH/A": "iPhone 7 Plus Silver - 128 GB",
        "MNFW2CH/A": "iPhone 7 Plus Silver - 256 GB",
        "timeSlot": ""
    }

    model_name = model_mapping.get(k)
    # print(model_name)
    if(len(model_name) <= 0):
        model_name = k

    return bcolors.OKGREEN + model_name


def initClients(clients):
    mainDict = {}
    for c in clients:
        clientDict = {
                    "fengId": c[1],
                    "appleId": c[2],
                    "pwd": c[3],
                    "govidType": c[4],
                    "govid": c[5],
                    "area": c[6],
                    "models": c[7],
                }

        area = clientDict["area"]

        if mainDict.get(area) is None:
            areaDict = {}
            mainDict[area] = areaDict
        else:
            areaDict = mainDict[area]

        models = clientDict["models"]
        modelArr = models.split(",")
        for model in modelArr:
            if areaDict.get(model) is None:
                areaDict[model] = [clientDict]
            else:
                areaDict[model].append(clientDict)

    return mainDict


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\0330m'


def storeCheck():
    starttime = time.time()
    # imp.reload(sys)

    # https://reserve.cdn-apple.com/HK/zh_HK/reserve/iPhone/availability.json
    # https://reserve.cdn-apple.com/HK/zh_HK/reserve/iPhone/stores.json

    availurl = "https://reserve.cdn-apple.com/CN/zh_CN/reserve/iPhone/availability.json"
    avail_json = requests.get(availurl).json()
    if len(avail_json) < 1:
        print(bcolors.FAIL + time.strftime('%d, %b %Y %H:%M:%S') +
                " - Data Unavailable.")
        return

    # Fetch all clientInfos from DB
    clients = d.getClientInfos()

    # 组织好数据结构
    mainDict = initClients(clients)
    print(mainDict)
    modelSelectURL = "https://reserve-cn.apple.com/CN/zh_CN/reserve/iPhone?channel=1&rv=&path=&sourceID=&iPP=false&appleCare=&iUID=&iuToken=&carrier="

    # 遍历数据结构
    for areaId, areaDict in mainDict.items():
        stores = d.getStoresByArea(areaId)
        # 对于每一个地区的所有店铺遍历
        for item in stores:
            storeId = item[0]
            storeName = item[1]
            areaName = item[2]

            storeStr = bcolors.OKGREEN + storeName + ", " + areaName + ", " + storeId
            print(storeStr)

            hasAvailModel = False
            # 过滤出当前店铺所有有库存的产品
            allModels = avail_json.get(storeId)
            for modelId in allModels:
                # 如果当前产品id在顾客选择的产品范围之内，并且有库存的话
                # 如果是测试模式，则不过滤
                if modelId in areaDict and allModels[modelId] == "ALL":
                    hasAvailModel = True
                    # Get model name from DB
                    # Create a new thread to open URL in browser
                    url = modelSelectURL + "&partNumber=" + modelId +\
                        "&store=" + storeId
                    if not test:
                        print(bcolors.OKGREEN + modelId + " - " +
                                getModelName(modelId))
                        logger.info(modelId + "   -   " + getModelName(modelId) +
                                "   -   " + storeStr)
                        os.system('espeak "Congratulations!"')

                    print(areaId + storeId + modelId)
                    clientInfo = areaDict[modelId][0]

                    print ("clientInfo --", clientInfo)

                    IReserve = myutil.get_class(configHelper.readEngine())
                    ir = IReserve()
                    errorList = ir.reserve(url, clientInfo, test)
                    # errorList = requestTest2.doIt()
                    # requestWithSelenium.doIt(url, clientInfo, test)

                    # Create applog record
                    error = ""
                    for errItem in errorList:
                        error += errItem

                    runtime = str(round(time.time()-starttime, 2))
                    print('运行时间' + runtime)

                    now = datetime.datetime.now()
                    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
                    applog = {
                            "storeName": storeName,
                            "area": areaName,
                            "modelName": getModelName(modelId),
                            "fengId": clientInfo["fengId"],
                            "appleId": clientInfo["appleId"],
                            "error": error,
                            "timestamp": timestamp,
                            "sleepTime": configHelper.readConfig(
                                'submitTimeSleep'),
                            "totalTime": runtime,
                            }
                    d.setApplog(applog)

                    time.sleep(60)
                    return

            if not hasAvailModel:
                print(bcolors.FAIL + "Nothing Available\n")

    print(bcolors.OKBLUE + "Updated: " + time.strftime('%d, %b %Y %H:%M:%S') +
        "\n")

    return

try:
    while True:
        storeCheck()
        time.sleep(5)
except Exception as e:
    os.system('espeak "Exception"')
    traceback.print_exc()
