from config import LAST_UPDATE_PATH
import os.path
import datetime

DATE_FORMAT = "%Y-%m-%d"

def getLastUpdate():

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

        saveLastUpdate(date)

    return date.rstrip()

def saveLastUpdate(date=None):
    # Save the next day
    if date == None:
        today = datetime.datetime.now()
        oneDay = datetime.timedelta(days=1)
        todayPlusOne = today + oneDay
        date = todayPlusOne.strftime(DATE_FORMAT)

    file = open(LAST_UPDATE_PATH, "w")
    file.write(date)
    return date