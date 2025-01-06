from collections import namedtuple
import os
import logging

DEBUG = bool(os.environ.get("DEBUG", False))

# LOG_FORMAT = "%(levelname)-8s:: %(message)s"
LOG_FORMAT = "        %(message)s"

if DEBUG:
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
else:
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


HoursLog = namedtuple("HourLog", ["date", "hours"])

class Logger:
    _BLUE = "\033[94m"
    _GREEN = "\033[92m"
    _RED = "\033[31m"
    _BRIGHT_RED = "\033[91m"
    _YELLOW = "\033[93m"
    _RESET = "\033[0m"
    _CYAN = "\033[96m"
    _ORANGE = "\033[33m"

    _BACKGROUND_BRIGHT_RED = "\033[101m"
    _BACKGROUND_BRIGHT_YELLOW = "\033[103m"

    INFO = _BLUE
    INFO_SECONDARY = _CYAN
    SUCCESS = _GREEN
    ERROR = _RED
    WARNING = _ORANGE
    DEBUG = _YELLOW

    HIGHLIGHT_WARNING = _BACKGROUND_BRIGHT_YELLOW
    HIGHLIGHT_ERROR = _BACKGROUND_BRIGHT_RED

    @staticmethod
    def format_message(message: str, color=None) -> str:
        color = color or Logger.INFO
        return color + message + Logger._RESET

    @staticmethod
    def log_info_raw(message: str) -> None:
        logging.info(message)

    @staticmethod
    def log_info(message: str, color=None) -> None:
        color = color or Logger.INFO
        logging.info(color + message + Logger._RESET)

    @staticmethod
    def log_warning(message: str) -> None:
        logging.warning(Logger.WARNING + message + Logger._RESET)

    @staticmethod
    def log_success(message: str) -> None:
        logging.info(Logger.SUCCESS + message + Logger._RESET)

    @staticmethod
    def log_error(message: str) -> None:
        logging.error(Logger.ERROR + message + Logger._RESET)

    @staticmethod
    def log_debug(message: str) -> None:
        logging.debug(Logger.DEBUG + message + Logger._RESET)
