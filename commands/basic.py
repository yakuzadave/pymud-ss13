"""
Basic command handlers for MUDpy SS13.
This module provides handlers for basic MUD commands like look, help, etc.
"""

import logging
from typing import Optional, Dict, Any

# Configure logging
logger = logging.getLogger(__name__)

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

def look_handler(client_id: str, target: Optional[str] = None, **kwargs) -> str:
    """
    Handle the look command.
    
    Args:
        client_id: The ID of the client issuing the command.
        target: Optional target to look at.
        
    Returns:
        Description of the current location or target.
    """
    logger.debug(f"Look command called by client {client_id}")
    
    # Get the interface from kwargs
    interface = kwargs.get('interface')
    if not interface:
        return "Error: Interface not available"
    
    if target:
        logger.debug(f"Looking at target: {target}")
        
        # Get player location
        player_location = interface.get_player_location(client_id)
        if not player_location:
            return "You are nowhere. This is a strange phenomenon indeed."
        
        # Get items in the room
        room_items = interface.get_items_in_room(player_location)
        
        # Get exits from the room
        exits = interface.get_exits_from_room(player_location)
        
        # Get player inventory
        inventory = interface.get_player_inventory(client_id)
        
        # Try to find the target in:
        # 1. Room items
        # 2. Exits
        # 3. Inventory
        
        # Check room items
        for item_id in room_items:
            item_name = interface.get_item_name(item_id)
            if item_name and item_name.lower() == target.lower():
                item_desc = interface.get_item_description(item_id)
                return f"{item_name}: {item_desc}"
        
        # Check exits
        for exit_dir, exit_target in exits.items():
            if exit_dir.lower() == target.lower():
                exit_name = interface.get_room_name(exit_target)
                return f"You see a path leading {exit_dir} to {exit_name}."
        
        # Check inventory
        for item_id in inventory:
            item_name = interface.get_item_name(item_id)
            if item_name and item_name.lower() == target.lower():
                item_desc = interface.get_item_description(item_id)
                return f"{item_name} (in your inventory): {item_desc}"
        
        # Target not found
        return f"You don't see anything called '{target}' here."
    else:
        # Look at current location
        logger.debug(f"Looking at current location for client {client_id}")
        return interface._look(client_id)

def inventory_handler(client_id: str, **kwargs) -> str:
    """
    Handle the inventory command.
    
    Args:
        client_id: The ID of the client issuing the command.
        
    Returns:
        Description of the player's inventory.
    """
    logger.debug(f"Inventory command called by client {client_id}")
    
    # Get the interface from kwargs
    interface = kwargs.get('interface')
    if not interface:
        return "Error: Interface not available"
    
    # Get inventory for this client
    inventory = interface.get_player_inventory(client_id)
    
    if not inventory:
        return "Your inventory is empty."
    
    # Build inventory description
    inventory_desc = "You are carrying:\n"
    for item_id in inventory:
        item_name = interface.get_item_name(item_id)
        inventory_desc += f"- {item_name}\n"
    
    return inventory_desc

def move_handler(client_id: str, direction: Optional[str] = None, **kwargs) -> str:
    """
    Handle the move command.
    
    Args:
        client_id: The ID of the client issuing the command.
        direction: The direction to move.
        
    Returns:
        Result of the movement attempt.
    """
    logger.debug(f"Move command called by client {client_id} with direction {direction}")
    
    # Get the interface from kwargs
    interface = kwargs.get('interface')
    if not interface:
        return "Error: Interface not available"
    
    if not direction:
        return "Move in which direction?"
    
    # Normalize direction
    direction = direction.lower()
    
    # Check for shortcuts
    if direction == "n":
        direction = "north"
    elif direction == "s":
        direction = "south"
    elif direction == "e":
        direction = "east"
    elif direction == "w":
        direction = "west"
    
    # Try to move the player
    return interface._move(client_id, direction)

def say_handler(client_id: str, message: str, **kwargs) -> str:
    """
    Handle the say command.
    
    Args:
        client_id: The ID of the client issuing the command.
        message: The message to say.
        
    Returns:
        Confirmation of the message.
    """
    logger.debug(f"Say command called by client {client_id} with message: {message}")
    
    # Get the interface from kwargs
    interface = kwargs.get('interface')
    if not interface:
        return "Error: Interface not available"
    
    # Get player location
    player_location = interface.get_player_location(client_id)
    
    if not player_location:
        return "You are nowhere. Your words echo into the void."
    
    # Publish event for this message
    from events import publish
    publish("player_said", client_id=client_id, location=player_location, message=message)
    
    return f"You say: {message}"

