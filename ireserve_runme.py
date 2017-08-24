#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import signal
import traceback
import sys

import configHelper
import ireserve_ctrl
import ireserve_error as errors


def main():
    # Avoid the 'too many open files' exception
    os.system('ulimit -n 10000')

    def signal_handler(signal, frame):
        print(' - Stop Monitoring')
        sys.exit(0)

    # Handle Ctrl+C in terminal
    signal.signal(signal.SIGINT, signal_handler)
    print('Apple Store Monitoring \n')

    # Calculate program execution time
    starttime = time.time()

    ctrl = ireserve_ctrl.IReserveCtrl()
    # Check stock and get available model info
    values = ctrl.storeCheck()
    # If stock is available
    if values:
        reserve_info, applog_info = values

        error = ""
        try:
            # Reservation
            ctrl.do_reserve(reserve_info["areaId"],
                                            reserve_info["storeId"],
                                            reserve_info["modelId"],
                                            reserve_info["clientInfo"],
                                            reserve_info["storeStr"])

        except (errors.IReserveLoginError, errors.IReserveReserveError) as e:
            error = e.message
            os.system('espeak "login or reserve error"')
            traceback.print_exc()
            # TODO remove current client from maindict
            ctrl.inactiveClient(reserve_info["clientInfo"]["oid"])
        except errors.IReserveLoginFastError as e:
            error = e.message
            os.system('espeak "login too fast"')
            traceback.print_exc()
            time.sleep(configHelper.readConfig("loginsleep"))
        except errors.IReserveSMSError as e:
            os.system('espeak "phone number error"')
            error = e.message
            raise e
        except errors.IReserveAvailError as e:
            os.system('espeak "availability error"')
            error = e.message
            traceback.print_exc()
        except errors.ISMSTimeoutError as e:
            os.system('espeak "SMS timeout"')
            traceback.print_exc()
            time.sleep(configHelper.readConfig("loginsleep"))
        else:
            os.system('espeak "successfully reserved"')
            error = "success"
            ctrl.inactiveClient(reserve_info["clientInfo"]["oid"])
        finally:
            runtime = str(round(time.time() - starttime, 2))
            print('运行时间' + runtime)

            ctrl.write_applog(applog_info, error, runtime)

            time.sleep(2)


try:
    while True:
        main()
        time.sleep(5)
except Exception as e:
    os.system('espeak "Exception"')
    traceback.print_exc()
