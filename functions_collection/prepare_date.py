import datetime


def ei_period(start=0, end=90):
    date = datetime.datetime.now()
    duration_date_start = date + datetime.timedelta(days=start)
    start_date = duration_date_start.strftime('%Y-%m-%dT%H:%M:%SZ')
    duration_date_end = date + datetime.timedelta(days=end)
    end_date = duration_date_end.strftime('%Y-%m-%dT%H:%M:%SZ')
    return start_date, end_date
