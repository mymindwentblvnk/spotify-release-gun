from config import LOGGING_ON

def log(message):
    """
    Logs a message to the console if LOGGING_ON is set true
    :param message: Message to log
    """
    if LOGGING_ON:
        print(message)