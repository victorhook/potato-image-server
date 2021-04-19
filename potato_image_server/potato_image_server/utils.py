from datetime import datetime
import calendar


DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M'


def datetime_to_date_and_time(_datetime: datetime):
    date = _datetime.strftime(DATE_FORMAT)
    time = _datetime.strftime(TIME_FORMAT)
    return date, time


def dateify_sample(sample):
    date, time = datetime_to_date_and_time(sample.date)
    sample.date = date
    sample.time = time
    return sample


def get_weekday(date: str) -> str:
    weekday = datetime.strptime(date, DATE_FORMAT).weekday()
    return calendar.day_name[weekday]
    