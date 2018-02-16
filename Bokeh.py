from math import pi
import pandas as pd
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, PanTool, WheelZoomTool, ResetTool, SaveTool, HoverTool


def create_chart_new():
    df = pd.read_csv("Output/csv/NASDAQ_APPL_60m.csv", delimiter=',')
    df["date"] = pd.to_datetime(df["date"], format='%Y%m%d%H%M')
    source = ColumnDataSource(df)

    inc = df.close > df.open
    dec = df.open > df.close

    df_green = df[inc]
    df_red = df[dec]

    green_source = ColumnDataSource(df_green)
    red_source = ColumnDataSource(df_red)

    pan = PanTool()
    wheel_zoom = WheelZoomTool()
    reset = ResetTool()
    save = SaveTool()

    print(source.data['open'][inc])
    print(green_source.data['open'])

    hover = HoverTool(
        tooltips=[
            ("index:", "@index"),
            ("open:", "@open"),
            ("high:", "@high"),
            ("low:", "@low"),
            ("close:", "@close"),
            ("volume:", "@volume"),
        ]
    )

    p = figure(x_axis_type="datetime", tools=[pan, wheel_zoom, reset, save, hover], plot_width=1000, title="Candlestick")
    p.xaxis.major_label_orientation = pi / 4

    # map dataframe indices to date strings and use as label overrides
    p.xaxis.major_label_overrides = {
        i: date.strftime('%F, %H:%M') for i, date in enumerate(pd.to_datetime(df["date"]))
    }
    p.grid.grid_line_alpha = 0.3

    p.segment(
        x0='index',
        y0='high',
        x1='index',
        y1='low',
        color='black',
        source=source
    )

    # green candle bodies
    p.vbar(
        'index',
        0.5,
        'close',
        'open',
        fill_color="#D5E1DD",
        line_color="black",
        source=green_source
    )

    # red candle bodies
    p.vbar(
        'index',
        0.5,
        'open',
        'close',
        fill_color="#F2583E",
        line_color="black",
        source=red_source
    )

    output_file("candlestick.html", title="candlestick.py example")
    show(p)  # open a browser


def example():
    source = ColumnDataSource(data=dict(
        x=[1, 2, 3, 4, 5],
        y=[2, 5, 8, 2, 7],
        desc=['A', 'b', 'C', 'd', 'E'],
    ))

    print(source.data)

    hover = HoverTool(tooltips=[
        ("index", "$index"),
        # ("(x,y)", "($x, $y)"),
        ("desc", "@desc"),
    ])

    p = figure(plot_width=400, plot_height=400, tools=[hover],
               title="Mouse over the dots")

    p.circle('x', 'y', size=20, source=source)

    output_file("toolbar.html")
    show(p)

if __name__ == '__main__':
    # example()
    create_chart_new()
