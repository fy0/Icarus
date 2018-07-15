import time
import datetime


def get_today_start_timestamp():
    today = datetime.date.today()
    return time.mktime(today.timetuple())
