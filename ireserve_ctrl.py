#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import time
import sys
import imp
import requests
import logging
import datetime
import urllib2
import json

import configHelper
import dao
import myutil
from bcolors import bcolors


class IReserveCtrl(object):

    """docstring for IReserveCtrl"""

    def __init__(self):
        self.__test = configHelper.readMode('test')
        # construct logger instance
        self.__logger = self.__getLogger()
        self.__dao = dao.Dao(self.__test)
        self.__models = self.__initModelDict()
        self.__maindict = self.__initClients()

    def storeCheck(self):

        # imp.reload(sys)

        availurl = configHelper.readURL("availURL")
        # response = urllib2.urlopen(availurl)
        # content = response.read()
        # avail_json = json.loads(content)
        headers = myutil.getHTMLHeaders()
        avail_json = requests.get(availurl, headers=headers).json()
        # Apple.com reservation is not available yet
        if len(avail_json) < 1:
            print(bcolors.FAIL + time.strftime('%d, %b %Y %H:%M:%S') +
                    " - Data Unavailable.")
            return

        # 组织好area-model-clients数据结构
        print("--------------- area-model-clients 数据结构 -----------------")
        print(bcolors.OKBLUE + myutil.format_dict(self.__maindict))

        # 遍历area-model-clients数据结构
        for areaId, areaDict in self.__maindict.items():
            stores = self.__dao.getStoresByArea(areaId)
            # 对于每一个地区的所有店铺遍历
            for item in stores:
                storeId = item[0]
                storeName = item[1]
                areaName = item[2]

                storeStr = storeName + ", " + areaName + ", " + storeId
                print(bcolors.OKGREEN + storeStr)

                # 过滤出当前店铺所有产品
                allModels = avail_json.get(storeId)
                for modelId in allModels:
                    # 如果当前产品id在顾客选择的产品范围之内，并且有库存的话
                    if modelId in areaDict and allModels[modelId] == "ALL":
                        reserve_info = {
                            "modelId": modelId,
                            "storeId": storeId,
                            "clientInfo": areaDict[modelId][0],
                            "areaId": areaId,
                            "storeStr": storeStr,
                        }
                        clientInfo = areaDict[modelId][0]
                        applog_info = {
                            "storeName": storeName,
                            "areaName": areaName,
                            "modelName": self.__models[modelId],
                            "fengId": clientInfo["fengId"],
                            "appleId": clientInfo["appleId"],
                        }
                        return reserve_info, applog_info

                print(bcolors.FAIL + "Nothing Available\n")
        print(bcolors.OKBLUE + "Updated: " +
              time.strftime('%d, %b %Y %H:%M:%S') + "\n")

    def do_reserve(self, areaId, storeId, modelId, clientInfo, storeStr):
        # Get initial request URL
        modelSelectURL = configHelper.readURL("modelSelectURL")
        url = modelSelectURL + "&partNumber=" + modelId + "&store=" + storeId
        if not self.__test:
            print(bcolors.OKGREEN + modelId + " - " +
                  self.__models[modelId])
            self.__logger.info(modelId + "   -   " + self.__models[modelId] +
                               "   -   " + storeStr)
            os.system('espeak "Congratulations!"')

        print(u"当前的预约信息： " + areaId + " " + storeId + " " + modelId)
        print (u"客户信息 -- " + myutil.format_dict(clientInfo, tab=1))

        IReserve = myutil.get_class(configHelper.readEngine())
        ir = IReserve()
        errorList = ir.reserve(url, clientInfo, self.__test)

        return errorList

    def write_applog(self, applog_info, error, runtime):
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        applog = {
            "storeName": applog_info["storeName"],
            "area": applog_info["areaName"],
            "modelName": applog_info["modelName"],
            "fengId": applog_info["fengId"],
            "appleId": applog_info["appleId"],
            "error": error,
            "timestamp": timestamp,
            "sleepTime": configHelper.readConfig(
                'submitTimeSleep'),
            "totalTime": runtime,
        }
        self.__dao.setApplog(applog)

    def inactiveClient(self, oid):
        self.__dao.inactiveClientInfo(oid)

    def __initModelDict(self):
        models = self.__dao.getModels()
        modelDict = {}
        for item in models:
            modelDict[item[1]] = item[2]
        return modelDict

    def __getLogger(self):
        logger = logging.getLogger('mylogger')
        logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler('iphoneStock.log')
        fh.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
                        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)

        logger.addHandler(fh)
        return logger

    def __initClients(self):
        clients = self.__dao.getClientInfos()
        mainDict = {}
        for c in clients:
            clientDict = {
                        "oid": c[0],
                        "fengId": c[1],
                        "appleId": c[2],
                        "pwd": c[3],
                        "govidType": c[4],
                        "govid": c[5],
                        "area": c[6],
                        "models": c[7],
                        "quantity": c[8],
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


# def test():
    # o = IReserveCtrl()
    # o.initModelDict()
