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
    ser = serial.Serial('/dev/ttyACM1', 9600)
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
        x = float(values[0])
        t1.append(x)
        t2.append(float(values[1]))
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
