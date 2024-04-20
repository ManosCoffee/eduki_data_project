import logging
from typing import Dict, Optional



class ColorLogFormatter(logging.Formatter):
    """
    Class of custom log formatter
    """

    grey: str = "\x1b[38;20m"
    blue: str = "\x1b[1;34m"
    yellow: str = "\x1b[33;20m"
    red: str = "\x1b[31;20m"
    bold_red: str = "\x1b[31;1m"
    reset: str = "\x1b[0m"

    format1: str = "%(asctime)s | "
    format2: str = "%(levelname)s "
    format3: str = "| %(message)s"

    FORMATS: Dict[int, str] = {
        logging.DEBUG: format1 + grey + format2 + reset + format3,
        logging.INFO: format1 + blue + format2 + reset + format3,
        logging.WARNING: format1 + yellow + format2 + reset + format3,
        logging.ERROR: format1 + red + format2 + reset + format3,
        logging.CRITICAL: format1 + bold_red + format2 + reset + format3,
    }

    def format(self, record: logging.LogRecord) -> str:
        """
        Implements logging.formatter.format with the custom format settings.
        """
        record.name = record.filename.split(".py")[0].replace("_", "")
        log_fmt: Optional[str] = self.FORMATS.get(record.levelno)
        formatter: logging.Formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
