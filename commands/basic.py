"""
Basic commands for MUDpy SS13.
These include looking, help, and other informational commands.
"""

import logging
from engine import register
from events import publish

logger = logging.getLogger(__name__)

@register("look")
def cmd_look(interface, client_id, args):
    """
    Look at the current location or a specific object.
    
    Args:
        interface: The MUDpy interface instance.
        client_id: The ID of the client.
        args: Additional arguments (optional target to look at).
        
    Returns:
        str: Description of what was seen.
    """
    logger.debug(f"Look command called by client {client_id}")
    
    # Get session data for debugging
    session = interface.client_sessions.get(client_id, {})
    logger.debug(f"Client session data: {session}")
    
    # If no args, look at the room
    if not args:
        logger.debug(f"Looking at current location for client {client_id}")
        response = interface._look(client_id)
        logger.debug(f"Look response: {response[:50]}..." if response else "None")
        return response
    
    # Otherwise, try to look at a specific object
    # This should be enhanced to use the world and component system
    logger.debug(f"Looking at specific object: {args}")
    return f"You look at {args}, but don't see anything special."

@register("help")
def cmd_help(interface, client_id, args):
    """
    Display help information about commands.
    
    Args:
        interface: The MUDpy interface instance.
        client_id: The ID of the client.
        args: Command to get help for (optional).
        
    Returns:
        str: Help information.
    """
    # If no args, show general help
    if not args:
        commands = [
            "help [command] - Display help information",
            "look [target] - Look at your surroundings or a specific target",
            "go <direction> - Move in a direction (north, south, east, west)",
            "say <message> - Say something to others in the room",
            "inventory - List items you are carrying",
            "take <item> - Pick up an item",
            "drop <item> - Drop an item",
            "use <item> - Use an item",
            "examine <item> - Examine an item in detail",
            "scan - Perform environmental scan",
            "stats - Check your vital statistics",
            "quit - Disconnect from the system"
        ]
        
        help_text = "Available commands:\n" + "\n".join(commands)
        return help_text
    
    # Show help for a specific command
    cmd = args.lower()
    
    if cmd == "look":
        return "look [target] - Look at your surroundings or a specific target."
    elif cmd == "go":
        return "go <direction> - Move in a direction (north, south, east, west)."
    elif cmd == "say":
        return "say <message> - Say something to others in the room."
    elif cmd == "inventory" or cmd == "i":
        return "inventory - List items you are carrying."
    elif cmd == "take":
        return "take <item> - Pick up an item from your surroundings."
    elif cmd == "drop":
        return "drop <item> - Drop an item from your inventory."
    elif cmd == "use":
        return "use <item> - Use an item from your inventory."
    elif cmd == "examine":
        return "examine <item> - Examine an item in detail."
    elif cmd == "scan":
        return "scan - Perform a scan of the environment and your vital signs."
    elif cmd == "stats":
        return "stats - Check your vital statistics (health, energy, etc.)."
    elif cmd == "quit":
        return "quit - Disconnect from the system."
    else:
        return f"No help available for '{cmd}'. Type 'help' for a list of commands."

@register("say")
def cmd_say(interface, client_id, args):
    """
    Say something to others in the same location.
    
    Args:
        interface: The MUDpy interface instance.
        client_id: The ID of the client.
        args: The message to say.
        
    Returns:
        str: Confirmation of the message.
    """
    if not args:
        return "Say what? Type 'say <message>'."
    
    # Get the client's session data
    session = interface.client_sessions.get(client_id, {})
    player_name = session.get("character", f"Player_{client_id}")  # Use 'character' which is set in connect_client
    location = session.get("location", "nowhere")
    
    # Create the message and log for debugging
    message = f"{player_name} says: {args}"
    logger.debug(f"Say command: player={player_name}, location={location}, message={args}")
    
    # Publish an event for this message
    publish("player_said", client_id=client_id, location=location, message=args)
    
    # This is a placeholder that should be enhanced to use the world and component system
    return interface._say(client_id, args)

@register("scan")
def cmd_scan(interface, client_id, args):
    """
    Perform a scan of the environment and vital signs.
    
    Args:
        interface: The MUDpy interface instance.
        client_id: The ID of the client.
        args: Additional arguments (unused).
        
    Returns:
        str: Results of the scan.
    """
    # This is a placeholder that should be enhanced to use the world and component system
    return interface._scan(client_id)

@register("stats")
def cmd_stats(interface, client_id, args):
    """
    Check your vital statistics.
    
    Args:
        interface: The MUDpy interface instance.
        client_id: The ID of the client.
        args: Additional arguments (unused).
        
    Returns:
        str: Current player statistics.
    """
    # This is a placeholder that should be enhanced to use the world and component system
    return interface._stats(client_id)