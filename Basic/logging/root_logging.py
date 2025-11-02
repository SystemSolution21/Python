# root_logging.py
"""
This script demonstrates the use of root logging.
Root logging is the default logger that is used when no other logger is specified.
"""

import logging
from pathlib import Path

# Create log file
log_file: Path = Path(__file__).parent / "root_logging.log"

# Configure logging
logging.basicConfig(
    filename=log_file,
    encoding="utf-8",
    filemode="w",
    level=logging.DEBUG,
    # format="%(asctime)s - %(levelname)s - %(module)s - %(message)s", # old style
    # format="{asctime} - {levelname} - {module} - {funcName} - {message}", # new style
    format="{asctime} - {levelname} - {module} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# log messages
logging.debug("This is a debug message")

logging.info("This is an info message")

logging.warning("This is a warning message")

logging.error("This is an error message")

logging.critical("This is a critical message")


def calculate_donuts() -> int | None:
    """Capture stack trace."""
    donuts: int = 1
    people: int = 0

    # try:
    #     donuts_per_person: int = int(donuts / people)
    #     logging.info(f"Donuts per person: {donuts_per_person}")
    #     return donuts_per_person
    # except ZeroDivisionError:
    #     logging.error("Donuts calculation error!", exc_info=True)

    try:
        donuts_per_person: int = int(donuts / people)
        logging.info(f"Donuts per person: {donuts_per_person}")
        return donuts_per_person
    except ZeroDivisionError:
        logging.exception("Donuts calculation error!")


# Calculate donuts
calculate_donuts()
