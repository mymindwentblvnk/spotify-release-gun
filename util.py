from config import LAST_UPDATE_PATH
import os.path
import datetime
from config import LOGGING_ON

DATE_FORMAT = "%Y-%m-%d"


def get_last_update():

    date = None

    # If file already exists
    if os.path.exists(LAST_UPDATE_PATH):
        # Load and return date in file
        file = open(LAST_UPDATE_PATH, "r")
        date = file.readline()
    else:
        # If not create file with "today - one week"
        file = open(LAST_UPDATE_PATH, "w")

        today = datetime.datetime.now()
        sevenDays = datetime.timedelta(days=7)
        todayMinusSeven = today - sevenDays
        date = todayMinusSeven.strftime(DATE_FORMAT)

        save_last_update(date)

    return date.rstrip()


def save_last_update(date=None):
    # Save the next day
    if date is None:
        today = datetime.datetime.now()
        oneDay = datetime.timedelta(days=1)
        todayPlusOne = today + oneDay
        date = todayPlusOne.strftime(DATE_FORMAT)

    file = open(LAST_UPDATE_PATH, "w")
    file.write(date)
    return date


def log(message):
    """
    Logs a message to the console if LOGGING_ON is set true
    :param message: Message to log
    """
    if LOGGING_ON:
        print(message)
