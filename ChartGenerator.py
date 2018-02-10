import csv
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

plotly.tools.set_credentials_file(username='remludar', api_key='gnyC5UMq2Nmjd3wjFLvo')
plotly.tools.set_config_file(world_readable=True, sharing='public')

INCREASING_COLOR = '#00FF00'
DECREASING_COLOR = '#FF0000'

candle_open = list()
candle_high = list()
candle_low = list()
candle_close = list()


class Parser:

    @staticmethod
    def parse(a_filepath):
        file_reader = csv.reader(open(a_filepath, newline=''), delimiter=',', quotechar='|')
        for row in file_reader:
            candle_open.append(row[0])
            candle_high.append(row[1])
            candle_low.append(row[2])
            candle_close.append(row[3])


def run():
    Parser.parse("Output/csv/NASDAQ_APPL_5m.csv")

    candles = go.Candlestick(
        open=candle_open,
        high=candle_high,
        low=candle_low,
        close=candle_close,
        increasing=dict(line=dict(color=INCREASING_COLOR)),
        decreasing=dict(line=dict(color=DECREASING_COLOR))
    )

    data = go.Data([candles])
    py.plot(data, filename='candle-test')


if __name__ == '__main__':
    run()
