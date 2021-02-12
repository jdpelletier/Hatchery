import os
import time
import datetime
import statistics
import serial
import smtplib
from email.message import EmailMessage

def NowString():
    today = datetime.datetime.now()
    time = today.time().strftime('%H:%M:%S ')
    return time

def FileWrite(filepath, data):
    filename = os.path.join(str(filepath), "dataFile.txt")
    with open(filename, 'a') as f:
        f.write(NowString())
        f.write(data)
        f.write("\n")
        f.close()

def FolderCreate(today):
    todaystr = today.isoformat()

    parent_directory = "/home/pi/Desktop/Hatchery/TestData"
    path = os.path.join(parent_directory, todaystr)
    try:
        os.mkdir(path)
    except OSError:
        print ("The folder %s is already created" % path)
    else:
        print ("Successfully created the directory %s " % path)
    return path

def serRead():
    ser = serial.Serial('/dev/ttyACM0', 9600)
    time.sleep(2)
    i = 0
    values = []
    t1 = []
    t2 = []
    t3 = []
    p = []
    for i in range(10):
        b = ser.readline()         # read a byte string
        try:
            string_n = b.decode()      # decode byte string into Unicode
        except UnicodeDecodeError:
            print("Decode Error")
            continue
        string = string_n.rstrip() # remove \n and \r
        values = string.split()
        if len(values) != 4:
            print("Read Error")
            continue
        if float(values[0]) > 10:
            t1.append(float(values[0]))
        if float(values[1]) > 10:
            t2.append(float(values[1]))
        if float(values[2]) > 10:
            t3.append(float(values[2]))
        p.append(float(values[3]))
        time.sleep(1)
        i += 1
    t1_av = statistics.mean(t1)
    t2_av = statistics.mean(t2)
    t3_av = statistics.mean(t3)
    ph_av = statistics.mean(p)
    ser.close()
    return t1_av, t2_av, t3_av, ph_av


def pump_on(valve):
    try:
        arduino = serial.Serial('/dev/ttyACM0', 9600)
        time.sleep(2)
        if valve == 1:
            arduino.write(b'H')
        elif valve == 2:
            arduino.write(b'I')
        elif valve == 3:
            arduino.write(b'J')
        time.sleep(1)
        arduino.close()
        pump_file_write(valve, 'on')
        return True
    except serial.serialutil.SerialException:
        return False

def pump_off(valve):
    try:
        arduino = serial.Serial('/dev/ttyACM0', 9600)
        time.sleep(2)
        if valve == 1:
            arduino.write(b'K')
        elif valve == 2:
            arduino.write(b'L')
        elif valve == 3:
            arduino.write(b'M')
        time.sleep(1)
        arduino.close()
        pump_file_write(valve, 'off')
        return False
    except serial.serialutil.SerialException:
        return True

def pump_check(valve):
    if valve == 1:
        pfile = 'pumpcheck1.txt'
    else:
        pfile = 'pumpcheck2.txt'
    try:
        with open(pfile, 'r') as f:
            onoff = f.readline()
        if onoff == 'on':
            return True
        else:
            return False
    except FileNotFoundError: #catch on boot up, assume pump off
        return False

def pump_file_write(valve, onoff):
    if valve == 1:
        pfile = 'pumpcheck1.txt'
        with open(pfile, 'w+') as f:
            f.write(onoff)
            f.close()
    elif valve == 2:
        pfile = 'pumpcheck2.txt'
        with open(pfile, 'w+') as f:
            f.write(onoff)
            f.close()
    elif valve == 3:
        pfile1 = 'pumpcheck1.txt'
        pfile2 = 'pumpcheck2.txt'
        with open(pfile1, 'w+') as f:
            f.write(onoff)
            f.close()
        with open(pfile2, 'w+') as f:
            f.write(onoff)
            f.close()


def auto_check():
    try:
        with open('autocheck.txt', 'r') as f:
            onoff = f.readline()
        if onoff == 'on':
            return True
        else:
            return False
    except FileNotFoundError: #catch on boot up, assume pump off
        return False

def auto_file_write(onoff):
    with open('autocheck.txt', 'w+') as f:
        f.write(onoff)
        f.close()

