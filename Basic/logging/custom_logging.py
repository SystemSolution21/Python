# custom_logging.py
"""
This script demonstrates advanced logging with filters and .env configuration.
Shows real-world use cases:
1. Module-specific filtering
2. Custom condition filtering (message content, user ID, request ID)
3. Specialized handlers (errors to email, warnings to Slack simulation)
"""

# import standard modules
import logging
import os
from pathlib import Path

# import third party modules
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get logging level from environment variable
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()

# Create log files
log_file: Path = Path(__file__).parent / "custom_logging.log"
error_file: Path = Path(__file__).parent / "errors.log"
slack_file: Path = Path(__file__).parent / "slack_warnings.log"


# ============================================================================
# FILTER 1: Specific Module Filtering
# ============================================================================
class ModuleFilter(logging.Filter):
    """Only show logs from specific modules."""

    def __init__(self, allowed_modules: list[str]):
        super().__init__()
        self.allowed_modules = allowed_modules

    def filter(self, record: logging.LogRecord) -> bool:
        """Return True if record is from an allowed module."""
        return record.module in self.allowed_modules


# ============================================================================
# FILTER 2: Custom Conditions (message content, user ID, request ID)
# ============================================================================
class CustomConditionFilter(logging.Filter):
    """Filter by message content, user ID, request ID, etc."""

    def __init__(
        self,
        exclude_keywords: list[str] | None = None,
        required_user_id: str | None = None,
        required_request_id: str | None = None,
    ):
        super().__init__()
        self.exclude_keywords = exclude_keywords or []
        self.required_user_id = required_user_id
        self.required_request_id = required_request_id

    def filter(self, record: logging.LogRecord) -> bool:
        """Apply custom filtering logic."""
        # Exclude messages containing certain keywords
        for keyword in self.exclude_keywords:
            if keyword.lower() in record.getMessage().lower():
                return False

        # Filter by user_id if specified (must be added to LogRecord)
        if self.required_user_id:
            user_id = getattr(record, "user_id", None)
            if user_id != self.required_user_id:
                return False

        # Filter by request_id if specified
        if self.required_request_id:
            request_id = getattr(record, "request_id", None)
            if request_id != self.required_request_id:
                return False

        return True


# ============================================================================
# FILTER 3: Specialized Handlers (errors only, warnings only)
# ============================================================================
class ErrorOnlyFilter(logging.Filter):
    """Only allow ERROR and CRITICAL messages (for email handler)."""

    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno >= logging.ERROR


class WarningOnlyFilter(logging.Filter):
    """Only allow WARNING messages (for Slack handler)."""

    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno == logging.WARNING


# ============================================================================
# Logger Setup
# ============================================================================
logger: logging.Logger = logging.getLogger(name=__name__)
logger.setLevel(level=getattr(logging, LOG_LEVEL))

# Format log messages
formatter: logging.Formatter = logging.Formatter(
    fmt="{asctime} - {levelname} - {module} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Enhanced formatter with extra fields
enhanced_formatter: logging.Formatter = logging.Formatter(
    fmt="{asctime} - {levelname} - {module} - [User:{user_id}] [Req:{request_id}] - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S",
    defaults={"user_id": "N/A", "request_id": "N/A"},
)


# ============================================================================
# Handler 1: Console Handler (with module filtering)
# ============================================================================
console_handler: logging.StreamHandler = logging.StreamHandler()
console_handler.setLevel(level=getattr(logging, LOG_LEVEL))
# Only show logs from specific modules
console_handler.addFilter(ModuleFilter(allowed_modules=["custom_logging", "payment"]))
console_handler.setFormatter(fmt=enhanced_formatter)
logger.addHandler(hdlr=console_handler)


# ============================================================================
# Handler 2: File Handler (with custom condition filtering)
# ============================================================================
file_handler: logging.FileHandler = logging.FileHandler(
    filename=log_file, mode="w", encoding="utf-8"
)
file_handler.setLevel(level=logging.DEBUG)
# Exclude sensitive information from general logs
file_handler.addFilter(
    CustomConditionFilter(exclude_keywords=["password", "secret", "token"])
)
file_handler.setFormatter(fmt=enhanced_formatter)
logger.addHandler(hdlr=file_handler)


# ============================================================================
# Handler 3: Error Handler (simulating email alerts)
# ============================================================================
error_handler: logging.FileHandler = logging.FileHandler(
    filename=error_file, mode="w", encoding="utf-8"
)
error_handler.setLevel(level=logging.ERROR)
# Only errors and critical (would send to email in production)
error_handler.addFilter(ErrorOnlyFilter())
error_handler.setFormatter(fmt=enhanced_formatter)
logger.addHandler(hdlr=error_handler)


# ============================================================================
# Handler 4: Slack Handler (simulating Slack notifications)
# ============================================================================
slack_handler: logging.FileHandler = logging.FileHandler(
    filename=slack_file, mode="w", encoding="utf-8"
)
slack_handler.setLevel(level=logging.WARNING)
# Only warnings (would send to Slack in production)
slack_handler.addFilter(WarningOnlyFilter())
slack_handler.setFormatter(fmt=enhanced_formatter)
logger.addHandler(hdlr=slack_handler)


# ============================================================================
# Demo: Log messages with different scenarios
# ============================================================================
if __name__ == "__main__":
    print(f"Current LOG_LEVEL from .env: {LOG_LEVEL}\n")

    # Basic logging
    logger.debug("Just checking in!")
    logger.info("All is well!")
    logger.warning("Stay curious!")  # Goes to console, file, and Slack
    logger.error("Stay put!")  # Goes to console, file, and error handler

    # Logging with custom attributes (user_id, request_id)
    logger.info("User logged in", extra={"user_id": "user123", "request_id": "req-001"})
    logger.warning(
        "High memory usage detected",
        extra={"user_id": "user456", "request_id": "req-002"},
    )

    # These will be filtered out from file handler (contain excluded keywords)
    logger.info("User password updated successfully")  # Filtered from file
    logger.debug("API token: secret-key-123")  # Filtered from file

    # Error that goes to error handler (simulating email)
    logger.error(
        "Database connection failed!",
        extra={"user_id": "system", "request_id": "req-003"},
    )

    # Critical error
    logger.critical(
        "System shutdown imminent!",
        extra={"user_id": "system", "request_id": "req-004"},
    )

    print("\n✅ Logs written to:")
    print("   - Console (module filter applied)")
    print(f"   - {log_file} (keyword filter applied)")
    print(f"   - {error_file} (errors only)")
    print(f"   - {slack_file} (warnings only)")
