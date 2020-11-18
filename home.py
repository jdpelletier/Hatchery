from datetime import datetime, date
import statistics

from flask import Flask, render_template, request

from bokeh.plotting import figure, output_file, show
from bokeh.layouts import gridplot
from bokeh.embed import components

from Util import pump_on, pump_off, pump_check

def home(path):
    # prepare some data
    time_arr = []
    temp1 = []
    temp2 = []
    temp3 = []
    ph = []
    with open(path, 'r') as f:
        for line in f:
            data = line.split()
            time = datetime.strptime(data[0], '%H:%M:%S')
            today = date.today()
            time = time.replace(year=today.year, month=today.month, day=today.day)
            time_arr.append(time)
            temp1.append(float(data[1]))
            temp2.append(float(data[2]))
            temp3.append(float(data[3]))
            ph.append(float(data[3]))
    t1_max = max(temp1)
    t2_max = max(temp2)
    t3_max = max(temp3)
    t1_min = min(temp1)
    t2_min = min(temp2)
    t3_min = min(temp3)
    ph_av = statistics.mean(ph)
    datadic = {
        "day" : today,
        "time" : time.strftime("%H:%M:%S"),
        "temp1" : float(data[1]),
        "temp2" : float(data[2]),
        "temp3" : float(data[3]),
        "ph" : float(data[3])
        }

    t1_plot = figure(title="Temp 1", x_axis_label='Time', y_axis_label='Temp F',
               x_axis_type='datetime')
    t1_plot.circle(time_arr, temp1, size=5)
    t1_plot.line(time_arr, t1_max, legend_label="Max temp today: %f" % t1_max,
                 line_color="red")
    t1_plot.line(time_arr, t1_min, legend_label="Min temp today: %f" % t1_min,
                 line_color="blue")
    t2_plot = figure(title="Temp 2", x_axis_label='Time', y_axis_label='Temp F',
               x_axis_type='datetime')
    t2_plot.circle(time_arr, temp2, size=5)
    t2_plot.line(time_arr, t2_max, legend_label="Max temp today: %f" % t2_max,
                 line_color="red")
    t2_plot.line(time_arr, t2_min, legend_label="Min temp today: %f" % t2_min,
                 line_color="blue")
    t3_plot = figure(title="Temp 3", x_axis_label='Time', y_axis_label='Temp F',
               x_axis_type='datetime')
    t3_plot.circle(time_arr, temp3, size=5)
    t3_plot.line(time_arr, t3_max, legend_label="Max temp today: %f" % t3_max,
                 line_color="red")
    t3_plot.line(time_arr, t3_min, legend_label="Min temp today: %f" % t3_min,
                 line_color="blue")
    ph_plot = figure(title="Fish Tank pH", x_axis_label='Time', y_axis_label='pH',
               x_axis_type='datetime')
    ph_plot.circle(time_arr, ph, size=5)
    ph_plot.line(time_arr, ph_av, legend_label="Average pH today: %f" % ph_av,
                 line_color="green")

    p = gridplot([[t1_plot, t2_plot], [t3_plot, ph_plot, None]])
    # p = gridplot([[t1_plot, t2_plot], [ph_plot, None]])

    script, div = components(p)

    ##Button stuff##
    pumprunning = pump_check()
    pumpon = request.form.get("pumpon")
    if pumpon:
        if pumprunning == False:
            pumprunning = pump_on()

    pumpoff = request.form.get("pumpoff")
    if pumpoff:
        if pumprunning == True:
            pumprunning = pump_off()


    return render_template("home.html", datadic=datadic, script=script, div=div, pumpon=pumpon, pumpoff=pumpoff, pumprunning=pumprunning)