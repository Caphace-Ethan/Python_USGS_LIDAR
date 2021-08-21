# Import packages for logging
import log
import log.handlers
import os


def logger(filename):
    handler = log.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", f"../logs/{filename}.log"))
    formatter = log.Formatter(log.BASIC_FORMAT)
    handler.setFormatter(formatter)
    root = log.getLogger()
    root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
    root.addHandler(handler)
    # logging.info("Testing Loggings")