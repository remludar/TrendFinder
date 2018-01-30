import csv
import sys


class Record:
    ticker = ""
    date = ""
    open = ""
    high = ""
    low = ""
    close = ""
    vol = ""

    def add(self, a_ticker, a_date, a_open, a_high, a_low, a_close, a_vol):
        self.ticker = a_ticker
        self.date = a_date
        self.open = a_open
        self.high = a_high
        self.low = a_low
        self.close = a_close
        self.vol = a_vol

    def __str__(self):
        return self.ticker + "," + self.date + "," + self.open + "," + self.high + "," + \
               self.low + "," + self.close + "," + self.vol


class Sample:
    def __init__(self):
        self.records = []

    def add_record(self, a_record):
        self.records.append(a_record)

    def print(self):
        result = ''
        for record in self.records:
            print(record)


class Parser:
    def parse(self, a_filepath):
        sample = Sample()
        file_reader = csv.reader(open(a_filepath, newline=''), delimiter=',', quotechar='|')
        for row in file_reader:
            record = Record()
            record.add(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            sample.add_record(record)
        sample.records.pop(0)
        return sample

    def get_up_trends(self, data):
        previous_high = 0.0
        previous_low = 0.0
        master_list = []
        trend_row_list = []
        for row in data.records:
            if float(row.high) > previous_high and float(row.low) > previous_low:
                previous_high = float(row.high)
                previous_low = float(row.low)
                trend_row_list.append(row)
            else:
                if trend_row_list.__len__() > 1:
                    master_list.append(trend_row_list)
                previous_high = float(row.high)
                previous_low = float(row.low)
                trend_row_list = [row]
        return master_list

    def get_down_trends(self, data):
        previous_high = sys.float_info.max
        previous_low = sys.float_info.max
        master_list = []
        trend_row_list = []
        for row in data.records:
            if float(row.high) < previous_high and float(row.low) < previous_low:
                previous_high = float(row.high)
                previous_low = float(row.low)
                trend_row_list.append(row)
            else:
                if trend_row_list.__len__() > 1:
                    master_list.append(trend_row_list)
                previous_high = float(row.high)
                previous_low = float(row.low)
                trend_row_list = [row]
        return master_list


def print_list(data):
    for r in data:
        print("TREND")
        for i in r:
            print("ROW: " + str(i))


if __name__ == '__main__':
    parser = Parser()
    full_sample = parser.parse("NASDAQ_AAPL.txt")
    up_trends_list = parser.get_up_trends(full_sample)
    down_trends_list = parser.get_down_trends(full_sample)

    print("=========UP TRENDS==========")
    print_list(up_trends_list)
    print("=========DOWN TRENDS==========")
    print_list(down_trends_list)



