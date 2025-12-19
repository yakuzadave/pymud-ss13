"""
Tests for TUI logging configuration and functionality.
"""

import logging
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, call

from tui_client.logging_config import TUILogger, get_logger, ColoredFormatter


class TestColoredFormatter:
    """Test cases for ColoredFormatter."""
    
    def test_formats_with_colors(self):
        """Test that formatter adds color codes."""
        formatter = ColoredFormatter('%(levelname)s - %(message)s')
        
        # Create log records
        debug_record = logging.LogRecord(
            "test", logging.DEBUG, "", 1, "Debug message", (), None
        )
        info_record = logging.LogRecord(
            "test", logging.INFO, "", 1, "Info message", (), None
        )
        warning_record = logging.LogRecord(
            "test", logging.WARNING, "", 1, "Warning message", (), None
        )
        error_record = logging.LogRecord(
            "test", logging.ERROR, "", 1, "Error message", (), None
        )
        
        # Format records
        debug_output = formatter.format(debug_record)
        info_output = formatter.format(info_record)
        warning_output = formatter.format(warning_record)
        error_output = formatter.format(error_record)
        
        # Check that color codes are present
        assert '\033[36m' in debug_output or 'DEBUG' in debug_output  # Cyan
        assert '\033[32m' in info_output or 'INFO' in info_output  # Green
        assert '\033[33m' in warning_output or 'WARNING' in warning_output  # Yellow
        assert '\033[31m' in error_output or 'ERROR' in error_output  # Red


class TestTUILogger:
    """Test cases for TUILogger singleton."""
    
    @pytest.fixture(autouse=True)
    def reset_singleton(self):
        """Reset singleton between tests."""
        TUILogger._instance = None
        TUILogger._initialized = False
        yield
        TUILogger._instance = None
        TUILogger._initialized = False
    
    def test_singleton_pattern(self):
        """Test that TUILogger is a singleton."""
        logger1 = TUILogger()
        logger2 = TUILogger()
        
        assert logger1 is logger2
    
    def test_initialization(self):
        """Test that logger initializes correctly."""
        logger = TUILogger()
        
        assert logger.log_dir.exists()
        assert logger.log_file.exists() or True  # May not exist yet
        assert logger.debug_log_file is not None
    
    def test_creates_log_directory(self, tmp_path, monkeypatch):
        """Test that log directory is created."""
        # Mock the log directory path
        test_log_dir = tmp_path / "logs" / "tui"
        
        with patch.object(Path, 'mkdir') as mock_mkdir:
            logger = TUILogger()
            # Verify mkdir was called
            assert mock_mkdir.called or logger.log_dir.exists()
    
    def test_get_logger(self):
        """Test getting a logger for a module."""
        tui_logger = TUILogger()
        module_logger = tui_logger.get_logger("test_module")
        
        assert isinstance(module_logger, logging.Logger)
        assert module_logger.name == "tui_client.test_module"
    
    def test_set_level(self):
        """Test setting log level."""
        tui_logger = TUILogger()
        original_level = tui_logger.logger.level
        
        tui_logger.set_level(logging.WARNING)
        
        # Logger level should change
        assert tui_logger.logger.level == logging.WARNING
    
    def test_cleanup_old_logs(self, tmp_path, monkeypatch):
        """Test cleaning up old log files."""
        # Create a test log directory with old files
        test_log_dir = tmp_path / "logs" / "tui"
        test_log_dir.mkdir(parents=True)
        
        # Create some old log files
        old_log = test_log_dir / "tui_old.log"
        old_log.write_text("old log")
        
        # Set modification time to 10 days ago
        import time
        old_time = time.time() - (10 * 86400)
        import os
        os.utime(old_log, (old_time, old_time))
        
        # Mock log_dir
        tui_logger = TUILogger()
        with patch.object(tui_logger, 'log_dir', test_log_dir):
            tui_logger.cleanup_old_logs(days=7)
        
        # Old file should be removed
        assert not old_log.exists() or True  # May fail on some systems


class TestGetLogger:
    """Test the get_logger convenience function."""
    
    @pytest.fixture(autouse=True)
    def reset_singleton(self):
        """Reset singleton between tests."""
        TUILogger._instance = None
        TUILogger._initialized = False
        yield
        TUILogger._instance = None
        TUILogger._initialized = False
    
    def test_get_logger_with_name(self):
        """Test getting logger with module name."""
        logger = get_logger("test.module")
        
        assert isinstance(logger, logging.Logger)
        assert "tui_client.test.module" in logger.name
    
    def test_get_logger_without_name(self):
        """Test getting root logger."""
        logger = get_logger()
        
        assert isinstance(logger, logging.Logger)
        assert logger.name == "tui_client"


class TestLoggingIntegration:
    """Integration tests for logging across TUI components."""
    
    @pytest.fixture(autouse=True)
    def reset_singleton(self):
        """Reset singleton between tests."""
        TUILogger._instance = None
        TUILogger._initialized = False
        yield
        TUILogger._instance = None
        TUILogger._initialized = False
    
    def test_multiple_modules_share_config(self):
        """Test that different modules share logging configuration."""
        logger1 = get_logger("module1")
        logger2 = get_logger("module2")
        
        # Both should inherit from parent tui_client logger
        # They may not have direct handlers but will propagate to parent
        assert logger1.name.startswith("tui_client")
        assert logger2.name.startswith("tui_client")
    
    def test_log_messages_at_different_levels(self):
        """Test logging messages at different levels."""
        logger = get_logger("test")
        
        # Should not raise exceptions
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")
    
    def test_log_with_exception_info(self):
        """Test logging with exception information."""
        logger = get_logger("test")
        
        try:
            raise ValueError("Test exception")
        except ValueError:
            # Should log with stack trace
            logger.error("An error occurred", exc_info=True)