def get_handler(client_id: str, item: str, container: Optional[str] = None, **kwargs) -> str:
    """
    Handle the get command.
    
    Args:
        client_id: The ID of the client issuing the command.
        item: The item to get.
        container: Optional container to get the item from.
        
    Returns:
        Result of the get attempt.
    """
    logger.debug(f"Get command called by client {client_id} for item {item}")
    
    # Get the interface from kwargs
    interface = kwargs.get('interface')
    if not interface:
        return "Error: Interface not available"
    
    # Get player location
    player_location = interface.get_player_location(client_id)
    
    if not player_location:
        return "You are nowhere. There is nothing to take."
    
    if container:
        # Get from container - not implemented yet
        return f"Taking items from containers is not implemented yet."
    else:
        # Try to get the item from the room
        items_in_room = interface.get_items_in_room(player_location)
        
        # Find item with matching name
        for item_id in items_in_room:
            item_name = interface.get_item_name(item_id)
            if item_name and item_name.lower() == item.lower():
                # Found the item, try to take it
                result = interface._take(client_id, item_id)
                return result
        
        # Item not found
        return f"You don't see '{item}' here."

def drop_handler(client_id: str, item: str, **kwargs) -> str:
    """
    Handle the drop command.
    
    Args:
        client_id: The ID of the client issuing the command.
        item: The item to drop.
        
    Returns:
        Result of the drop attempt.
    """
    logger.debug(f"Drop command called by client {client_id} for item {item}")
    
    # Get the interface from kwargs
    interface = kwargs.get('interface')
    if not interface:
        return "Error: Interface not available"
    
    # Get player location
    player_location = interface.get_player_location(client_id)
    
    if not player_location:
        return "You are nowhere. There is nowhere to drop anything."
    
    # Get player inventory
    inventory = interface.get_player_inventory(client_id)
    
    # Find item with matching name
    for item_id in inventory:
        item_name = interface.get_item_name(item_id)
        if item_name and item_name.lower() == item.lower():
            # Found the item, try to drop it
            result = interface._drop(client_id, item_id)
            return result
    
    # Item not found
    return f"You don't have '{item}' in your inventory."

def use_handler(client_id: str, item: str, target: Optional[str] = None, **kwargs) -> str:
    """
    Handle the use command.
    
    Args:
        client_id: The ID of the client issuing the command.
        item: The item to use.
        target: Optional target to use the item on.
        
    Returns:
        Result of the use attempt.
    """
    logger.debug(f"Use command called by client {client_id} for item {item}")
    
    # Get the interface from kwargs
    interface = kwargs.get('interface')
    if not interface:
        return "Error: Interface not available"
    
    # Get player inventory
    inventory = interface.get_player_inventory(client_id)
    
    # Find item with matching name
    for item_id in inventory:
        item_name = interface.get_item_name(item_id)
        if item_name and item_name.lower() == item.lower():
            # Found the item, try to use it
            result = interface._use(client_id, item_id, target)
            return result
    
    # Item not found
    return f"You don't have '{item}' in your inventory."

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

def scan_handler(client_id: str, target: Optional[str] = None, **kwargs) -> str:
    """
    Handle the scan command.
    
    Args:
        client_id: The ID of the client issuing the command.
        target: Optional target to scan.
        
    Returns:
        Result of the scan.
    """
    logger.debug(f"Scan command called by client {client_id}")
    
    # Get the interface from kwargs
    interface = kwargs.get('interface')
    if not interface:
        return "Error: Interface not available"
    
    # Check if player has a scanner
    inventory = interface.get_player_inventory(client_id)
    
    has_scanner = False
    for item_id in inventory:
        item_name = interface.get_item_name(item_id)
        if item_name and "scanner" in item_name.lower():
            has_scanner = True
            break
    
    if not has_scanner:
        return "You need a scanner to perform a scan."
    
    if target:
        # Scan a specific target
        return f"Scanning {target}...\nNo anomalies detected."
    else:
        # Scan the environment
        return "Scanning environment...\nAtmospheric conditions normal. No anomalies detected."
