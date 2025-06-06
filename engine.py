"""
Engine module for MUDpy SS13.
This module provides a command processing system for the MUD engine.
"""

import logging
import os
from typing import Optional, Dict, Any

# Import our new parser and command handlers
from parser import CommandParser

# Import basic handlers (for backward compatibility)
from commands.basic import (
    help_handler,
    inventory_handler,
    get_handler,
    drop_handler,
    use_handler,
    status_handler,
)

# Import movement command handlers
from commands.movement import (
    move_handler,
    sprint_handler,
)

# Import observation command handlers
from commands.observation import (
    look_handler,
    scan_handler,
    map_handler,
)

# Import social command handlers
from commands.social import (
    say_handler,
    shout_handler,
    whisper_handler,
    tell_handler,
    ooc_handler,
)

# Set up module logger
logger = logging.getLogger(__name__)

# Create the command parser
command_parser = CommandParser()

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

class MudEngine:
    """
    Core engine class for the MUD.
    
    This class handles command processing and dispatches to the appropriate handler.
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
        """Initialize the command parser with handlers."""
        # Register basic command handlers
        command_parser.register_handler('help', help_handler)
        command_parser.register_handler('inventory', inventory_handler)
        command_parser.register_handler('get', get_handler)
        command_parser.register_handler('drop', drop_handler)
        command_parser.register_handler('use', use_handler)
        command_parser.register_handler('status', status_handler)
        
        # Register movement command handlers
        command_parser.register_handler('move', move_handler)
        command_parser.register_handler('sprint', sprint_handler)
        
        # Register observation command handlers
        command_parser.register_handler('look', look_handler)
        command_parser.register_handler('scan', scan_handler)
        command_parser.register_handler('map', map_handler)
        
        # Register social command handlers
        command_parser.register_handler('say', say_handler)
        command_parser.register_handler('shout', shout_handler)
        command_parser.register_handler('whisper', whisper_handler)
        command_parser.register_handler('tell', tell_handler)
        command_parser.register_handler('ooc', ooc_handler)
        
        # Load command specs from YAML
        if os.path.exists('data/commands.yaml'):
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
        logger.debug(f"Engine processing command: client={client_id}, command='{command_string}'")
        
        # Ensure command_string is a string
        if not isinstance(command_string, str):
            command_string = str(command_string)
            logger.debug(f"Converted command to string: '{command_string}'")
        
        try:
            # Process the command using the DSL parser
            context = {
                'client_id': client_id,
                'interface': self.interface,
            }
            
            response = command_parser.dispatch(command_string, context)
            
            # Safer response logging
            if response:
                truncated = response[:50] + "..." if len(response) > 50 else response
                logger.debug(f"Command response: '{truncated}'")
            else:
                logger.warning(f"Command '{command_string}' returned empty response")
                response = f"Command completed but returned no output."
            
            return response
            
        except Exception as e:
            import traceback
            logger.error(f"Error processing command '{command_string}': {e}")
            logger.error(f"Exception traceback: {traceback.format_exc()}")
            return f"An error occurred while processing your command: {e}"
