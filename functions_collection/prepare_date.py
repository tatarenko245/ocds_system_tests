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


def enquiry_period(tenderperiod_startdate):
    tenderperiod_startdate = datetime.datetime.strptime(tenderperiod_startdate, "%Y-%m-%dT%H:%M:%SZ")
    duration_date_end = tenderperiod_startdate - datetime.timedelta(days=4)
    end_date = duration_date_end.strftime('%Y-%m-01T%H:%M:%SZ')
    return end_date


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


def framework_agreement_enquiry_period_end_date(pre_qual_period_end_date, interval_seconds: int):
    duration_date_end = datetime.datetime.strptime(
        pre_qual_period_end_date, '%Y-%m-%dT%H:%M:%SZ') - datetime.timedelta(seconds=interval_seconds)
    end_date = duration_date_end.strftime('%Y-%m-%dT%H:%M:%SZ')
    return end_date


def get_min_date(dates_list):
    new_dates_list = list()
    for d in range(len(dates_list)):
        new_dates_list.append(datetime.datetime.strptime(dates_list[d], "%Y-%m-%dT%H:%M:%SZ"))
    min_date = min(new_dates_list)
    return min_date.strftime('%Y-%m-%dT%H:%M:%SZ')


def get_actual_datetime():
    date = datetime.datetime.now()
    actual_date = date.strftime('%Y-%m-%dT%H:%M:%SZ')
    return actual_date


def is_the_date_within_range(first_date, second_date):
    """Check that the date is within range"""
    is_it_ok = False
    first_date = datetime.datetime.strptime(first_date, '%Y-%m-%dT%H:%M:%SZ')
    second_date = datetime.datetime.strptime(second_date, '%Y-%m-%dT%H:%M:%SZ')
    if first_date >= second_date:
        date_diff = first_date - second_date
    else:
        date_diff = second_date - first_date

    date_diff_as_sec = date_diff.seconds
    if date_diff_as_sec <= 3:
        is_it_ok = True
    return is_it_ok
