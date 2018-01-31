import csv
import sys
import math

class Record:
    ticker = ""
    date = ""
    open = ""
    high = ""
    low = ""
    close = ""
    vol = ""
    candle_color = ""
    candle_type = ""
    candle_top = ""
    candle_bottom = ""

    def add(self, a_ticker, a_date, a_open, a_high, a_low, a_close, a_vol):
        self.ticker = a_ticker
        self.date = a_date
        self.open = a_open
        self.high = a_high
        self.low = a_low
        self.close = a_close
        self.vol = a_vol

    def __str__(self):
        return self.ticker + "," + self.date + "," + self.open + "," + self.high + "," + self.low + "," + \
               self.close + "," + self.vol + "," + self.candle_color + "," + self.candle_type


class Sample:
    def __init__(self):
        self.records = []

    def add_record(self, a_record):
        self.records.append(a_record)

    def print(self):
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

    def parse_wo_ticker(self, a_filepath):
        sample = Sample()
        file_reader = csv.reader(open(a_filepath, newline=''), delimiter=',', quotechar='|')
        for row in file_reader:
            record = Record()
            record.add("AAPL", row[0], row[1], row[2], row[3], row[4], row[6])
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

    def set_candle_data(self, data):
        for row in data.records:

            body_size = math.fabs(float(row.open) - float(row.close))
            upper_shadow = float(row.high) - float(row.close)
            lower_shadow = float(row.open) - float(row.low)
            range = float(row.high) - float(row.low)

            # Candle color
            if float(row.open) < float(row.close):
                row.candle_color = "green"
                row.candle_top = row.close
                row.candle_bottom = row.open
            elif float(row.open) > float(row.close):
                row.candle_color = "red"
                row.candle_top = row.open
                row.candle_bottom = row.close
                upper_shadow = float(row.high) - float(row.open)
                lower_shadow = float(row.close) - float(row.low)
            elif float(row.open) == float(row.close):
                row.candle_color = "none"
                row.candle_top = row.open
                row.candle_bottom = row.candle_top

            # Marubozu
            if (float(row.open) == float(row.low) and float(row.close) == float(row.high)) or\
               (float(row.open) == float(row.high) and float(row.close) == float(row.low)):
                row.candle_type = "marubozu"

            # Long Upper Shadow
            if row.candle_color == "red" and\
               upper_shadow >= 0.66 * range and\
               lower_shadow <= 0.33 * range and\
               float(row.close) != float(row.low):
                row.candle_type = "longUpperShadow"

            # Long Lower Shadow
            if row.candle_color == "green" and\
               upper_shadow <= 0.33 * range and\
               lower_shadow >= 0.66 * range and\
               float(row.close) != float(row.high):
                row.candle_type = "longLowerShadow"

            # Spinning Top
            if 0.33 * range >= body_size >= 0.10 * range and\
                upper_shadow >= 2.5 * body_size and\
                lower_shadow >= 2.5 * body_size and \
               math.fabs(upper_shadow / range - lower_shadow / range) < 0.20:
                row.candle_type = "spinningTop"

            # Doji
            if 0.10 * range >= body_size:
                if upper_shadow == 0:
                    row.candle_type = "dragonflyDoji"
                if lower_shadow == 0:
                    row.candle_type = "gravestoneDoji"
                if upper_shadow >= 8 * body_size and \
                   lower_shadow >= 8 * body_size and \
                   math.fabs(upper_shadow / range - lower_shadow / range) < 0.20:
                    row.candle_type = "longLeggedDoji"
                else:
                    row.candle_type = "doji"

            # Hammer / Hanging Man
            if 0.33 * range >= body_size >= 0.10 * range and\
               upper_shadow <= 1 * body_size and\
               lower_shadow >= 3 * body_size:
                if row.candle_color == "green":
                    row.candle_type = "hammer"
                elif row.candle_color == "red":
                    row.candle_type = "hangingMan"

            if row.date == "2018-01-23":
                i = 0

            # Inverted Hammer / Shooting Star
            if 0.33 * range >= body_size >= 0.05 * range and\
               upper_shadow >= 3 * body_size and\
               lower_shadow <= 1 * body_size:
                if row.candle_color == "green":
                    row.candle_type = "invertedHammer"
                elif row.candle_color == "red":
                    row.candle_type = "shootingStar"


def print_list(data):
    for r in data:
        print("TREND")
        for i in r:
            print("ROW: " + str(i))


def print_sample(data):
    for record in data.records:
        print(record)


def run_old_parse():
    parser = Parser()
    full_sample = parser.parse("csv/NASDAQ_AAPL.txt")
    up_trends_list = parser.get_up_trends(full_sample)
    down_trends_list = parser.get_down_trends(full_sample)
    parser.set_candle_data(full_sample)

    print("=========UP TRENDS==========")
    print_list(up_trends_list)
    print("=========DOWN TRENDS==========")
    print_list(down_trends_list)
    print("=========FULL DATA WITH CANDLE INFO===========")
    for r in full_sample.records:
        print(r)


def run():
    parser = Parser()
    full_sample = parser.parse_wo_ticker("csv/AAPL.csv")

    parser.set_candle_data(full_sample)

    print_sample(full_sample)


if __name__ == '__main__':
    # run_old_parse()
    run()