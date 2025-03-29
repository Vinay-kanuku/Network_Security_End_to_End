import logging
import os

# Create a logs directory if it doesn't exist
log_dir = os.path.join(os.path.dirname(__file__), "logs")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Set up the logging configuration
def setup_logger():
    """
    Sets up a custom logger with both file and console handlers.
    The logger writes logs to a specified log file and outputs logs to the console.
    Both handlers use the DEBUG log level by default, and the log format includes
    the timestamp, logger name, log level, and message.
    Returns:
        logging.Logger: A configured logger instance.
    """
    # Create a logger object
    logger = logging.getLogger("CustomLogger")
    logger.setLevel(logging.DEBUG)  # Set the log level to DEBUG (can be changed based on needs)

    # Define the log file path
    log_file = os.path.join(log_dir, "logger.log")

    # Create a file handler to write logs to the log file
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)  # Set the log level for the file handler
    
    # Create a stream handler to output logs to the console
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)  # Set the log level for the stream handler
    
    # Define a log format (can be customized)
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Apply the log format to both handlers
    file_handler.setFormatter(log_format)
    stream_handler.setFormatter(log_format)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger

# Instantiate the logger and set it up
logging = setup_logger()