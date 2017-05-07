import os
import settings
import datetime


def save_last_update_date(date=None):
    if not date:
        today = datetime.datetime.now()
        one_day = datetime.timedelta(days=1)
        today_plus_one = today + one_day
        date = today_plus_one.strftime(settings.DATE_FORMAT)
    with open(settings.LAST_UPDATE_PATH, "w") as out:
        out.write(date)
    return date


def get_last_update_date():
    if os.path.exists(settings.LAST_UPDATE_PATH):
        # Load and return date in file
        with open(settings.LAST_UPDATE_PATH, "r") as file:
            date = file.readline()
    else:
        # If not create file with "today - one week"
        today = datetime.datetime.now()
        seven_days = datetime.timedelta(days=7)
        today_minus_seven = today - seven_days
        date = today_minus_seven.strftime(settings.DATE_FORMAT)
        save_last_update_date(date)
    return date.rstrip()
