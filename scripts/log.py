# Import packages for logging
import logging
import logging.handlers
import os


def logger(filename):
    handler = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", f"./logs/{filename}.log"))
    formatter = logging.Formatter(logging.BASIC_FORMAT)
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
    root.addHandler(handler)
    # logging.info("Testing Loggings")