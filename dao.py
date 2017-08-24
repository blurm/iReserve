#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sqlite3


class Dao(object):

    """Dao to access database"""

    def __init__(self, test):
        if test:
            self.conn = sqlite3.connect("/home/damon/iphoneRevTest.db")
        else:
            self.conn = sqlite3.connect("/home/damon/iphoneRev.db")
        print("conn has been opened")

    def __del__(self):
        self.conn.close()
        print("conn has been closed")

    __GET_CLIENTINFOS = "select * from clientInfo where isActive=1"
    __GET_STORES = "select * from store"
    __GET_MODELS = "select * from model"
    __GET_CLIENTINFO = "select * from clientInfo where oid=?"
    __GET_STORE = "select storeName,area,areaName from store where \
            storeId=?"
    __GET_STORES_BY_AREA = "select storeId,storeName,areaName \
            from store where area=?"
    __GET_MODEL = "select modelName from model where modelId=?"
    __INSERT_APPLOG = "insert into applog (area,storeName,modelName,appleId,\
            fengId,sleepTime,totalTime,error,timestamp) \
            values(?,?,?,?,?,?,?,?,?)"
    __INACTIVE_CLIENTINFO = "update clientInfo set isactive=0 where oid=?"
    __GET_RCODE = "select * from rcode where phoneNumber=? and appleId=?"
    __INSERT_RCODE = "insert into rcode (rcode, phoneNumber, appleId, \
            timestamp) values(?,?,?,?)"
    __UPDATE_RCODE = "update rcode set rcode=?, timestamp=? where phoneNumber=? and \
            appleId=?"
    __GET_CELLPHONEINFO = "select * from cellphoneInfo where phoneNumber=?"
    __UPDATE_CELLPHONEINFO = "update cellphoneInfo set todayCount=?, \
            availCount=? where phoneNumber=?"

    def getClientInfos(self):
        return self.__getDomains(Dao.__GET_CLIENTINFOS)

    def getStores(self):
        return self.__getDomains(Dao.__GET_STORES)

    def getModels(self):
        return self.__getDomains(Dao.__GET_MODELS)

    def getClientInfo(self, oid):
        cursor = self.conn.cursor()
        try:
            cursor.execute(Dao.__GET_CLIENTINFO, (oid,))
            result = cursor.fetchone()
        except Exception as e:
            raise e
        finally:
            cursor.close()
        return result

    def getStore(self, storeId):
        cursor = self.conn.cursor()
        try:
            cursor.execute(Dao.__GET_STORE, (storeId,))
            result = cursor.fetchall()
        except Exception as e:
            raise e
        finally:
            cursor.close()
        return result[0]

    def getStoresByArea(self, area):
        cursor = self.conn.cursor()
        try:
            cursor.execute(Dao.__GET_STORES_BY_AREA, (area,))
            result = cursor.fetchall()
        except Exception as e:
            raise e
        finally:
            cursor.close()
        return result

    def getModel(self, modelId):
        cursor = self.conn.cursor()
        try:
            cursor.execute(Dao.__GET_MODEL, (modelId))
            result = cursor.fetchall()
        except Exception as e:
            raise e
        finally:
            cursor.close()
        return result[0]

    def setApplog(self, logDict):
        cursor = self.conn.cursor()
        try:
            cursor.execute(Dao.__INSERT_APPLOG, (
                logDict["area"],
                logDict["storeName"],
                logDict["modelName"],
                logDict["appleId"],
                logDict["fengId"],
                logDict["sleepTime"],
                logDict["totalTime"],
                logDict["error"],
                logDict["timestamp"]
            )
            )
        except Exception as e:
            raise e
        finally:
            cursor.close()
            self.conn.commit()

    def inactiveClientInfo(self, oid):
        cursor = self.conn.cursor()
        try:
            cursor.execute(Dao.__INACTIVE_CLIENTINFO, (oid,))
        except Exception as e:
            raise e
        finally:
            cursor.close()
            self.conn.commit()

    def getRCode(self, phoneNumber, appleId):
        cursor = self.conn.cursor()
        try:
            cursor.execute(Dao.__GET_RCODE, (phoneNumber, appleId))
            result = cursor.fetchall()
        except Exception as e:
            raise e
        finally:
            cursor.close()
        return result

    def insertOrUpdateRCode(self, rCode, phoneNumber, appleId, time):
        cursor = self.conn.cursor()
        try:
            cursor.execute(Dao.__GET_RCODE, (phoneNumber, appleId))
            result = cursor.fetchall()
            if not result:
                cursor.execute(Dao.__INSERT_RCODE, (
                    rCode,
                    phoneNumber,
                    appleId,
                    time,
                )
                )
            else:
                cursor.execute(Dao.__UPDATE_RCODE, (
                    rCode,
                    time,
                    phoneNumber,
                    appleId,
                )
                )
        except Exception as e:
            raise e
        finally:
            cursor.close()
            self.conn.commit()

    def getCellphoneInfo(self, phoneNumber):
        cursor = self.conn.cursor()
        try:
            cursor.execute(Dao.__GET_CELLPHONEINFO, (phoneNumber,))
            result = cursor.fetchall()
        except Exception as e:
            raise e
        finally:
            cursor.close()
        return result[0]

    def updateCellphoneInfo(self, phoneNumber, todayCount, availCount):
        cursor = self.conn.cursor()
        try:
            cursor.execute(Dao.__UPDATE_CELLPHONEINFO, (
                todayCount,
                availCount,
                phoneNumber,
            )
            )
        except Exception as e:
            raise e
        finally:
            cursor.close()
            self.conn.commit()


    def __getDomains(self, sql):
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
        except Exception as e:
            raise e
        finally:
            cursor.close()
        return result


def test():
    dao = Dao(True)
    c = dao.getClientInfo(1)
    cs = dao.getClientInfos()
    clientInfo = {
                "fengId": c[1],
                "appleId": c[2],
                "pwd": c[3],
                "govidType": c[4],
                "govid": c[5],
                "area": c[6],
                "models": c[7],
            }

    print(clientInfo)
    print(cs)

# test()
