import os
import time
import datetime
import statistics
import serial

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


def pump_on():
    try:
        arduino = serial.Serial('/dev/ttyACM0', 9600)
        time.sleep(2)
        arduino.write(b'H')
        time.sleep(1)
        arduino.close()
        pump_file_write('on')
        return True
    except serial.serialutil.SerialException:
        return False

def pump_off():
    try:
        arduino = serial.Serial('/dev/ttyACM0', 9600)
        time.sleep(2)
        arduino.write(b'L')
        time.sleep(1)
        arduino.close()
        pump_file_write('off')
        return False
    except serial.serialutil.SerialException:
        return True

def pump_check():
    try:
        with open('pumpcheck.txt', 'r') as f:
            onoff = f.readline()
        if onoff == 'on':
            return True
        else:
            return False
    except FileNotFoundError: #catch on boot up, assume pump off
        return False

def pump_file_write(onoff):
    with open('pumpcheck.txt', 'w+') as f:
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
