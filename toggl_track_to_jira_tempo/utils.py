import os
import logging

DEBUG = bool(os.environ.get("DEBUG", False))

LOG_FORMAT = "%(levelname)-8s:: %(message)s"

if DEBUG:
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
else:
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


class Logger:
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    CYAN = "\033[96m"

    @staticmethod
    def log_info(message: str, color=None) -> None:
        color = color or Logger.BLUE
        logging.info(color + message + Logger.RESET)

    @staticmethod
    def log_success(message: str) -> None:
        logging.info(Logger.GREEN + message + Logger.RESET)

    @staticmethod
    def log_error(message: str) -> None:
        logging.error(Logger.RED + message + Logger.RESET)

    @staticmethod
    def log_debug(message: str) -> None:
        logging.debug(Logger.YELLOW + message + Logger.RESET)
