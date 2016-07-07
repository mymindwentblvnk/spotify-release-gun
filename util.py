from config import LAST_UPDATE_PATH
import os.path

def loadLastUpdate():
    # If file already exists
    if os.path.exists(LAST_UPDATE_PATH):
        file = open(LAST_UPDATE_PATH, "r")
    else:
        pass

def saveLastUpdate():
    pass