def auto_run(t2, t3, path, string):
    sensors = sensor_check(t2, t3) #check for bad sensors
    if sensors[0] == True and sensors[1] == True:
        email_check('good')
        while ((t2 > 80.0) or (t3 > 80.0)) and auto_check() and (sensors[0]==True) and (sensors[1]==True):
            if (t2 > 80.0) and (t3 > 80.0):
                print("Auto on both pumps")
                print(f"t2={t2} t3={t3} sensor 0 = {sensors[0]} sensor 1 = {sensors[1]}")
                pump_on(3)
                time.sleep(288)
                pump_off(3)
            elif (t2 > 80.0) and (t3 < 80.0):
                print("Auto on t2")
                print(f"t2={t2} t3={t3} sensor 0 = {sensors[0]} sensor 1 = {sensors[1]}")
                pump_on(1)
                time.sleep(288)
                pump_off(1)
            elif (t2 < 80.0) and (t3 > 80.0):
                print("Auto on t3")
                print(f"t2={t2} t3={t3} sensor 0 = {sensors[0]} sensor 1 = {sensors[1]}")
                pump_on(2)
                time.sleep(288)
                pump_off(2)
            time.sleep(2)
            t1, t2, t3, p = serRead()
            string = f"{t1} {t2} {t3} {p}"
            FileWrite(path, string)
            sensors = sensor_check(t2, t3)
            if (t2 < 65.0) or (t3 < 65.0):
                alert_email("software")
                auto_file_write('off')
    elif sensors[0] == True and sensors[1] == False:
        email_check('tank3')
        while (t2 > 80.0) and auto_check():
            print("Auto on both no t3")
            print(f"t2={t2} t3={t3} sensor 0 = {sensors[0]} sensor 1 = {sensors[1]}")
            pump_on(3)
            time.sleep(288)
            pump_off(3)
            time.sleep(2)
            t1, t2, t3, p = serRead()
            string = f"{t1} {t2} {t3} {p}"
            FileWrite(path, string)
            if (t2 < 65.0) or (t3 < 65.0):
                alert_email("software")
                auto_file_write('off')
    elif sensors[0] == False and sensors[1] == True:
        email_check('tank2')
        while (t3 > 80.0) and auto_check():
            print("Auto on t3 no t2")
            print(f"t2={t2} t3={t3} sensor 0 = {sensors[0]} sensor 1 = {sensors[1]}")
            pump_on(3)
            time.sleep(288)
            pump_off(3)
            time.sleep(2)
            t1, t2, t3, p = serRead()
            string = f"{t1} {t2} {t3} {p}"
            FileWrite(path, string)
            if (t2 < 65.0) or (t3 < 65.0):
                alert_email("software")
                auto_file_write('off')
    else: #both sensors are broken, shutoff system
        email_check('both')
        auto_file_write('off')
        print("Lost both sensors, shutting off auto")
    print(f"Exiting autoprogram with t2={t2} and t3={t3}")

def sensor_check(t2, t3):
    sensorlist = []
    if t2 == 185.0:
        sensorlist.append(False)
    else:
        sensorlist.append(True)
    if t3 == 185.0:
        sensorlist.append(False)
    else:
        sensorlist.append(True)
    return sensorlist

def alert_email(sensor):
    msg = EmailMessage()
    if sensor == 'both':
        content = """Warning: Both temperature sensors are not reading correctly.
        The automated temperature adjustment will be shut off."""
    elif sensor == 'sensor':
        content = """Warning: Something up with the software.
        The automated temperature adjustment will be shut off."""
    else:
        content = f"""Warning: Temperature sensor on {sensor} is not reading correctly.
        The automated temperature adjustment is now running both tanks off of the other sensor."""
    msg.set_content(content)
    msg['Subject'] = f'ATTENTION: Sensor Problem on {sensor}'
    msg['From'] = "njordan@kohanakai.com"
    msg['To'] = ['jdp2766@gmail.com', 'njordan@kohanakai.com']
    s = smtplib.SMTP('smtp-relay.gmail.com', 25)
    s.send_message(msg)
    s.quit()
    email_file_write(sensor)

def email_check(arg):
    try:
        with open('emailcheck.txt', 'r') as f:
            content = f.readline()
    except FileNotFoundError:
        content = ""
    if arg == 'good' and content != arg:
        email_file_write(arg)
    elif arg != 'good' and content != arg:
        alert_email(arg)


def email_file_write(sensor):
    with open('emailcheck.txt', 'w+') as f:
        f.write(sensor)
        f.close()
