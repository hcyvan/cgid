import time
import datetime


def timestamp2week_label(ts):
    if ts:
        ts = float(ts)
    else:
        ts = time.time()
    date_time = datetime.datetime.fromtimestamp(ts)
    monday = date_time.date() - datetime.timedelta(days=(date_time.isoweekday() - 1))
    return monday.strftime('%Y%m%d')


def timestamp2day_label(ts):
    if ts:
        ts = float(ts)
    else:
        ts = time.time()
    date_time = datetime.datetime.fromtimestamp(ts)
    return date_time.strftime('%Y%m%d')
