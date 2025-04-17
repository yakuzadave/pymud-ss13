"""
Commands package for MUDpy SS13.
Commands are registered with the engine and provide the interface for player actions.
"""

# Note: All command modules will be dynamically loaded when imported by mud_websocket_server.py
# This prevents circular imports while still registering all handlers

# Leave this file intentionally minimal to prevent import cycles