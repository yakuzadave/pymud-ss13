"""
Movement commands for MUDpy SS13.
These include moving between locations, teleporting (for admins), etc.
"""

import logging
from engine import register
from events import publish

logger = logging.getLogger(__name__)

@register("go")
def cmd_go(interface, client_id, args):
    """
    Move in a specified direction.
    
    Args:
        interface: The MUDpy interface instance.
        client_id: The ID of the client.
        args: The direction to move.
        
    Returns:
        str: Result of the movement.
    """
    if not args:
        return "Go where? Specify a direction like 'go north' or 'go east'."
    
    direction = args.lower()
    valid_directions = ["north", "south", "east", "west", "up", "down", "n", "s", "e", "w", "u", "d"]
    
    # Normalize shorthand directions
    if direction == "n":
        direction = "north"
    elif direction == "s":
        direction = "south"
    elif direction == "e":
        direction = "east"
    elif direction == "w":
        direction = "west"
    elif direction == "u":
        direction = "up"
    elif direction == "d":
        direction = "down"
    
    if direction not in valid_directions:
        return f"Invalid direction '{args}'. Try north, south, east, west, up, or down."
    
    # This is a placeholder that should be enhanced to use the world and component system
    return interface._go(client_id, direction)

@register("north")
def cmd_go_north(interface, client_id, args):
    """
    Shortcut to go north.
    
    Args:
        interface: The MUDpy interface instance.
        client_id: The ID of the client.
        args: Additional arguments (unused).
        
    Returns:
        str: Result of the movement.
    """
    return cmd_go(interface, client_id, "north")

@register("south")
def cmd_go_south(interface, client_id, args):
    """
    Shortcut to go south.
    
    Args:
        interface: The MUDpy interface instance.
        client_id: The ID of the client.
        args: Additional arguments (unused).
        
    Returns:
        str: Result of the movement.
    """
    return cmd_go(interface, client_id, "south")

@register("east")
def cmd_go_east(interface, client_id, args):
    """
    Shortcut to go east.
    
    Args:
        interface: The MUDpy interface instance.
        client_id: The ID of the client.
        args: Additional arguments (unused).
        
    Returns:
        str: Result of the movement.
    """
    return cmd_go(interface, client_id, "east")

@register("west")
def cmd_go_west(interface, client_id, args):
    """
    Shortcut to go west.
    
    Args:
        interface: The MUDpy interface instance.
        client_id: The ID of the client.
        args: Additional arguments (unused).
        
    Returns:
        str: Result of the movement.
    """
    return cmd_go(interface, client_id, "west")

@register("up")
def cmd_go_up(interface, client_id, args):
    """
    Shortcut to go up.
    
    Args:
        interface: The MUDpy interface instance.
        client_id: The ID of the client.
        args: Additional arguments (unused).
        
    Returns:
        str: Result of the movement.
    """
    return cmd_go(interface, client_id, "up")

@register("down")
def cmd_go_down(interface, client_id, args):
    """
    Shortcut to go down.
    
    Args:
        interface: The MUDpy interface instance.
        client_id: The ID of the client.
        args: Additional arguments (unused).
        
    Returns:
        str: Result of the movement.
    """
    return cmd_go(interface, client_id, "down")

# Single-letter shortcuts for movement
@register("n")
def cmd_go_n(interface, client_id, args):
    """Shortcut to go north."""
    return cmd_go(interface, client_id, "north")

@register("s")
def cmd_go_s(interface, client_id, args):
    """Shortcut to go south."""
    return cmd_go(interface, client_id, "south")

@register("e")
def cmd_go_e(interface, client_id, args):
    """Shortcut to go east."""
    return cmd_go(interface, client_id, "east")

@register("w")
def cmd_go_w(interface, client_id, args):
    """Shortcut to go west."""
    return cmd_go(interface, client_id, "west")

@register("u")
def cmd_go_u(interface, client_id, args):
    """Shortcut to go up."""
    return cmd_go(interface, client_id, "up")

@register("d")
def cmd_go_d(interface, client_id, args):
    """Shortcut to go down."""
    return cmd_go(interface, client_id, "down")