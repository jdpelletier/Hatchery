import time
import datetime

import Util

def hatchery_data_collector():
    # Read and record the data
    currentDay = datetime.date.today()
    path = Util.FolderCreate(currentDay)
    Util.pump_off(1)
    Util.pump_off(2)
    while(True):
        if currentDay != datetime.date.today():
            currentDay = datetime.date.today()
            path = Util.FolderCreate(currentDay)
        #Taking average of 10 measurements
        pumprunning1 = Util.pump_check(1)
        pumprunning2 = Util.pump_check(2)
        t1, t2, t3, p = Util.serRead()
        string = f"{t1} {t2} {t3} {p}"
        Util.FileWrite(path, string)
        if pumprunning1 == True and pumprunning2 == True:
            pumprunning1 = Util.pump_off(3)
            pumprunning1 = Util.pump_on(3)
            pumprunning2 = pumprunning1
        elif pumprunning1 == True: #if pump was on before read, cycle it back on after
            pumprunning1 = Util.pump_off(1)
            pumprunning1 = Util.pump_on(1)
        elif pumprunning2 == True: #if pump was on before read, cycle it back on after
            pumprunning2 = Util.pump_off(2)
            pumprunning2 = Util.pump_on(2)
        if ((t1 > 84.0 and t1 != 185.0) or (t2 > 84.0 and t2 != 185.0)) and Util.auto_check():
            Util.auto_run(t1, t2, path, string)
        time.sleep(288)            # wait 5 minutes
    return


if __name__=='__main__':
    hatchery_data_collector()
