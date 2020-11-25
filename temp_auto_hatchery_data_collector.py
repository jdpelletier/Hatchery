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
        t1, t2, t3, p = Util.serRead()
        if t2 or t3 >= 85.0: #TODO get temp value from nick
            Util.pump_on()
            while t2 or t3 > 80.0:
                t1, t2, t3, p = Util.serRead()
            # time.sleep(60)    #TODO get time from nick
            Util.pump_off()
            # t1, t2, t3, p = Util.serRead()
        string = f"{t1} {t2} {t3} {p}"
        Util.FileWrite(path, string)
        time.sleep(288)            # wait 5 minutes
    return


if __name__=='__main__':
    hatchery_data_collector()
