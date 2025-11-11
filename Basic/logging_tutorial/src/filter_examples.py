# filter_examples.py
"""
Additional examples showing how to use logging filters in real-world scenarios.
This complements custom_logging.py with more specific use cases.
"""

import logging
import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()


# ============================================================================
# EXAMPLE 1: Filter by Specific User ID (useful for debugging specific users)
# ============================================================================
class UserIdFilter(logging.Filter):
    """Only show logs for a specific user ID."""

    def __init__(self, user_id: str):
        super().__init__()
        self.user_id = user_id

    def filter(self, record: logging.LogRecord) -> bool:
        """Only allow logs for the specified user."""
        return getattr(record, "user_id", None) == self.user_id


# ============================================================================
# EXAMPLE 2: Filter by Request ID (useful for tracing specific requests)
# ============================================================================
class RequestIdFilter(logging.Filter):
    """Only show logs for a specific request ID."""

    def __init__(self, request_id: str):
        super().__init__()
        self.request_id = request_id

    def filter(self, record: logging.LogRecord) -> bool:
        """Only allow logs for the specified request."""
        return getattr(record, "request_id", None) == self.request_id


# ============================================================================
# EXAMPLE 3: Exclude Noisy Modules (filter out verbose third-party libraries)
# ============================================================================
class ExcludeModulesFilter(logging.Filter):
    """Exclude logs from noisy modules (e.g., third-party libraries)."""

    def __init__(self, excluded_modules: list[str]):
        super().__init__()
        self.excluded_modules = excluded_modules

    def filter(self, record: logging.LogRecord) -> bool:
        """Exclude logs from specified modules."""
        return record.module not in self.excluded_modules


# ============================================================================
# EXAMPLE 4: Rate Limiting Filter (prevent log spam)
# ============================================================================
class RateLimitFilter(logging.Filter):
    """Limit the rate of log messages to prevent spam."""

    def __init__(self, max_logs_per_minute: int = 60):
        super().__init__()
        self.max_logs = max_logs_per_minute
        self.log_count = 0
        self.last_reset_time = None
        import time

        self.time = time

    def filter(self, record: logging.LogRecord) -> bool:
        """Allow only max_logs messages per minute."""
        current_time = self.time.time()

        # Reset counter every minute
        if self.last_reset_time is None or current_time - self.last_reset_time >= 60:
            self.log_count = 0
            self.last_reset_time = current_time

        # Check if we've exceeded the limit
        if self.log_count < self.max_logs:
            self.log_count += 1
            return True
        return False


# ============================================================================
# EXAMPLE 5: Environment-based Filter (different logs for dev/staging/prod)
# ============================================================================
class EnvironmentFilter(logging.Filter):
    """Filter logs based on environment (dev, staging, production)."""

    def __init__(self, allowed_environments: list[str]):
        super().__init__()
        self.allowed_environments = allowed_environments
        self.current_env = os.getenv("ENVIRONMENT", "development")

    def filter(self, record: logging.LogRecord) -> bool:
        """Only allow logs in specified environments."""
        return self.current_env in self.allowed_environments


