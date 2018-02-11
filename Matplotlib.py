from matplotlib.finance import candlestick_ohlc
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import numpy as np
import urllib
from matplotlib.dates import datestr2num
import datetime
from matplotlib.dates import num2date
from matplotlib.dates import date2num


class Parser:

    # @staticmethod
    # def parse(a_filepath):
    #
    #     fig = plt.figure()
    #     ax = plt.subplot2grid((1, 1), (0, 0))
    #
    #     date = list()
    #     openp = list()
    #     highp = list()
    #     lowp = list()
    #     closep = list()
    #     volume = list()
    #
    #     # date.append(float("20101015"))
    #     date.append(date2num(datetime.datetime(2015, 10, 15)))
    #     openp.append(float("305.9"))
    #     highp.append(float("306"))
    #     lowp.append(float("305.26"))
    #     closep.append(float("305.95"))
    #     volume.append(int("40927"))
    #
    #     date.append(date2num(datetime.datetime(2015, 10, 16)))
    #     openp.append(float("305.94"))
    #     highp.append(float("306.87"))
    #     lowp.append(float("305.93"))
    #     closep.append(float("306.8"))
    #     volume.append(int("49084"))
    #
    #
    #     ohlc = []
    #     append_me = date[0], openp[0], highp[0], lowp[0], closep[0], volume[0]
    #     ohlc.append(append_me)
    #
    #     append_me = date[1], openp[1], highp[1], lowp[1], closep[1], volume[1]
    #     ohlc.append(append_me)
    #
    #     candlestick_ohlc(ax, ohlc, width=0.1, colorup='#77d879', colordown='#db3f3f')
    #
    #     for label in ax.xaxis.get_ticklabels():
    #         label.set_rotation(45)
    #
    #     ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    #     ax.xaxis.set_major_locator(mticker.MaxNLocator(1))
    #     ax.grid(True)
    #
    #
    #
    #     plt.xlabel('Date')
    #     plt.ylabel('Price')
    #     plt.title('NASDAQ_APPL')
    #     plt.legend()
    #     plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
    #     plt.show()

    @staticmethod
    def parse(a_filepath):

        ax1 = plt.subplot2grid((1, 1), (0, 0))

        date, closep, highp, lowp, openp, volume = np.loadtxt(a_filepath,
                                                              dtype='str',
                                                              delimiter=',',
                                                              unpack=True)

        x = 0
        y = len(date)
        ohlc = []

        while x < y:
            a_year = int(date[x][0:4])
            a_month = int(date[x][4:6])
            a_day = int(date[x][6:8])
            a_hour = int(date[x][8:10])
            a_minute = int(date[x][10:12])
            my_date_time = datetime.datetime(a_year, a_month, a_day, a_hour, a_minute)
            a_open = float(openp[x])
            a_high = float(highp[x])
            a_low = float(lowp[x])
            a_close = float(closep[x])
            a_volume = float(volume[x])
            append_me = date2num(my_date_time), a_open, a_high, a_low, a_close, a_volume
            ohlc.append(append_me)
            x += 1

        candlestick_ohlc(ax1, ohlc, width=0.0001, colorup='#77d879', colordown='#db3f3f')

        for label in ax1.xaxis.get_ticklabels():
            label.set_rotation(45)

        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y%m%d%H%M'))
        ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
        # ax1.yaxis.limit_range_for_scale(1, 10)
        ax1.grid(True)

        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title('Test')
        plt.legend()
        plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
        plt.show()

    @staticmethod
    def parse_example():
        fig = plt.figure()
        ax1 = plt.subplot2grid((1, 1), (0, 0))

        # Unfortunately, Yahoo's API is no longer available
        # feel free to adapt the code to another source, or use this drop-in replacement.
        stock_price_url = 'https://pythonprogramming.net/yahoo_finance_replacement'
        source_code = urllib.request.urlopen(stock_price_url).read().decode()
        stock_data = []
        split_source = source_code.split('\n')
        for line in split_source[1:]:
            split_line = line.split(',')
            if len(split_line) == 7:
                if 'values' not in line and 'labels' not in line:
                    stock_data.append(line)

        date, closep, highp, lowp, openp, adj_closep, volume = np.loadtxt(stock_data,
                                                                          delimiter=',',
                                                                          unpack=True,
                                                                          converters={0: bytespdate2num('%Y-%m-%d')})

        x = 0
        y = len(date)
        ohlc = []

        while x < y:
            append_me = date[x], openp[x], highp[x], lowp[x], closep[x], volume[x]
            ohlc.append(append_me)
            x += 1

        candlestick_ohlc(ax1, ohlc, width=0.4, colorup='#77d879', colordown='#db3f3f')

        for label in ax1.xaxis.get_ticklabels():
            label.set_rotation(45)

        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
        ax1.grid(True)

        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title('Test')
        plt.legend()
        plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
        plt.show()


def stringtonum(a_string):
    return

def bytespdate2num(fmt, encoding='utf-8'):
    strconverter = mdates.strpdate2num(fmt)

    def bytesconverter(b):
        s = b.decode(encoding)
        return strconverter(s)
    return bytesconverter


def run():
    Parser.parse("Output/csv/NASDAQ_APPL_5m.csv")
    # Parser.parse("Output/csv/NASDAQ_APPL_15m.csv")
    # Parser.parse("Output/csv/NASDAQ_APPL_30m.csv")
    # Parser.parse("Output/csv/NASDAQ_APPL_60m.csv")
    # Parser.parse_example()


if __name__ == '__main__':
    run()
