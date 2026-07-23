import logging
import sys


FORMATTER_DATE = '[%(asctime)s][%(levelname)s]: %(name)s - %(message)s'

def get_logger(name: str):
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(FORMATTER_DATE)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
