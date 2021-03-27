from datetime import datetime, date
import statistics

from flask import Flask, render_template, request

from bokeh.plotting import figure, output_file, show
from bokeh.layouts import gridplot
from bokeh.embed import components

from Util import pump_on, pump_off, pump_check, auto_file_write, auto_check, auto_file_write_2, auto_check_2, pump_check_2

def home(path1, path2):
    # prepare some data
    time_arr = []
    temp1 = []
    temp2 = []
    temp3 = []
    ph = []
    with open(path, 'r') as f:
        for line in f:
            data = line.split()
            time = data[0].strip().strip('*\x00')
            time = datetime.strptime(time, '%H:%M:%S')
            today = date.today()
            time = time.replace(year=today.year, month=today.month, day=today.day)
            time_arr.append(time)
            temp1.append(float(data[1]))
            temp2.append(float(data[2]))
            temp3.append(float(data[3]))
            ph.append(float(data[4]))
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
        "ph" : float(data[4])
        }

    t1_plot = figure(title="Temp 1", x_axis_label='Time', y_axis_label='Temp F',
               x_axis_type='datetime')
    t1_plot.sizing_mode = 'scale_width'
    t1_plot.circle(time_arr, temp1, size=5)
    t1_plot.line(time_arr, t1_max, legend_label="Max temp today: %f" % t1_max,
                 line_color="red")
    t1_plot.line(time_arr, t1_min, legend_label="Min temp today: %f" % t1_min,
                 line_color="blue")
    t1plots = {'plot' : t1_plot}
    t1plot = components(t1plots)

    t2_plot = figure(title="Temp 2", x_axis_label='Time', y_axis_label='Temp F',
               x_axis_type='datetime')
    t2_plot.sizing_mode = 'scale_width'
    t2_plot.circle(time_arr, temp2, size=5)
    t2_plot.line(time_arr, t2_max, legend_label="Max temp today: %f" % t2_max,
                 line_color="red")
    t2_plot.line(time_arr, t2_min, legend_label="Min temp today: %f" % t2_min,
                 line_color="blue")
    t2plots = {'plot' : t2_plot}
    t2plot = components(t2plots)

    t3_plot = figure(title="Temp 3", x_axis_label='Time', y_axis_label='Temp F',
               x_axis_type='datetime')
    t3_plot.sizing_mode = 'scale_width'
    t3_plot.circle(time_arr, temp3, size=5)
    t3_plot.line(time_arr, t3_max, legend_label="Max temp today: %f" % t3_max,
                 line_color="red")
    t3_plot.line(time_arr, t3_min, legend_label="Min temp today: %f" % t3_min,
                 line_color="blue")
    t3plots = {'plot' : t3_plot}
    t3plot = components(t3plots)

    ph_plot = figure(title="Fish Tank pH", x_axis_label='Time', y_axis_label='pH',
               x_axis_type='datetime')
    ph_plot.sizing_mode = 'scale_width'
    ph_plot.circle(time_arr, ph, size=5)
    ph_plot.line(time_arr, ph_av, legend_label="Average pH today: %f" % ph_av,
                 line_color="green")
    phplots = {'plot' : ph_plot}
    phplot = components(phplots)

    # p = gridplot([[t1_plot, t2_plot], [t3_plot, ph_plot]])
    # p.sizing_mode = 'scale_width'
    #
    # script, div = components(p)

    ##Button stuff##
    pump1running = pump_check(1)
    pump2running = pump_check(2)
    pump1on = request.form.get("pump1on")
    if pump1on:
        pump1running = pump_check(1)
        pump2running = pump_check(2)
        if pump1running == False and pump2running == True:
            pump1running = pump_on(3)
        elif pump1running == False and pump2running == False:
            pump1running = pump_on(1)

    pump2on = request.form.get("pump2on")
    if pump2on:
        pump1running = pump_check(1)
        pump2running = pump_check(2)
        if pump1running == True and pump2running == False:
            pump2running = pump_on(3)
        elif pump1running == False and pump2running == False:
            pump2running = pump_on(2)

    pump1off = request.form.get("pump1off")
    if pump1off:
        pump1running = pump_check(1)
        pump2running = pump_check(2)
        if pump1running == True and pump2running == False:
            pump1running = pump_off(1)
        elif pump1running == True and pump2running == True:
            pump1running = pump_off(1)
            pump2running = pump_on(2)

    pump2off = request.form.get("pump2off")
    if pump2off:
        pump1running = pump_check(1)
        pump2running = pump_check(2)
        if pump1running == False and pump2running == True:
            pump2running = pump_off(2)
        elif pump1running == True and pump2running == True:
            pump2running = pump_off(2)
            pump1running = pump_on(1)

    autorunning = auto_check()
    autoon = request.form.get("autoon")
    if autoon:
        if autorunning == False:
            autorunning = auto_file_write('on')

    autooff = request.form.get("autooff")
    if autooff:
        if autorunning == True:
            autorunning = auto_file_write('off')

    #Setup 2 stuff
    # prepare some data
    time_arr_2 = []
    temp1_2 = []
    temp2_2 = []
    temp3_2 = []
    with open(path2, 'r') as f:
        for line in f:
            data_2 = line.split()
            time = data_2[0].strip().strip('*\x00')
            time = datetime.strptime(time, '%H:%M:%S')
            today = date.today()
            time = time.replace(year=today.year, month=today.month, day=today.day)
            time_arr_2.append(time)
            temp1_2.append(float(data_2[1]))
            temp2_2.append(float(data_2[2]))
            temp3_2.append(float(data_2[3]))
    t1_max_2 = max(temp1_2)
    t2_max_2 = max(temp2_2)
    t3_max_2 = max(temp3_2)
    t1_min_2 = min(temp1_2)
    t2_min_2 = min(temp2_2)
    t3_min_2 = min(temp3_2)
    datadic_2 = {
        "day" : today,
        "time" : time.strftime("%H:%M:%S"),
        "temp1" : float(data_2[1]),
        "temp2" : float(data_2[2]),
        "temp3" : float(data_2[3]),
        }

    t1_plot_2 = figure(title="Temp 1", x_axis_label='Time', y_axis_label='Temp F',
               x_axis_type='datetime')
    t1_plot_2.sizing_mode = 'scale_width'
    t1_plot_2.circle(time_arr_2, temp1_2, size=5)
    t1_plot_2.line(time_arr_2, t1_max_2, legend_label="Max temp today: %f" % t1_max_2,
                 line_color="red")
    t1_plot_2.line(time_arr_2, t1_min_2, legend_label="Min temp today: %f" % t1_min_2,
                 line_color="blue")
    t1plots_2 = {'plot' : t1_plot_2}
    t1plot_2 = components(t1plots_2)

    t2_plot_2 = figure(title="Temp 2", x_axis_label='Time', y_axis_label='Temp F',
               x_axis_type='datetime')
    t2_plot_2.sizing_mode = 'scale_width'
    t2_plot_2.circle(time_arr_2, temp2_2, size=5)
    t2_plot_2.line(time_arr_2, t2_max_2, legend_label="Max temp today: %f" % t2_max_2,
                 line_color="red")
    t2_plot_2.line(time_arr_2, t2_min_2, legend_label="Min temp today: %f" % t2_min_2,
                 line_color="blue")
    t2plots_2 = {'plot' : t2_plot_2}
    t2plot_2 = components(t2plots_2)

    t3_plot_2 = figure(title="Temp 3", x_axis_label='Time', y_axis_label='Temp F',
               x_axis_type='datetime')
    t3_plot_2.sizing_mode = 'scale_width'
    t3_plot_2.circle(time_arr_2, temp3_2, size=5)
    t3_plot_2.line(time_arr_2, t3_max_2, legend_label="Max temp today: %f" % t3_max_2,
                 line_color="red")
    t3_plot_2.line(time_arr_2, t3_min_2, legend_label="Min temp today: %f" % t3_min_2,
                 line_color="blue")
    t3plots_2 = {'plot' : t3_plot_2}
    t3plot_2 = components(t3plots_2)

    pump1running_2 = pump_check_2(1)
    pump2running_2 = pump_check_2(2)
    pump1on_2 = request.form.get("pump1on_2")
    if pump1on_2:
        pump1running_2 = pump_check_2(1)
        pump2running_2 = pump_check_2(2)
        if pump2running_2 == True:
            pump_onoff_write('11')
        else:
            pump_onoff_write('10')

    pump2on_2 = request.form.get("pump2on_2")
    if pump2on_2:
        pump1running_2 = pump_check_2(1)
        pump2running_2 = pump_check_2(2)
        if pump1running_2 == True:
            pump_onoff_write('11')
        else:
            pump_onoff_write('01')

    pump1off_2 = request.form.get("pump1off")
    if pump1off_2:
        pump1running_2 = pump_check_2(1)
        pump2running_2 = pump_check_2(2)
        if pump2running_2 == False:
            pump_onoff_write('00')
        else:
            pump_onoff_write('01')

    pump2off_2 = request.form.get("pump2off")
    if pump2off_2:
        pump1running_2 = pump_check_2(1)
        pump2running_2 = pump_check_2(2)
        if pump1running_2 == False:
            pump_onoff_write('00')
        else:
            pump_onoff_write('10')

    autorunning_2 = auto_check_2()
    autoon_2 = request.form.get("autoon_2")
    if autoon_2:
        if autorunning_2 == False:
            autorunning_2 = auto_file_write_2('on')

    autooff_2 = request.form.get("autooff_2")
    if autooff_2:
        if autorunning_2 == True:
            autorunning_2 = auto_file_write_2('off')


    return render_template("home2setups.html", datadic=datadic, t1plot=t1plot,
                            t2plot=t2plot, t3plot=t3plot, phplot=phplot,
                            pump1on=pump1on, pump1off=pump1off, pump2on=pump2on,
                            pump2off=pump2off, pump1running=pump1running,
                            pump2running=pump2running, pump1on_2=pump1on_2,
                            pump1off_2=pump1off_2, pump2on_2=pump2on_2,
                            pump2off_2=pump2off_2, pump1running_2=pump1running_2,
                            pump2running_2=pump2running_2, datadic_2=datadic_2, t1plot_2=t1plot_2,
                            t2plot_2=t2plot_2, t3plot_2=t3plot_2, autoon=autoon,
                            autooff=autooff, autorunning=autorunning, autoon_2=autoon_2,
                            autooff_2=autooff_2, autorunning_2=autorunning_2)
