"""
Observation command handlers for MUDpy SS13.
This module provides handlers for observation commands like look, scan, etc.
"""

import logging
from typing import Optional, Dict, Any

# Configure logging
logger = logging.getLogger(__name__)

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
        # 4. Players in the room
        
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
        
        # Check other players in the room
        for other_id in interface.get_clients():
            if other_id != client_id:  # Don't include self
                other_location = interface.get_player_location(other_id)
                if other_location == player_location:
                    other_session = interface.get_session(other_id)
                    if other_session and 'character' in other_session:
                        other_name = other_session['character']
                        if other_name.lower() == target.lower():
                            other_stats = interface.get_player_stats(other_id)
                            health_status = "in good health"
                            if other_stats and 'health' in other_stats:
                                health = other_stats['health']
                                if health < 30:
                                    health_status = "severely injured"
                                elif health < 70:
                                    health_status = "slightly injured"
                            return f"{other_name} is here, appears to be {health_status}."
        
        # Target not found
        return f"You don't see anything called '{target}' here."
    else:
        # Look at current location
        logger.debug(f"Looking at current location for client {client_id}")
        
        # Get player location
        player_location = interface.get_player_location(client_id)
        if not player_location:
            return "You are nowhere. This is a strange phenomenon indeed."
        
        # Get room info
        room_name = interface.get_room_name(player_location)
        room_desc = interface.get_room_description(player_location)
        
        # Get items in the room
        room_items = interface.get_items_in_room(player_location)
        
        # Get exits from the room
        exits = interface.get_exits_from_room(player_location)
        
        # Get other players in the room
        other_players = []
        for other_id in interface.get_clients():
            if other_id != client_id:  # Don't include self
                other_location = interface.get_player_location(other_id)
                if other_location == player_location:
                    other_session = interface.get_session(other_id)
                    if other_session and 'character' in other_session:
                        other_players.append(other_session['character'])
        
        # Build the room description
        result = f"\n{room_name}\n{room_desc}\n"
        
        # Add items
        if room_items:
            result += "\nYou see here:\n"
            for item_id in room_items:
                item_name = interface.get_item_name(item_id)
                result += f"- {item_name}\n"
        
        # Add other players
        if other_players:
            result += "\nOther crew members here:\n"
            for player in other_players:
                result += f"- {player}\n"
        
        # Add exits
        if exits:
            result += "\nExits: " + ", ".join(exits.keys())
        else:
            result += "\nThere are no obvious exits."
        
        return result

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
    scanner_type = None
    for item_id in inventory:
        item_name = interface.get_item_name(item_id)
        if item_name and "scanner" in item_name.lower():
            has_scanner = True
            scanner_type = item_name
            break
    
    if not has_scanner:
        return "You need a scanner to perform a scan."
    
    # Get player location
    player_location = interface.get_player_location(client_id)
    if not player_location:
        return "You are nowhere. There is nothing to scan."
    
    # Different scan results based on scanner type
    if target:
        # Targeted scan
        if scanner_type and "biometric" in scanner_type.lower():
            # Scan for life signs
            for other_id in interface.get_clients():
                if other_id != client_id:  # Don't include self
                    other_location = interface.get_player_location(other_id)
                    other_session = interface.get_session(other_id)
                    if other_session and 'character' in other_session:
                        other_name = other_session['character']
                        if other_name.lower() == target.lower():
                            other_stats = interface.get_player_stats(other_id)
                            health = other_stats.get('health', 'unknown')
                            oxygen = other_stats.get('oxygen', 'unknown')
                            radiation = other_stats.get('radiation', 'unknown')
                            return f"Biometric scan of {other_name}:\nHealth: {health}%\nOxygen: {oxygen}%\nRadiation: {radiation} rads"
            
            # Look for the target item
            room_items = interface.get_items_in_room(player_location)
            for item_id in room_items:
                item_name = interface.get_item_name(item_id)
                if item_name and item_name.lower() == target.lower():
                    return f"Biometric scan of {item_name} shows no life signs."
            
            return f"No target '{target}' found for biometric scanning."
        
        elif scanner_type and "radiation" in scanner_type.lower():
            # Scan for radiation
            room_items = interface.get_items_in_room(player_location)
            for item_id in room_items:
                item_name = interface.get_item_name(item_id)
                if item_name and item_name.lower() == target.lower():
                    # Random radiation levels based on item type
                    if "reactor" in item_name.lower():
                        return f"Radiation scan of {item_name}: DANGER! 345 rads detected!"
                    else:
                        return f"Radiation scan of {item_name}: Safe levels (0.1 rads)"
            
            return f"No target '{target}' found for radiation scanning."
        
        # Default scanning behavior if scanner type doesn't match specific types
        return f"Your {scanner_type if scanner_type else 'scanner'} can't perform detailed scans on {target}."
    else:
        # Room scan
        if scanner_type and "biometric" in scanner_type.lower():
            life_signs = 0
            scan_result = "Biometric scan of the area:\n"
            
            # Count other players in the room
            for other_id in interface.get_clients():
                if other_id != client_id:  # Don't include self
                    other_location = interface.get_player_location(other_id)
                    if other_location == player_location:
                        life_signs += 1
            
            scan_result += f"Detected {life_signs} humanoid life forms in addition to yourself.\n"
            
            # Check for any non-human life forms
            room_name = interface.get_room_name(player_location)
            if room_name and "lab" in room_name.lower():
                scan_result += "Warning: Non-humanoid life form signatures detected."
            
            return scan_result
        
        elif scanner_type and "radiation" in scanner_type.lower():
            # Check room for radiation
            room_name = interface.get_room_name(player_location)
            if room_name and "reactor" in room_name.lower():
                return "Radiation scan: CAUTION! Elevated radiation levels detected (15.7 rads)."
            else:
                return "Radiation scan: Normal background radiation levels (0.1 rads)."
        
        # Default scanning behavior
        return f"Scanning with {scanner_type if scanner_type else 'scanner'}... No anomalies detected."

