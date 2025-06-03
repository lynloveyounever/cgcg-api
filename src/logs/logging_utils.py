import logging
import os

def setup_logging(level=logging.INFO, log_file=None):
    """
    Configures logging for the application.

    Args:
        level (int): The minimum logging level (e.g., logging.INFO, logging.DEBUG).
        log_file (str, optional): Path to a file to log to. If None, logs to console.
    """
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    handlers = []

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(logging.Formatter(log_format))
    handlers.append(console_handler)

    # File handler (if log_file is provided)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(logging.Formatter(log_format))
        handlers.append(file_handler)

    logging.basicConfig(level=level, format=log_format, handlers=handlers)

# Example usage:
# In your main application file (e.g., main.py), call setup_logging()
# from app.utils.logging_utils import setup_logging
# setup_logging(level=logging.DEBUG, log_file="app.log")
