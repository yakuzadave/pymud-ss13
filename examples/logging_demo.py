#!/usr/bin/env python3
"""
Demonstration of the TUI logging system.

This script shows how to use the enhanced logging features
in the TUI client.
"""

import sys
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tui_client.logging_config import get_logger, TUILogger
import logging


def demonstrate_basic_logging():
    """Show basic logging at different levels."""
    logger = get_logger(__name__)
    
    print("\n" + "="*60)
    print("BASIC LOGGING DEMONSTRATION")
    print("="*60 + "\n")
    
    print("Logging at different levels:")
    logger.debug("This is a DEBUG message - detailed diagnostic info")
    logger.info("This is an INFO message - general information")
    logger.warning("This is a WARNING message - something unexpected")
    logger.error("This is an ERROR message - an error occurred")
    logger.critical("This is a CRITICAL message - severe error")
    
    print("\n✓ Messages logged to files in logs/tui/")
    print("  (Only WARNING and above show in console by default)")


def demonstrate_contextual_logging():
    """Show logging with context information."""
    logger = get_logger(__name__)
    
    print("\n" + "="*60)
    print("CONTEXTUAL LOGGING DEMONSTRATION")
    print("="*60 + "\n")
    
    # Simulate user actions
    username = "demo_user"
    command = "look"
    
    logger.info(f"User {username} executed command: {command}")
    logger.info(f"Processing command '{command}' for user '{username}'")
    logger.info(f"Command '{command}' completed successfully")
    
    print("✓ Logged user actions with context")


def demonstrate_exception_logging():
    """Show exception logging."""
    logger = get_logger(__name__)
    
    print("\n" + "="*60)
    print("EXCEPTION LOGGING DEMONSTRATION")
    print("="*60 + "\n")
    
    try:
        # Simulate an error
        result = 1 / 0
    except ZeroDivisionError as e:
        logger.error(f"Error in calculation: {e}", exc_info=True)
        print("✓ Exception logged with full stack trace")
    
    try:
        # Simulate connection error
        raise ConnectionError("Unable to connect to server")
    except ConnectionError as e:
        logger.exception("Connection failed")
        print("✓ Connection error logged")


def demonstrate_conditional_logging():
    """Show conditional logging for performance."""
    logger = get_logger(__name__)
    
    print("\n" + "="*60)
    print("CONDITIONAL LOGGING DEMONSTRATION")
    print("="*60 + "\n")
    
    # Only generate debug info if debug logging is enabled
    if logger.isEnabledFor(logging.DEBUG):
        expensive_debug_info = "Detailed state: " + str({
            "users": 100,
            "connections": 50,
            "memory_mb": 256
        })
        logger.debug(expensive_debug_info)
        print("✓ Debug logging is enabled - generated debug info")
    else:
        print("✓ Debug logging is disabled - skipped expensive operation")


def demonstrate_performance_logging():
    """Show performance logging."""
    logger = get_logger(__name__)
    
    print("\n" + "="*60)
    print("PERFORMANCE LOGGING DEMONSTRATION")
    print("="*60 + "\n")
    
    # Measure operation time
    start_time = time.time()
    time.sleep(0.1)  # Simulate work
    duration = time.time() - start_time
    
    logger.info(f"Operation completed in {duration:.3f}s")
    
    if duration > 0.05:
        logger.warning(f"Slow operation detected: {duration:.3f}s")
    
    print("✓ Performance metrics logged")


def demonstrate_log_levels():
    """Show changing log levels dynamically."""
    logger = get_logger(__name__)
    tui_logger = TUILogger()
    
    print("\n" + "="*60)
    print("LOG LEVEL DEMONSTRATION")
    print("="*60 + "\n")
    
    print("Current log level: INFO")
    logger.debug("This DEBUG message won't show in console")
    logger.info("This INFO message will show in console if WARNING or lower")
    
    print("\nChanging log level to DEBUG...")
    tui_logger.set_level(logging.DEBUG)
    
    logger.debug("This DEBUG message now shows!")
    logger.info("This INFO message shows too")
    
    print("\n✓ Log level changed dynamically")
    
    # Reset to WARNING for console
    tui_logger.set_level(logging.WARNING)


def demonstrate_cleanup():
    """Show log cleanup functionality."""
    tui_logger = TUILogger()
    
    print("\n" + "="*60)
    print("LOG CLEANUP DEMONSTRATION")
    print("="*60 + "\n")
    
    print(f"Log directory: {tui_logger.log_dir}")
    print(f"Current log file: {tui_logger.log_file.name}")
    print(f"Debug log file: {tui_logger.debug_log_file.name}")
    
    print("\nYou can cleanup old logs with:")
    print("  tui_logger.cleanup_old_logs(days=7)")
    print("\nThis removes log files older than 7 days")


def main():
    """Run all demonstrations."""
    print("\n" + "="*60)
    print("TUI LOGGING SYSTEM DEMONSTRATION")
    print("="*60)
    print("\nThis script demonstrates the enhanced logging features")
    print("of the PyMUD-SS13 TUI client.\n")
    
    # Run demonstrations
    demonstrate_basic_logging()
    time.sleep(0.5)
    
    demonstrate_contextual_logging()
    time.sleep(0.5)
    
    demonstrate_exception_logging()
    time.sleep(0.5)
    
    demonstrate_conditional_logging()
    time.sleep(0.5)
    
    demonstrate_performance_logging()
    time.sleep(0.5)
    
    demonstrate_log_levels()
    time.sleep(0.5)
    
    demonstrate_cleanup()
    
    print("\n" + "="*60)
    print("DEMONSTRATION COMPLETE")
    print("="*60)
    print("\nCheck the following locations for logs:")
    print("  - logs/tui/tui_*.log (standard logs, INFO and above)")
    print("  - logs/tui/tui_debug_*.log (debug logs, all levels)")
    print("\nFor more information, see docs/LOGGING_GUIDE.md")
    print()


if __name__ == "__main__":
    main()
