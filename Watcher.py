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

    @staticmethod
    def parse(a_filepath):
        sample = Sample()
        file_reader = csv.reader(open(a_filepath, newline=''), delimiter=',', quotechar='|')
        for row in file_reader:
            record = Record()
            record.add(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            sample.add_record(record)
        sample.records.pop(0)
        return sample

    @staticmethod
    def set_resolution(data, resolution, beg="", end=""):

        if beg == "":
            beg = data.records[0].date
        if end == "":
            len = data.records.__len__()
            end = data.records[len - 1].date

        sample = Sample()
        index = 0
        resolution_modifier = int(resolution / 5)

        while index < data.records.__len__() - resolution_modifier:

            if data.records[index].date >= beg and data.records[index + (resolution_modifier - 1)].date <= end:
                new_ticker = data.records[index].ticker
                new_date = data.records[index + (resolution_modifier - 1)].date
                new_open = data.records[index].open

                tmp_list = list()
                for i in range(0, resolution_modifier):
                    tmp_list.append(data.records[index + i].high)
                new_high = max(tmp_list)

                tmp_list.clear()
                for i in range(0, resolution_modifier):
                    tmp_list.append(data.records[index + i].low)
                new_low = min(tmp_list)

                new_close = data.records[index + resolution_modifier - 1].close

                tmp_list.clear()
                for i in range(0, resolution_modifier):
                    tmp_list.append(int(data.records[index + i].vol))
                new_volume = sum(tmp_list)

                record = Record()
                record.add(new_ticker, new_date, new_open, new_high, new_low, new_close, str(new_volume))
                sample.add_record(record)
            index += 3

        return sample;

    @staticmethod
    def set_candle_data(data):
        for row in data.records:

            body_size = math.fabs(float(row.open) - float(row.close))
            upper_shadow = float(row.high) - float(row.close)
            lower_shadow = float(row.open) - float(row.low)
            full_range = float(row.high) - float(row.low)

            # Candle color
            if float(row.open) < float(row.close):
                row.candle_color = "green"
            elif float(row.open) > float(row.close):
                row.candle_color = "red"
                upper_shadow = float(row.high) - float(row.open)
                lower_shadow = float(row.close) - float(row.low)
            elif float(row.open) == float(row.close):
                row.candle_color = "none"

            # Don't bother trying to assign a candle_type if the full_range is 0
            if full_range == 0:
                continue

            # Marubozu
            if (float(row.open) == float(row.low) and float(row.close) == float(row.high)) or\
               (float(row.open) == float(row.high) and float(row.close) == float(row.low)):
                row.candle_type = "marubozu"

            # Long Upper Shadow
            if row.candle_color == "red" and\
               upper_shadow >= 0.66 * full_range and\
               lower_shadow <= 0.33 * full_range and\
               float(row.close) != float(row.low):
                row.candle_type = "longUpperShadow"

            # Long Lower Shadow
            if row.candle_color == "green" and\
               upper_shadow <= 0.33 * full_range and\
               lower_shadow >= 0.66 * full_range and\
               float(row.close) != float(row.high):
                row.candle_type = "longLowerShadow"

            # Spinning Top
            if 0.33 * full_range >= body_size >= 0.10 * full_range and\
               upper_shadow >= 2.5 * body_size and\
               lower_shadow >= 2.5 * body_size and\
               math.fabs(upper_shadow / full_range - lower_shadow / full_range) < 0.20:
                row.candle_type = "spinningTop"

            # Doji
            if 0.10 * full_range >= body_size:
                if upper_shadow == 0:
                    row.candle_type = "dragonflyDoji"
                if lower_shadow == 0:
                    row.candle_type = "gravestoneDoji"
                if upper_shadow >= 8 * body_size and\
                   lower_shadow >= 8 * body_size and\
                   math.fabs(upper_shadow / full_range - lower_shadow / full_range) < 0.20:
                    row.candle_type = "longLeggedDoji"
                else:
                    row.candle_type = "doji"

            # Hammer / Hanging Man
            if 0.33 * full_range >= body_size >= 0.10 * full_range and\
               upper_shadow <= 1 * body_size and\
               lower_shadow >= 3 * body_size:
                if row.candle_color == "green":
                    row.candle_type = "hammer"
                elif row.candle_color == "red":
                    row.candle_type = "hangingMan"

            if row.date == "2018-01-23":
                i = 0

            # Inverted Hammer / Shooting Star
            if 0.33 * full_range >= body_size >= 0.05 * full_range and\
               upper_shadow >= 3 * body_size and\
               lower_shadow <= 1 * body_size:
                if row.candle_color == "green":
                    row.candle_type = "invertedHammer"
                elif row.candle_color == "red":
                    row.candle_type = "shootingStar"


def run():
    parser = Parser()
    sample_5m = parser.parse("csv/NASDAQ_AAPL.csv")
    sample_15m = parser.set_resolution(sample_5m, 15, "201010110915", "201010110955")
    # sample_30m = parser.set_resolution(sample_5m, 30)
    # sample_60m = parser.set_resolution(sample_5m, 60)

    sample_15m.print()
    # sample_30m.print()
    # sample_60m.print()


if __name__ == '__main__':
    run()
