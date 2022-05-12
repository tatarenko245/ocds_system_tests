import datetime

import pytz


def ei_period(start=0, end=90):
    date = datetime.datetime.now()
    duration_date_start = date + datetime.timedelta(days=start)
    start_date = duration_date_start.strftime('%Y-%m-%dT%H:%M:%SZ')
    duration_date_end = date + datetime.timedelta(days=end)
    end_date = duration_date_end.strftime('%Y-%m-%dT%H:%M:%SZ')
    return start_date, end_date


def pn_period():
    date = datetime.datetime.now()
    duration_date_start = date + datetime.timedelta(days=31)
    start_date = duration_date_start.strftime('%Y-%m-01T%H:%M:%SZ')
    return start_date


def contact_period(max_duration_of_fa=None):
    date = datetime.datetime.now()
    if max_duration_of_fa is None:
        duration_date_start = date + datetime.timedelta(days=60)
        start_date = duration_date_start.strftime('%Y-%m-%dT%H:%M:%SZ')
        duration_date_end = date + datetime.timedelta(days=80)
        end_date = duration_date_end.strftime('%Y-%m-%dT%H:%M:%SZ')
    else:
        days = int(max_duration_of_fa) / 60 / 60 / 24
        duration_date_start = date + datetime.timedelta(days=1)
        start_date = duration_date_start.strftime('%Y-%m-%dT%H:%M:%SZ')
        duration_date_end = date + datetime.timedelta(days=days-1)
        end_date = duration_date_end.strftime('%Y-%m-%dT%H:%M:%SZ')
    return start_date, end_date


def old_period():
    date = datetime.datetime.now()
    duration_date_start = date - datetime.timedelta(days=365)
    start_date = duration_date_start.strftime('%Y-%m-%dT%H:%M:%SZ')
    duration_date_end = date - datetime.timedelta(days=350)
    end_date = duration_date_end.strftime('%Y-%m-%dT%H:%M:%SZ')
    return start_date, end_date


def pre_qualification_period_end_date(interval_seconds: int):
    date = datetime.datetime.now(pytz.utc)
    duration_date_end = date + datetime.timedelta(seconds=interval_seconds)
    end_date = duration_date_end.strftime('%Y-%m-%dT%H:%M:%SZ')
    return end_date
