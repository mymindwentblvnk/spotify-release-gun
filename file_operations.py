from config import LAST_UPDATE_PATH
import os.path
import datetime
import pickle
from config import SPOTIFY_CACHE_PATH


DATE_FORMAT = "%Y-%m-%d"


def get_last_update():
    """
    Returns the last update date.
    :return: Last update date.
    """

    date = None

    # If file already exists
    if os.path.exists(LAST_UPDATE_PATH):
        # Load and return date in file
        with open(LAST_UPDATE_PATH, "r") as file:
            date = file.readline()
    else:
        # If not create file with "today - one week"
        today = datetime.datetime.now()
        seven_days = datetime.timedelta(days=7)
        today_minus_seven = today - seven_days
        date = today_minus_seven.strftime(DATE_FORMAT)

        save_last_update(date)

    return date.rstrip()


def save_last_update(date=None):
    """
    Saves a given date in the YYYY-mm-dd format.
    :param date: Date to save. If no date is given "tommorow" will be saved.
    :return: Date string that was saved.
    """
    # Save the next day
    if date is None:
        today = datetime.datetime.now()
        one_day = datetime.timedelta(days=1)
        today_plus_one = today + one_day
        date = today_plus_one.strftime(DATE_FORMAT)

    with open(LAST_UPDATE_PATH, "w") as file:
        file.write(date)
    return date


def save_spotify_cache(cache):
    """
    Saves the Spotify cache.
    :param cache: Array of Spotify album ids.
    :return: True if successful, False if not.
    """
    try:
        with open(SPOTIFY_CACHE_PATH, "wb") as cache_file:
            pickle.dump(cache, cache_file)
        result = True
    except:
        result = False

    return result


def load_spotify_cache():
    """
        Loads the Spotify cache as a array of Spotify albumd ids as strings.
        :return: Array of Spotify album ids
        """
    try:
        with open(SPOTIFY_CACHE_PATH, "rb") as cache_file:
            result = pickle.load(cache_file)
    except FileNotFoundError:
        result = []

    return result
