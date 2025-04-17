"""
Commands package for MUDpy SS13.
Commands are registered with the engine and provide the interface for player actions.
"""

# Import all command modules to ensure handlers are registered
from commands import basic
from commands import movement
from commands import inventory
from commands import system
from commands import interaction
from commands import debug  # This should be disabled in production