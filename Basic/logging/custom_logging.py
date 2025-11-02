# custom_logging.py
"""
This script demonstrates the use of custom logging.
Custom logging allows you to create multiple loggers with different configurations.
This is useful when you want to log messages from different parts of your application
with different levels of detail.
"""

import logging
from pathlib import Path

# Create log file
log_file: Path = Path(__file__).parent / "custom_logging.log"


# Filter logging levels
def show_only_debug(record: logging.LogRecord) -> bool:
    """Show only debug messages."""
    return record.levelno == logging.DEBUG


# Custom logger
logger: logging.Logger = logging.getLogger(name=__name__)
logger.setLevel(level=logging.DEBUG)

# Format log messages
formatter: logging.Formatter = logging.Formatter(
    fmt="{asctime} - {levelname} - {module} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Console Handlers
console_handler: logging.StreamHandler = logging.StreamHandler()
console_handler.setLevel(level=logging.DEBUG)
console_handler.addFilter(filter=show_only_debug)
console_handler.setFormatter(fmt=formatter)
logger.addHandler(hdlr=console_handler)

# File handler
file_handler: logging.FileHandler = logging.FileHandler(
    filename=log_file, mode="w", encoding="utf-8"
)
file_handler.setLevel(level=logging.INFO)
file_handler.setFormatter(fmt=formatter)
logger.addHandler(hdlr=file_handler)

# Log messages
logger.debug("Just checking in!")
logger.info("All is well!")
logger.warning("Stay curious!")
logger.error("Stay put!")
