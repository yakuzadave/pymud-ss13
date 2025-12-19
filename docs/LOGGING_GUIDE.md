# Logging Guide for PyMUD-SS13

This guide covers the logging infrastructure for PyMUD-SS13, including configuration, usage, and best practices.

## Table of Contents

1. [Overview](#overview)
2. [TUI Logging System](#tui-logging-system)
3. [Server Logging](#server-logging)
4. [Log Levels](#log-levels)
5. [Configuration](#configuration)
6. [Usage Examples](#usage-examples)
7. [Log File Management](#log-file-management)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)

---

## Overview

PyMUD-SS13 uses Python's built-in `logging` module with custom configurations for:

- **TUI Client**: Structured logging with color-coded console output
- **Server**: Detailed server operation logs
- **Systems**: Individual system logs for debugging
- **File Rotation**: Automatic log file management

### Log Directory Structure

```
logs/
├── tui/                          # TUI client logs
│   ├── tui_YYYYMMDD_HHMMSS.log  # Standard TUI log
│   └── tui_debug_YYYYMMDD_HHMMSS.log  # Debug TUI log
├── behave/                       # BDD test logs
│   └── test_results.log
└── server.log                    # Server operation log
```

---

## TUI Logging System

The TUI client uses a custom logging configuration with multiple handlers and formatters.

### Architecture

```python
TUILogger (Singleton)
├── File Handler (INFO+)     → logs/tui/tui_*.log
├── Debug Handler (DEBUG+)   → logs/tui/tui_debug_*.log
└── Console Handler (WARNING+) → Terminal with colors
```

### Features

- **Singleton Pattern**: Single logger instance across all TUI components
- **Color-Coded Output**: Different colors for different log levels
- **Multiple Handlers**: Separate files for standard and debug logs
- **Automatic Cleanup**: Remove old log files
- **Module-Specific Loggers**: Each module gets its own logger

### Initialization

The TUI logger is automatically initialized on first use:

```python
from tui_client.logging_config import get_logger

logger = get_logger(__name__)
```

### Color Scheme

| Level    | Color   | ANSI Code | Icon |
|----------|---------|-----------|------|
| DEBUG    | Cyan    | `\033[36m` | 🔍 |
| INFO     | Green   | `\033[32m` | 💡 |
| WARNING  | Yellow  | `\033[33m` | ⚠️ |
| ERROR    | Red     | `\033[31m` | ❌ |
| CRITICAL | Magenta | `\033[35m` | 🚨 |

---

## Server Logging

Server logging is configured in `start_server.py`:

```python
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/server.log"),
        logging.StreamHandler()
    ]
)
```

### Server Log Format

```
2025-12-19 10:30:45,123 - mud_server - INFO - Server started on port 5000
2025-12-19 10:30:50,456 - systems.power - WARNING - Power grid overload in Sector A
2025-12-19 10:31:00,789 - commands.movement - DEBUG - Player moved from Bridge to Engineering
```

---

## Log Levels

### When to Use Each Level

#### DEBUG
Use for detailed diagnostic information:
```python
logger.debug(f"Received message: {data.get('type', 'unknown')}")
logger.debug(f"State updated: {self.current_state}")
```

**Examples:**
- Message received/sent details
- State changes
- Function entry/exit
- Variable values during execution

#### INFO
Use for general informational messages:
```python
logger.info("Connected to server successfully")
logger.info("Inventory updated")
logger.info("Player logged in")
```

**Examples:**
- Successful operations
- State transitions
- User actions
- System events

#### WARNING
Use for unexpected but recoverable situations:
```python
logger.warning("Connection unstable, retrying...")
logger.warning("Invalid command format, using default")
logger.warning("Cache miss, fetching from server")
```

**Examples:**
- Deprecated features
- Recoverable errors
- Performance issues
- Configuration problems

#### ERROR
Use for errors that affect functionality:
```python
logger.error(f"Failed to connect: {e}", exc_info=True)
logger.error("Unable to save game state")
logger.error("Invalid response from server")
```

**Examples:**
- Connection failures
- Invalid data
- Operation failures
- Exceptions

#### CRITICAL
Use for severe errors that may cause shutdown:
```python
logger.critical("Database connection lost, shutting down")
logger.critical("Fatal configuration error")
```

**Examples:**
- System failures
- Unrecoverable errors
- Security breaches

---

## Configuration

### Custom Log Level

Set logging level programmatically:

```python
from tui_client.logging_config import TUILogger
import logging

tui_logger = TUILogger()
tui_logger.set_level(logging.DEBUG)  # Show all messages
```

### Environment Variable

Set log level via environment variable:

```bash
export TUI_LOG_LEVEL=DEBUG
python -m tui_client
```

### Per-Module Configuration

Configure logging for specific modules:

```python
import logging

# Disable debug logs for noisy module
logging.getLogger('tui_client.screens.chat').setLevel(logging.INFO)

# Enable verbose logging for specific module
logging.getLogger('tui_client.client').setLevel(logging.DEBUG)
```

---

## Usage Examples

### Basic Logging

```python
from tui_client.logging_config import get_logger

logger = get_logger(__name__)

def connect_to_server(url: str):
    """Connect to game server."""
    logger.info(f"Connecting to {url}...")
    
    try:
        # Connection logic
        result = establish_connection(url)
        logger.info("Connected successfully")
        return result
    except ConnectionError as e:
        logger.error(f"Connection failed: {e}", exc_info=True)
        return None
```

### Logging with Context

```python
logger.info("Processing command", extra={
    'user': username,
    'command': command,
    'timestamp': datetime.now()
})
```

### Conditional Logging

```python
if logger.isEnabledFor(logging.DEBUG):
    # Expensive operation only if debug logging is on
    debug_info = generate_debug_info()
    logger.debug(f"Debug info: {debug_info}")
```

### Logging Exceptions

```python
try:
    result = risky_operation()
except Exception as e:
    logger.exception("Operation failed")  # Includes stack trace
    # OR
    logger.error("Operation failed", exc_info=True)
```

### Performance Logging

```python
import time

start_time = time.time()
result = expensive_operation()
duration = time.time() - start_time

logger.info(f"Operation completed in {duration:.2f}s")
if duration > 1.0:
    logger.warning(f"Slow operation: {duration:.2f}s")
```

### Structured Logging

```python
logger.info(
    "User action",
    extra={
        'action': 'login',
        'user_id': user_id,
        'success': True,
        'duration_ms': 150
    }
)
```

---

## Log File Management

### Automatic Cleanup

Remove logs older than 7 days:

```python
from tui_client.logging_config import TUILogger

tui_logger = TUILogger()
tui_logger.cleanup_old_logs(days=7)
```

### Manual Cleanup

```bash
# Remove logs older than 7 days
find logs/tui -name "*.log" -mtime +7 -delete

# Archive old logs
tar -czf logs_archive_$(date +%Y%m%d).tar.gz logs/
find logs/ -name "*.log" -delete
```

### Log Rotation

For production, implement log rotation:

```python
from logging.handlers import RotatingFileHandler

# Rotate when file reaches 10MB, keep 5 backups
handler = RotatingFileHandler(
    'logs/server.log',
    maxBytes=10*1024*1024,
    backupCount=5
)
```

### Viewing Logs

```bash
# View latest TUI log
ls -lt logs/tui/ | head -5
tail -f logs/tui/tui_*.log

# Search logs
grep "ERROR" logs/tui/*.log
grep -r "Connection failed" logs/

# View with colors preserved
less -R logs/tui/tui_*.log
```

---

## Best Practices

### DO

✅ **Use appropriate log levels**
```python
logger.debug("Variable x = 5")          # Debug detail
logger.info("Operation completed")       # General info
logger.warning("Using fallback value")   # Unexpected but ok
logger.error("Operation failed")         # Error condition
```

✅ **Include context in log messages**
```python
logger.error(f"Failed to process item {item_id} for user {user_id}")
```

✅ **Use exc_info for exceptions**
```python
logger.error("Database error", exc_info=True)
```

✅ **Log at boundaries**
```python
def handle_request(request):
    logger.info(f"Handling request: {request.type}")
    result = process_request(request)
    logger.info(f"Request completed: {result.status}")
    return result
```

✅ **Use structured data**
```python
logger.info("Event occurred", extra={'event_type': 'login', 'user': 'alice'})
```

### DON'T

❌ **Don't log sensitive data**
```python
# BAD
logger.info(f"User logged in with password: {password}")

# GOOD
logger.info(f"User logged in: {username}")
```

❌ **Don't log in tight loops**
```python
# BAD
for item in items:
    logger.debug(f"Processing {item}")  # Could create millions of logs

# GOOD
logger.debug(f"Processing {len(items)} items")
for item in items:
    process(item)
logger.debug("All items processed")
```

❌ **Don't use print() for logging**
```python
# BAD
print("Error occurred")

# GOOD
logger.error("Error occurred")
```

❌ **Don't ignore exceptions**
```python
# BAD
try:
    operation()
except:
    pass

# GOOD
try:
    operation()
except Exception as e:
    logger.exception("Operation failed")
```

---

## Troubleshooting

### No Logs Generated

**Problem:** Log files not being created

**Solutions:**
1. Check directory permissions: `ls -la logs/`
2. Verify logger is initialized: Add `logger.info("Test")` at startup
3. Check log level: Ensure level allows your messages
4. Verify path: Check `TUILogger().log_file` path

### Logs Too Verbose

**Problem:** Too many log messages

**Solutions:**
1. Increase log level: `tui_logger.set_level(logging.WARNING)`
2. Filter specific modules: `logging.getLogger('noisy_module').setLevel(logging.ERROR)`
3. Use log rotation to manage file size

### Missing Log Entries

**Problem:** Expected logs don't appear

**Solutions:**
1. Check log level (message level must be >= handler level)
2. Verify logger is initialized before use
3. Check for exception in logging code
4. Flush handlers: `handler.flush()`

### Performance Impact

**Problem:** Logging slows down application

**Solutions:**
1. Reduce log level in production
2. Use asynchronous logging handlers
3. Avoid expensive operations in log messages
4. Use conditional logging for debug statements

### Color Codes in Files

**Problem:** ANSI codes appearing in log files

**Solutions:**
1. Use ColoredFormatter only for console
2. Use plain formatter for file handlers
3. Strip ANSI codes: `re.sub(r'\033\[[0-9;]+m', '', message)`

---

## Advanced Topics

### Custom Formatter

Create a custom log formatter:

```python
class CustomFormatter(logging.Formatter):
    def format(self, record):
        # Add custom fields
        record.custom_field = "value"
        return super().format(record)
```

### Multiple Log Files

Log different events to different files:

```python
# User actions log
user_logger = logging.getLogger('user_actions')
user_handler = logging.FileHandler('logs/user_actions.log')
user_logger.addHandler(user_handler)

# System events log
system_logger = logging.getLogger('system_events')
system_handler = logging.FileHandler('logs/system_events.log')
system_logger.addHandler(system_handler)
```

### Logging to External Services

Send logs to external service (e.g., Sentry, LogDNA):

```python
import logging
from logging.handlers import HTTPHandler

http_handler = HTTPHandler(
    'logging-service.com',
    '/api/logs',
    method='POST'
)
logger.addHandler(http_handler)
```

---

## Resources

- [Python Logging Documentation](https://docs.python.org/3/library/logging.html)
- [Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html)
- [Best Practices](https://docs.python.org/3/howto/logging.html#logging-basic-tutorial)

---

**Last Updated:** 2025-12-19
