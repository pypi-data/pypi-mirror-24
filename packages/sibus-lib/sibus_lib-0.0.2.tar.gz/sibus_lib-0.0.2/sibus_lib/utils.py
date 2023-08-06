#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime as dt
import random

def nice_float(value):
    return float("%.6f" % float(value))

def parse_num(s):
    try:
        return int(s)
    except ValueError:
        try:
            return nice_float(s)
        except ValueError:
            return s

def datetime_now():
    return dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")

def random_value(value, percent_range=30):
    t = (random.random() - 0.5)*(percent_range/100.0)
    return value * (1+t)

def datetime_to_float(d):
    epoch = dt.datetime.utcfromtimestamp(0)
    total_seconds =  (d - epoch).total_seconds()
    # total_seconds will be in decimals (millisecond precision)
    return total_seconds

def float_to_datetime(fl):
    return dt.datetime.fromtimestamp(fl)

def datetime_now_float():
    return datetime_to_float(dt.datetime.utcnow())

