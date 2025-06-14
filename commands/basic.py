"""
Basic command handlers for MUDpy SS13.
This module provides handlers for basic MUD commands like look, help, etc.
"""

import logging
from typing import Optional
from engine import register

# Configure logging
logger = logging.getLogger(__name__)

@register("help")
def help_handler(client_id: str, command: Optional[str] = None, **kwargs) -> str:
    """
    Handle the help command.

    Args:
        client_id: The ID of the client issuing the command.
        command: Optional command name to get help for.

    Returns:
        Help text.
    """
    logger.debug(f"Help command called by client {client_id}, looking up '{command}'")

    # Access parent module command_parser
    import sys
    sys.path.append('.')
    from engine import command_parser

    if command:
        return command_parser.get_help(command)
    else:
        return command_parser.get_help()


@register("status")
def status_handler(client_id: str, **kwargs) -> str:
    """
    Handle the status command.

    Args:
        client_id: The ID of the client issuing the command.

    Returns:
        Status information for the player.
    """
    logger.debug(f"Status command called by client {client_id}")

    # Get the interface from kwargs
    interface = kwargs.get('interface')
    if not interface:
        return "Error: Interface not available"

    # Get player stats
    stats = interface.get_player_stats(client_id)

    if not stats:
        return "Unable to retrieve status information."

    # Build status description
    status_desc = "Status:\n"
    for stat, value in stats.items():
        status_desc += f"{stat.capitalize()}: {value}\n"

    return status_desc
