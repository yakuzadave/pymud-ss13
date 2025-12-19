"""
Behave environment configuration for TUI testing.

Sets up and tears down test context for BDD tests.
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def before_all(context):
    """
    Setup run once before all tests.
    
    Args:
        context: Behave context object
    """
    # Create logs directory if needed
    logs_dir = project_root / "logs" / "behave"
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    # Store project paths
    context.project_root = project_root
    context.logs_dir = logs_dir
    
    # Test configuration
    context.config.server_host = "localhost"
    context.config.server_port = 5000
    context.config.test_timeout = 30
    
    print("=" * 70)
    print("Starting TUI BDD Tests")
    print("=" * 70)


def before_scenario(context, scenario):
    """
    Setup run before each scenario.
    
    Args:
        context: Behave context object
        scenario: The scenario about to run
    """
    # Reset test state
    context.authenticated = False
    context.current_screen = None
    context.server_running = False
    context.command_history = []
    context.inventory_items = []
    
    print(f"\n--- Running: {scenario.name} ---")


def after_scenario(context, scenario):
    """
    Cleanup run after each scenario.
    
    Args:
        context: Behave context object
        scenario: The scenario that just ran
    """
    # Cleanup any test artifacts
    if hasattr(context, 'test_server'):
        # Stop test server if running
        pass
    
    if hasattr(context, 'test_client'):
        # Disconnect test client
        pass
    
    status = "✅ PASSED" if scenario.status == "passed" else "❌ FAILED"
    print(f"--- {status}: {scenario.name} ---")


def after_all(context):
    """
    Cleanup run once after all tests.
    
    Args:
        context: Behave context object
    """
    print("\n" + "=" * 70)
    print("TUI BDD Tests Complete")
    print("=" * 70)
