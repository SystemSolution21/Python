# Logging Filters Best Practices

## Overview

This guide explains when and how to use `addFilter()` with environment-based logging configuration.

## ✅ Best Practice: Combine .env LOG_LEVEL with Filters

### Use .env for -

- **Overall log verbosity** (DEBUG, INFO, WARNING, ERROR)
- **Environment-specific settings** (dev vs production)
- **Easy configuration changes** without code deployment

### Use addFilter() for -

- **Specialized routing** (errors to email, warnings to Slack)
- **Conditional logging** (specific users, requests, modules)
- **Security/Privacy** (exclude PII, sensitive data)
- **Performance** (rate limiting, slow operation tracking)

---

## Real-World Use Cases

### 1. Module-Specific Filtering

**When to use:** Debug specific parts of your application without noise from other modules.

```python
class ModuleFilter(logging.Filter):
    def __init__(self, allowed_modules: list[str]):
        self.allowed_modules = allowed_modules
    
    def filter(self, record: logging.LogRecord) -> bool:
        return record.module in self.allowed_modules

# Usage
console_handler.addFilter(ModuleFilter(['payment', 'checkout']))
```

**Real-world scenario:**

- Debugging payment processing without seeing database logs
- Focusing on authentication module during security audit

---

### 2. Custom Conditions (User ID, Request ID)

**When to use:** Trace specific user sessions or API requests.

```python
class UserIdFilter(logging.Filter):
    def __init__(self, user_id: str):
        self.user_id = user_id
    
    def filter(self, record: logging.LogRecord) -> bool:
        return getattr(record, 'user_id', None) == self.user_id

# Usage
logger.info("Action performed", extra={'user_id': 'user123', 'request_id': 'req-001'})
```

**Real-world scenario:**

- Customer reports an issue → filter logs by their user_id
- Debugging a specific API request using request_id
- Compliance audit for specific user activity

---

### 3. Specialized Handlers (Email, Slack, etc.)

**When to use:** Route different log levels to different destinations.

```python
class ErrorOnlyFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno >= logging.ERROR

# Email handler - only errors
email_handler.addFilter(ErrorOnlyFilter())

class WarningOnlyFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno == logging.WARNING

# Slack handler - only warnings
slack_handler.addFilter(WarningOnlyFilter())
```

**Real-world scenario:**

- Send critical errors to PagerDuty/email for immediate action
- Send warnings to Slack for team awareness
- Send all logs to file/cloud storage for analysis

---

### 4. Exclude Sensitive Information

**When to use:** Prevent logging of passwords, tokens, PII.

```python
class SensitiveDataFilter(logging.Filter):
    def __init__(self, exclude_keywords: list[str]):
        self.exclude_keywords = exclude_keywords
    
    def filter(self, record: logging.LogRecord) -> bool:
        message = record.getMessage().lower()
        return not any(keyword in message for keyword in self.exclude_keywords)

# Usage
file_handler.addFilter(SensitiveDataFilter(['password', 'token', 'secret', 'api_key']))
```

**Real-world scenario:**

- GDPR/CCPA compliance - don't log PII
- Security - prevent credentials in logs
- Prevent accidental exposure in log aggregation tools

---

### 5. Rate Limiting

**When to use:** Prevent log spam from high-frequency events.

```python
class RateLimitFilter(logging.Filter):
    def __init__(self, max_logs_per_minute: int = 60):
        self.max_logs = max_logs_per_minute
        self.log_count = 0
        self.last_reset_time = None
    
    def filter(self, record: logging.LogRecord) -> bool:
        import time
        current_time = time.time()
        
        if self.last_reset_time is None or current_time - self.last_reset_time >= 60:
            self.log_count = 0
            self.last_reset_time = current_time
        
        if self.log_count < self.max_logs:
            self.log_count += 1
            return True
        return False
```

**Real-world scenario:**

- Prevent disk space issues from runaway logging
- Avoid overwhelming log aggregation services (Datadog, Splunk)
- Reduce costs in cloud logging (CloudWatch, Stackdriver)

