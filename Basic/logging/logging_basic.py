# logging_basic.py
"""Basic logging example."""

import logging
from pathlib import Path

# Create log file
log_file: Path = Path(__file__).parent / "logging_basic.log"

# Configure logging
logging.basicConfig(
    filename=log_file,
    filemode="w",
    level=logging.DEBUG,
    # format="%(asctime)s - %(levelname)s - %(module)s - %(message)s", # old style
    # format="{asctime} - {levelname} - {module} - {funcName} - {message}", # new style
    format="{asctime} - {levelname} - {module} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger: logging.Logger = logging.getLogger(name=__name__)

# log messages
logger.debug("This is a debug message")

logger.info("This is an info message")

logger.warning("This is a warning message")

logger.error("This is an error message")

logger.critical("This is a critical message")
