import time
import datetime
import smtplib
from email.message import EmailMessage

import Util

def hatchery_data_collector():
    # Read and record the data
    currentDay = datetime.date.today()
    path = Util.FolderCreate(currentDay)
    while(True):
        Util.pump_off(1)
        Util.pump_off(2)
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
        if (t2 == 185.0 or t3 == 185.0) and (Util.auto_check()): #check for broken sensor
            Util.auto_file_write('off')
            msg = EmailMessage()
            content = """Warning: A sensor is not reading correctly.
            The automated temperature adjustment has been shutoff."""
            msg.set_content(content)
            msg['Subject'] = 'ATTENTION: Sensor Problem'
            msg['From'] = "njordan@kohanakai.com"
            msg['To'] = ['john.pelletier@ymail.com', 'njordan@kohanakai.com']
            s = smtplib.SMTP('smtp-relay.gmail.com', 25)
            s.send_message(msg)
            s.quit()
        if (t2 > 85.0 or t3 > 85.0) and (Util.auto_check()):
            while (t2 > 80.0 or t3 > 80.0) and (Util.auto_check()):
                if t2 > 80.0 and t3 > 80.0:
                    Util.pump_on(3)
                    time.sleep(288)
                    Util.pump_off(3)
                elif t2 > 80.0 and t3 < 80.0:
                    Util.pump_on(1)
                    time.sleep(288)
                    Util.pump_off(1)
                elif t2 < 80.0 and t3 > 80.0:
                    Util.pump_on(2)
                    time.sleep(288)
                    Util.pump_off(2)
                t1, t2, t3, p = Util.serRead()
                string = f"{t1} {t2} {t3} {p}"
                Util.FileWrite(path, string)
        else:
            time.sleep(288)            # wait 5 minutes
    return


if __name__=='__main__':
    hatchery_data_collector()
