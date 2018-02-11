from math import pi
import pandas as pd
from bokeh.plotting import figure, show, output_file
from bokeh.models import DatetimeTickFormatter


df = pd.read_csv("Output/csv/NASDAQ_APPL_5m.csv", delimiter=',')
df["date"] = pd.to_datetime(df["date"], format='%Y%m%d%H%M')


inc = df.close > df.open
dec = df.open > df.close
w = 240*1000 # half day in ms

TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000, title="Candlestick")
p.xaxis.major_label_orientation = pi/4
p.xaxis.formatter = DatetimeTickFormatter(
        microseconds=["%F, %H:%M"],
        milliseconds=["%F, %H:%M"],
        seconds=["%F, %H:%M"],
        minsec=["%F, %H:%M"],
        minutes=["%F, %H:%M"],
        hourmin=["%F, %H:%M"],
        hours=["%F, %H:%M"],
        days=["%F, %H:%M"],
        months=["%F, %H:%M"],
        years=["%F, %H:%M"],
    )
p.grid.grid_line_alpha=0.3

p.segment(df.date, df.high, df.date, df.low, color="black")
p.vbar(df.date[inc], w, df.open[inc], df.close[inc], fill_color="#1fb766", line_color="black")
p.vbar(df.date[dec], w, df.open[dec], df.close[dec], fill_color="#F2583E", line_color="black")

output_file("candlestick.html", title="candlestick.py example")

show(p)  # open a browser