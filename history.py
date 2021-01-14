from datetime import datetime, date
import statistics

from flask import Flask, render_template, request, flash, redirect, url_for

from bokeh.plotting import figure, output_file, show
from bokeh.layouts import gridplot
from bokeh.embed import components


def history(path, daystring, submit):
    time_arr = []
    temp1 = []
    temp2 = []
    temp3 = []
    ph = []
    try:
        with open(path, 'r') as f:
            for line in f:
                data = line.split()
                time = data[0].strip().strip('*\x00')
                time = datetime.strptime(time, '%H:%M:%S')
                data_date = datetime.strptime(daystring, '%Y-%m-%d')
                time = time.replace(year=data_date.year, month=data_date.month, day=data_date.day)
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

        days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
        months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        years = [2020, 2021]


        return render_template("history.html", data_date=data_date.strftime('%Y-%m-%d'),
                                t1plot=t1plot, t2plot=t2plot, t3plot=t3plot, phplot=phplot,
                                submit=submit, days=days, months=months, years=years)
    except FileNotFoundError:
        flash('No data on that day')
        return redirect(url_for('history_'))

    except IndexError:
        flash('Bad data on that day')
