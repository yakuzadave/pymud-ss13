"""
Engine module for MUDpy SS13.
This module provides a command registry system for the MUD engine.
"""

import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Command handler registry
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
    
    This class handles command processing and dispatches to the registered handlers.
    """
    
    def __init__(self, interface=None):
        """
        Initialize the MUD engine.
        
        Args:
            interface: Reference to the MUDpy interface instance.
        """
        self.interface = interface
        logger.info("MUD Engine initialized")
        
    def process_command(self, client_id: str, command_string: str) -> str:
        """
        Process a command from a client and return the response.
        
        Args:
            client_id (str): Unique identifier for the client.
            command_string (str): The full command to process.
            
        Returns:
            str: The response to the command.
        """
        # Ensure command_string is a string
        if not isinstance(command_string, str):
            command_string = str(command_string)
        
        # Split the command into the verb and arguments
        parts = command_string.strip().split(maxsplit=1)
        verb = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        
        # Lookup the handler in the registry
        handler = COMMAND_HANDLERS.get(verb)
        
        if handler:
            try:
                # Call the handler with the interface, client_id, and arguments
                return handler(self.interface, client_id, args)
            except Exception as e:
                logger.error(f"Error executing command handler for '{verb}': {e}")
                return f"An error occurred while processing your command: {e}"
        else:
            return f"Unknown command '{verb}'. Type 'help' for a list of commands."