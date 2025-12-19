"""
Logging configuration for the TUI client.

Provides structured logging with different levels, formatters,
and handlers for both file and console output.
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


class ColoredFormatter(logging.Formatter):
    """Custom formatter with color codes for different log levels."""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record):
        """Format the log record with colors."""
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.COLORS['RESET']}"
        return super().format(record)


class TUILogger:
    """
    Centralized logger for the TUI client.
    
    Provides consistent logging across all TUI components with
    file and console handlers.
    """
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        """Singleton pattern to ensure only one logger instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the logger if not already done."""
        if not TUILogger._initialized:
            self.log_dir = Path("logs/tui")
            self.log_dir.mkdir(parents=True, exist_ok=True)
            
            # Create log files
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.log_file = self.log_dir / f"tui_{timestamp}.log"
            self.debug_log_file = self.log_dir / f"tui_debug_{timestamp}.log"
            
            self._setup_loggers()
            TUILogger._initialized = True
    
    def _setup_loggers(self):
        """Setup logging handlers and formatters."""
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        simple_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        
        colored_formatter = ColoredFormatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        
        # File handler for all messages (INFO and above)
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(detailed_formatter)
        
        # Debug file handler (all levels)
        debug_handler = logging.FileHandler(self.debug_log_file)
        debug_handler.setLevel(logging.DEBUG)
        debug_handler.setFormatter(detailed_formatter)
        
        # Console handler (WARNING and above, with colors)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(colored_formatter)
        
        # Get root logger for tui_client
        self.logger = logging.getLogger('tui_client')
        self.logger.setLevel(logging.DEBUG)
        
        # Remove existing handlers to avoid duplicates
        self.logger.handlers.clear()
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(debug_handler)
        self.logger.addHandler(console_handler)
        
        # Prevent propagation to root logger
        self.logger.propagate = False
        
        self.logger.info("TUI logging initialized")
        self.logger.debug(f"Log file: {self.log_file}")
        self.logger.debug(f"Debug log file: {self.debug_log_file}")
    
    def get_logger(self, name: str) -> logging.Logger:
        """
        Get a logger for a specific module.
        
        Args:
            name: The module name (typically __name__)
            
        Returns:
            Logger instance configured with TUI handlers
        """
        return logging.getLogger(f'tui_client.{name}')
    
    def set_level(self, level: int):
        """
        Set the logging level for all handlers.
        
        Args:
            level: Logging level (e.g., logging.DEBUG, logging.INFO)
        """
        self.logger.setLevel(level)
        for handler in self.logger.handlers:
            if isinstance(handler, logging.FileHandler):
                # Keep file handlers at their current level
                continue
            handler.setLevel(level)
    
    def cleanup_old_logs(self, days: int = 7):
        """
        Remove log files older than specified days.
        
        Args:
            days: Number of days to keep logs
        """
        if not self.log_dir.exists():
            return
        
        cutoff = datetime.now().timestamp() - (days * 86400)
        removed = 0
        
        for log_file in self.log_dir.glob("tui*.log"):
            if log_file.stat().st_mtime < cutoff:
                try:
                    log_file.unlink()
                    removed += 1
                except Exception as e:
                    self.logger.warning(f"Failed to remove old log {log_file}: {e}")
        
        if removed > 0:
            self.logger.info(f"Cleaned up {removed} old log files")


# Convenience function to get a logger
def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance for TUI components.
    
    Args:
        name: Module name (typically __name__)
        
    Returns:
        Configured logger instance
    """
    tui_logger = TUILogger()
    if name:
        return tui_logger.get_logger(name)
    return tui_logger.logger