# ============================================================================
# EXAMPLE 6: PII (Personally Identifiable Information) Filter
# ============================================================================
class PIIFilter(logging.Filter):
    """Exclude logs containing PII (emails, phone numbers, SSN, etc.)."""

    def __init__(self):
        super().__init__()
        import re

        # Simple patterns for demonstration
        self.email_pattern = re.compile(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        )
        self.phone_pattern = re.compile(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b")
        self.ssn_pattern = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")

    def filter(self, record: logging.LogRecord) -> bool:
        """Exclude logs that might contain PII."""
        message = record.getMessage()

        # Block if any PII pattern is found
        if self.email_pattern.search(message):
            return False
        if self.phone_pattern.search(message):
            return False
        if self.ssn_pattern.search(message):
            return False

        return True


# ============================================================================
# EXAMPLE 7: Performance Filter (only log slow operations)
# ============================================================================
class PerformanceFilter(logging.Filter):
    """Only log operations that exceed a certain duration."""

    def __init__(self, min_duration_ms: float = 100.0):
        super().__init__()
        self.min_duration = min_duration_ms

    def filter(self, record: logging.LogRecord) -> bool:
        """Only allow logs for operations exceeding min_duration."""
        duration = getattr(record, "duration_ms", 0)
        return duration >= self.min_duration


# ============================================================================
# Demo: Using the filters
# ============================================================================
if __name__ == "__main__":
    # Setup logger
    logger = logging.getLogger(__name__)
    logger.setLevel(getattr(logging, LOG_LEVEL))

    formatter = logging.Formatter(
        fmt="{asctime} - {levelname} - [User:{user_id}] [Req:{request_id}] - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M:%S",
        defaults={"user_id": "N/A", "request_id": "N/A", "duration_ms": 0},
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, LOG_LEVEL))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    print("=" * 70)
    print("FILTER EXAMPLES DEMONSTRATION")
    print("=" * 70)

    # Example 1: Filter by User ID
    print("\n1. Filter by User ID (only user123):")
    user_filter = UserIdFilter(user_id="user123")
    console_handler.addFilter(user_filter)

    logger.info(
        "Login successful", extra={"user_id": "user123", "request_id": "req-001"}
    )
    logger.info(
        "Login successful", extra={"user_id": "user456", "request_id": "req-002"}
    )  # Filtered out

    console_handler.removeFilter(user_filter)

    # Example 2: Filter by Request ID
    print("\n2. Filter by Request ID (only req-003):")
    request_filter = RequestIdFilter(request_id="req-003")
    console_handler.addFilter(request_filter)

    logger.info(
        "Processing payment", extra={"user_id": "user789", "request_id": "req-003"}
    )
    logger.info(
        "Processing payment", extra={"user_id": "user101", "request_id": "req-004"}
    )  # Filtered out

    console_handler.removeFilter(request_filter)

    # Example 3: Exclude noisy modules
    print("\n3. Exclude noisy modules (excluding 'boto3', 'urllib3'):")
    exclude_filter = ExcludeModulesFilter(excluded_modules=["boto3", "urllib3"])
    console_handler.addFilter(exclude_filter)

    logger.info("Application log - this will show")
    # Simulating logs from excluded modules would be filtered

    console_handler.removeFilter(exclude_filter)

    # Example 4: Rate limiting
    print("\n4. Rate limiting (max 5 logs per minute):")
    rate_filter = RateLimitFilter(max_logs_per_minute=5)
    console_handler.addFilter(rate_filter)

    for i in range(10):
        logger.info(f"Log message {i + 1}")  # Only first 5 will show

    console_handler.removeFilter(rate_filter)

    # Example 5: Environment-based filtering
    print("\n5. Environment-based filtering (only in development):")
    env_filter = EnvironmentFilter(allowed_environments=["development", "staging"])
    console_handler.addFilter(env_filter)

    logger.debug("Debug info - only in dev/staging")

    console_handler.removeFilter(env_filter)

    # Example 6: PII filtering
    print("\n6. PII filtering (blocks emails, phones, SSN):")
    pii_filter = PIIFilter()
    console_handler.addFilter(pii_filter)

    logger.info("User registered successfully")  # Shows
    logger.info("User email: john.doe@example.com")  # Filtered out
    logger.info("Contact: 555-123-4567")  # Filtered out

    console_handler.removeFilter(pii_filter)

    # Example 7: Performance filtering
    print("\n7. Performance filtering (only operations > 100ms):")
    perf_filter = PerformanceFilter(min_duration_ms=100.0)
    console_handler.addFilter(perf_filter)

    logger.info("Fast operation", extra={"duration_ms": 50})  # Filtered out
    logger.warning("Slow operation", extra={"duration_ms": 250})  # Shows

    console_handler.removeFilter(perf_filter)

    print("\n" + "=" * 70)
    print("✅ All filter examples completed!")
    print("=" * 70)
