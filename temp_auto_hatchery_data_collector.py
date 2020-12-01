import time
import datetime

import Util

def hatchery_data_collector():
    # Read and record the data
    currentDay = datetime.date.today()
    path = Util.FolderCreate(currentDay)
    while(True):
        if currentDay != datetime.date.today():
            currentDay = datetime.date.today()
            path = Util.FolderCreate(currentDay)
        #Taking average of 10 measurements
        pumprunning = Util.pump_check()
        t1, t2, t3, p = Util.serRead()
        if pumprunning == True: #if pump was on before read, cycle it back on after
            pumprunning = Util.pump_off()
            pumprunning = Util.pump_on()
        if t2 or t3 > 78:
            while t2 or t3 > 75:
                Util.pump_on()
                time.sleep(120)
                Util.pump_off()
                t1, t2, t3, p = Util.serRead()
        string = f"{t1} {t2} {t3} {p}"
        Util.FileWrite(path, string)
        time.sleep(288)            # wait 5 minutes
    return


if __name__=='__main__':
    hatchery_data_collector()
