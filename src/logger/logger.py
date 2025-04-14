import logging
import os

# Create a logs directory if it doesn't exist
log_dir = os.path.join(os.path.dirname(__file__), "logs")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)


def setup_logger():
    logger = logging.getLogger("CustomLogger")
    logger.setLevel(logging.DEBUG)

    log_file = os.path.join(log_dir, "logger.log")
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)

    log_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(log_format)
    stream_handler.setFormatter(log_format)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


# Do NOT override 'logging' module
logger = setup_logger()
