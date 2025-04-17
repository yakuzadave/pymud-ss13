"""
Engine module for MUDpy SS13.
This module provides a command registry system for the MUD engine.
"""

import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
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
        logger.debug(f"Engine processing command: client={client_id}, command='{command_string}'")
        
        # Ensure command_string is a string
        if not isinstance(command_string, str):
            command_string = str(command_string)
            logger.debug(f"Converted command to string: '{command_string}'")
        
        # Split the command into the verb and arguments
        parts = command_string.strip().split(maxsplit=1)
        verb = parts[0].lower() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        
        logger.debug(f"Parsed command: verb='{verb}', args='{args}'")
        
        # Lookup the handler in the registry
        handler = COMMAND_HANDLERS.get(verb)
        
        if handler:
            try:
                logger.debug(f"Found handler for '{verb}', executing with client_id={client_id}, type={type(client_id)}")
                # Call the handler with the interface, client_id, and arguments
                response = handler(self.interface, client_id, args)
                
                # Safer response logging
                if response:
                    truncated = response[:50] + "..." if len(response) > 50 else response
                    logger.debug(f"Handler response: '{truncated}'")
                else:
                    logger.warning(f"Handler for '{verb}' returned empty response")
                    response = f"Command '{verb}' completed but returned no output."
                
                return response
                
            except Exception as e:
                import traceback
                logger.error(f"Error executing command handler for '{verb}': {e}")
                logger.error(f"Exception traceback: {traceback.format_exc()}")
                return f"An error occurred while processing your command: {e}"
        else:
            logger.debug(f"No handler found for command '{verb}'")
            return f"Unknown command '{verb}'. Type 'help' for a list of commands."