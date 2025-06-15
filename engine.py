"""
Engine module for MUDpy SS13.
This module provides a command processing system for the MUD engine.
"""

import logging
import os
from action_queue import ActionQueue

from parser import CommandParser

# Set up module logger
logger = logging.getLogger(__name__)

# Create the command parser
command_parser = CommandParser()

# Action queue to prevent spamming commands
action_queue = ActionQueue()
RATE_LIMITED = {"move", "get", "take", "drop", "use", "put", "wear", "remove", "sprint"}

# Legacy command handler registry (for backward compatibility)
COMMAND_HANDLERS = {}


def register(cmd_name):
    """
    Decorator to register command handlers.

    Args:
        cmd_name (str): The command name to register.

    Returns:
        function: Decorator function that registers the handler.
    """

    def decorator(fn):
        COMMAND_HANDLERS[cmd_name] = fn
        logger.info(f"Registered command handler for '{cmd_name}'")
        return fn

    return decorator


# Import command modules so decorators run and populate COMMAND_HANDLERS
from commands import (  # noqa: F401,E402
    basic,
    movement,
    observation,
    social,
    system,
    inventory,
    debug,
    aliases,
    interaction,
    engineer,
    doctor,
    security,
    chemist,
    bartender,
    botanist,
    research,
    cargo,
    antag,
    job,
    circuit,
    comms,
)


class MudEngine:
    """
    Core engine class for the MUD.

    This class handles command processing and dispatches to the appropriate
    handler.
    """

    def __init__(self, interface=None):
        """
        Initialize the MUD engine.

        Args:
            interface: Reference to the MUDpy interface instance.
        """
        self.interface = interface

        # Initialize the command parser
        self._initialize_command_parser()

        logger.info("MUD Engine initialized")

    def _initialize_command_parser(self):
        """Initialize the command parser with handlers from the registry."""
        for name, handler in COMMAND_HANDLERS.items():
            command_parser.register_handler(name, handler)

        # Load command specs from YAML
        if os.path.exists("data/commands.yaml"):
            command_parser.load_commands()
        else:
            logger.warning("Command specs file not found: data/commands.yaml")

    def process_command(self, client_id: str, command_string: str) -> str:
        """
        Process a command from a client and return the response.

        Args:
            client_id (str): Unique identifier for the client.
            command_string (str): The full command to process.

        Returns:
            str: The response to the command.
        """
        logger.debug(
            f"Engine processing command: client={client_id}, "
            f"command='{command_string}'"
        )

        cmd_name = command_string.split()[0] if command_string else ""
        if cmd_name in RATE_LIMITED and not action_queue.can_act(client_id):
            logger.debug("Action blocked by queue")
            return "You need to slow down and wait a moment."

        # Ensure command_string is a string
        if not isinstance(command_string, str):
            command_string = str(command_string)
            logger.debug(f"Converted command to string: '{command_string}'")

        try:
            # Process the command using the DSL parser
            context = {
                "client_id": client_id,
                "interface": self.interface,
            }

            response = command_parser.dispatch(command_string, context)
            if cmd_name in RATE_LIMITED:
                action_queue.record_action(client_id)

            # Safer response logging
            if response:
                truncated = response[:50] + "..." if len(response) > 50 else response
                logger.debug(f"Command response: '{truncated}'")
            else:
                logger.warning(f"Command '{command_string}' returned empty response")
                response = "Command completed but returned no output."

            return response

        except Exception as e:
            import traceback

            logger.error(f"Error processing command '{command_string}': {e}")
            logger.error(f"Exception traceback: {traceback.format_exc()}")
            return f"An error occurred while processing your command: {e}"
