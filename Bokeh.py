from math import pi
import pandas as pd
from bokeh.plotting import figure, show, output_file
from bokeh.models import DatetimeTickFormatter


df = pd.read_csv("Output/csv/NASDAQ_APPL_5m.csv", delimiter=',')
df["date"] = pd.to_datetime(df["date"], format='%Y%m%d%H%M')
print(df)

inc = df.close > df.open
dec = df.open > df.close
w = 240*1000 # half day in ms

TOOLS = "pan,wheel_zoom,xwheel_zoom,ywheel_zoom,box_zoom,reset,save"

p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000, title="Candlestick")
p.xaxis.major_label_orientation = pi/4


# map dataframe indices to date strings and use as label overrides
p.xaxis.major_label_overrides = {
    i: date.strftime('%F, %H:%M') for i, date in enumerate(pd.to_datetime(df["date"]))
}

p.grid.grid_line_alpha=0.3
p.segment(df.index, df.high, df.index, df.low, color="black")
p.vbar(df.index[inc], 0.5, df.open[inc], df.close[inc], fill_color="#D5E1DD", line_color="black")
p.vbar(df.index[dec], 0.5, df.open[dec], df.close[dec], fill_color="#F2583E", line_color="black")


output_file("candlestick.html", title="candlestick.py example")

show(p)  # open a browser