#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
该模块用于定时更新验证码。

因为验证码是针对每一个appleId的，换另外的id登录会要求重新获得验证码。
所以对于每一个appleId都新建一个进程来刷新。
"""

import requests
import time
import datetime
import multiprocessing

import configHelper
import myutil
import os
import traceback
from bcolors import bcolors
from dao import Dao
import ireserve_error as errors
from ireserve_http import IReserveHTTP
import ireserve_ctrl


dao = Dao(False)


def main():
    try:
        main_process()
    except Exception:
        os.system('espeak "SMS Exception"')
        traceback.print_exc()


def store_check(areaId):

    """ This is different with ireserve_ctrl.storeCheck.
    No matter which store and whatever the model is, this function will return
    true
    只是为了提供登录用的URL，以方便获取短信验证码。根据appleId所对应的城市，
    任何一家直营店的任何有库存的型号即可生成登录URL。
    :returns: TODO
    """
    availurl = configHelper.readURL("availURL")
    avail_json = requests.get(availurl).json()

    if len(avail_json) < 1:
        # Apple.com reservation is not available yet
        print(bcolors.FAIL + time.strftime('%d, %b %Y %H:%M:%S') +
                " - Data Unavailable.")
        return
    else:
        stores = dao.getStoresByArea(areaId)
        for item in stores:
            storeId = item[0]

            allModels = avail_json.get(storeId)
            for modelId in allModels:
                if allModels[modelId] == "ALL":
                    # 如果有货
                    reserve_info = {
                        "modelId": modelId,
                        "storeId": storeId,
                        "areaId": areaId,
                    }

                    return reserve_info


def main_process():
    """
    为每一个appleId分配新的进程，刷新验证码
    因为Python的thread不具备并发性（当前时间只能有一个线程跑，因为GIL锁的关系）
    所以用了process
    """
    # Get clientInfo from DB. 获取所有待预约的客户信息。
    results = dao.getClientInfos()
    ps = []
    # 该锁用来解决各个进程对gsm modem的争用
    lock = multiprocessing.Lock()
    for c in results:
        clientInfo = {
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

        # TODO
        p = multiprocessing.Process(
                name=clientInfo["appleId"],
                target=sms_update,
                args=(clientInfo, lock))
        print('Child process %s will start.' % clientInfo["appleId"])
        p.start()
        ps.append(p)
        # 因为同一IP登录太快会报错，这里等待1分钟
        time.sleep(60)

    # p.start()和p.join()要分开运行，否则一个进程运行完毕才会开始下一个进程
    for p in ps:
        p.join()
        print('Child process %s end.' % p.name)


def sms_update(clientInfo, lock):
    """
    Support reservation in different city with same appleId. As long as within
    half an hour, the same rcode can be used.Though different processed would
    be created based on records with same appleId in table 'rcode' still the
    same
    支持同一账号不同地区的预约。只要是同一账号验证码半小时内是通用的。
    虽然会根据rcode表中的相同的appleId启动不同的进程，但效果是一样的。
    """
    print("inside sms_update")
    while True:
        # 判断当前客户是否是active的, 如果已经是无效客户则立即退出子进程
        isActive = dao.getClientInfo(clientInfo["oid"])[9]
        if not isActive:
            return

        # 获得上一次更新rcode的时间, 计算出时间差
        phoneNumber = configHelper.readPhoneNumber(False)
        rcodeResult = dao.getRCode(phoneNumber, clientInfo["appleId"])
        if rcodeResult:
            last_time = datetime.datetime.strptime(
                    rcodeResult[0][4], "%Y-%m-%d %H:%M:%S")
            time_diff = round((datetime.datetime.now() - last_time)
                              .total_seconds() / 60, 2)
        else:
            time_diff = 999

        # 如果时间差超过30分钟，则需要更新rcode
        if time_diff >= 30:
            # 获得有效库存信息，用来生成登录URL
            reserve_info = store_check(clientInfo["area"])
            if reserve_info is None:
                print(u"当前区域 %s 已关闭预约" % clientInfo["area"])
                return
            storeId = reserve_info["storeId"]
            modelId = reserve_info["modelId"]

            # Get initial request URL
            modelSelectURL = configHelper.readURL("modelSelectURL")
            url = modelSelectURL + "&partNumber=" + modelId +\
                  "&store=" + storeId

            print (u"客户信息 -- " + myutil.format_dict(clientInfo, tab=1))

            # 获得当天已发短信数目和当天已成功预约数
            cellPhoneInfo = dao.getCellphoneInfo(phoneNumber)
            todayCount = cellPhoneInfo[2] + 1
            availCount = cellPhoneInfo[3]

            # There might be maximum limit for messages per day
            # if todayCount > 100:
                # os.system('espeak "already five messages"')
                # return

            ir = IReserveHTTP()
            rCode = None
            try:
                rCode = ir.get_avail_rcode(url, clientInfo, lock)
            except errors.IReserveLoginError as e:
                os.system('espeak "login or reserve error"')
                traceback.print_exc()
                ctrl = ireserve_ctrl.IReserveCtrl()
                ctrl.inactiveClient(clientInfo["oid"])
            except errors.IReserveLoginFastError as e:
                os.system('espeak "login too fast"')
                traceback.print_exc()
                print("sleeping 10 minutes")
                time.sleep(10 * 60)
            except errors.IReserveSMSError as e:
                os.system('espeak "phone number error"')
                raise e
            except errors.ISMSTimeoutError as e:
                os.system('espeak "SMS timeout"')
                traceback.print_exc()
                time.sleep(configHelper.readConfig("loginsleep"))

            if rCode:
                curTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                dao.insertOrUpdateRCode(
                        rCode, phoneNumber, clientInfo["appleId"], curTime)
                # 更新对应手机号的信息,其有效预约次数要减一
                dao.updateCellphoneInfo(phoneNumber, todayCount, availCount)

        else:
            sleep_min = 30.00 - time_diff
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            process_name = multiprocessing.current_process().name
            print(" Process[%s] sms_update() sleeping %s minutes..."
                    % (process_name, sleep_min))
            time.sleep(sleep_min * 60)

if __name__ == "__main__":
    main()