def map_handler(client_id: str, **kwargs) -> str:
    """
    Handle the map command.
    
    Args:
        client_id: The ID of the client issuing the command.
        
    Returns:
        ASCII map of the surrounding area.
    """
    logger.debug(f"Map command called by client {client_id}")
    
    # Get the interface from kwargs
    interface = kwargs.get('interface')
    if not interface:
        return "Error: Interface not available"
    
    # Check if player has a mapping device (e.g., PDA, tablet)
    inventory = interface.get_player_inventory(client_id)
    
    has_map_device = False
    for item_id in inventory:
        item_name = interface.get_item_name(item_id)
        if item_name and ("pda" in item_name.lower() or "tablet" in item_name.lower()):
            has_map_device = True
            break
    
    # Allow the map if they have comms_device too
    if not has_map_device and "comms_device" in inventory:
        has_map_device = True
    
    if not has_map_device:
        return "You need a PDA, tablet, or communications device to view the station map."
    
    # Get player location
    player_location = interface.get_player_location(client_id)
    if not player_location:
        return "ERROR: Unable to determine your location for mapping."
    
    # Generate a simple ASCII art map with the player's location
    # This is a simplified map; in a real implementation, you would generate 
    # a dynamic map based on the station layout and visited rooms
    room_name = interface.get_room_name(player_location) or "UNKNOWN"
    
    # Example simplified map
    map_art = f"""
    STATION MAP - YOU ARE AT: {room_name}
    
    +---------+----------+---------+
    |         |          |         |
    | SCIENCE | CORRIDOR | MEDBAY  |
    |         |          |         |
    +---------+----------+---------+
    |         |          |         |
    | STORAGE | BRIDGE   | SURGERY |
    |         |          |         |
    +---------+----------+---------+
    |         |          |         |
    | REACTOR | CORRIDOR | CARGO   |
    |         |          |         |
    +---------+----------+---------+
    """
    
    return map_art
