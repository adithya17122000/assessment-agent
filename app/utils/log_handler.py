import logging
from logging.handlers import RotatingFileHandler

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

file_handler = RotatingFileHandler(
    "logs/app.log",          # Creates logs/app.log
    maxBytes=30 * 1024 * 1024,
    backupCount=5,
)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logging.basicConfig(
    level=logging.INFO,
    handlers=[console_handler, file_handler],
)