---

### 6. Performance Monitoring

**When to use:** Only log slow operations for performance analysis.

```python
class PerformanceFilter(logging.Filter):
    def __init__(self, min_duration_ms: float = 100.0):
        self.min_duration = min_duration_ms
    
    def filter(self, record: logging.LogRecord) -> bool:
        duration = getattr(record, 'duration_ms', 0)
        return duration >= self.min_duration

# Usage
logger.info("Database query completed", extra={'duration_ms': 250})
```

**Real-world scenario:**

- Identify slow database queries
- Track API endpoints exceeding SLA
- Performance regression detection

---

### 7. Environment-Based Filtering

**When to use:** Different logging behavior per environment.

```python
class EnvironmentFilter(logging.Filter):
    def __init__(self, allowed_environments: list[str]):
        self.allowed_environments = allowed_environments
        self.current_env = os.getenv('ENVIRONMENT', 'development')
    
    def filter(self, record: logging.LogRecord) -> bool:
        return self.current_env in self.allowed_environments

# Usage - debug logs only in dev/staging
debug_handler.addFilter(EnvironmentFilter(['development', 'staging']))
```

**Real-world scenario:**

- Verbose logging in development, minimal in production
- Enable debug logs in staging for testing
- Different log retention policies per environment

---

## Configuration Example

### .env file

```bash
# Overall log level
LOG_LEVEL=INFO

# Environment
ENVIRONMENT=production

# Feature flags
ENABLE_DEBUG_USER_FILTER=false
DEBUG_USER_ID=user123
```

### Python code

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Base level from .env
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
logger.setLevel(getattr(logging, LOG_LEVEL))

# Conditional filter based on .env
if os.getenv('ENABLE_DEBUG_USER_FILTER', 'false').lower() == 'true':
    user_id = os.getenv('DEBUG_USER_ID')
    console_handler.addFilter(UserIdFilter(user_id))
```

---

## Anti-Patterns to Avoid

### ❌ DON'T: Use filters to set log levels

```python
# BAD - use handler.setLevel() instead
class DebugOnlyFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.DEBUG
```

### ✅ DO: Use setLevel() for level control

```python
# GOOD
console_handler.setLevel(logging.DEBUG)
```

### ❌ DON'T: Hardcode filter parameters

```python
# BAD
console_handler.addFilter(UserIdFilter('user123'))
```

### ✅ DO: Use environment variables

```python
# GOOD
user_id = os.getenv('DEBUG_USER_ID')
if user_id:
    console_handler.addFilter(UserIdFilter(user_id))
```

---

## Summary

| Use Case | Tool | Example |
|----------|------|---------|
| Overall verbosity | `.env` LOG_LEVEL | `LOG_LEVEL=DEBUG` |
| Specific modules | `addFilter()` | `ModuleFilter(['payment'])` |
| User/Request tracing | `addFilter()` | `UserIdFilter('user123')` |
| Route to email/Slack | `addFilter()` | `ErrorOnlyFilter()` |
| Exclude sensitive data | `addFilter()` | `PIIFilter()` |
| Prevent log spam | `addFilter()` | `RateLimitFilter()` |
| Performance tracking | `addFilter()` | `PerformanceFilter(100)` |

---

## Files in This Directory

- **`custom_logging.py`** - Main example with all 3 filter types
- **`filter_examples.py`** - 7 additional real-world filter examples
- **`FILTER_BEST_PRACTICES.md`** - This guide

---

## Quick Start

1. Set up `.env`:

```bash
   LOG_LEVEL=DEBUG
   ENVIRONMENT=development
```

2. Run the examples:

```bash
   python custom_logging.py
   python filter_examples.py
```

3. Observe different log outputs in:
   - Console (filtered)
   - `custom_logging.log` (keyword filtered)
   - `errors.log` (errors only)
   - `slack_warnings.log` (warnings only)
