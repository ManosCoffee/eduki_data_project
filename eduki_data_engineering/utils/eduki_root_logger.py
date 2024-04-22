import logging
import sys
from eduki_data_engineering.utils.color_log_formatter import ColorLogFormatter

def configure_root_logger(log_level=logging.DEBUG):
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Create and configure a StreamHandler with your ColorLogFormatter
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    formatter = ColorLogFormatter()
    console_handler.setFormatter(formatter)

    # Add the console handler to the root logger
    root_logger.addHandler(console_handler)