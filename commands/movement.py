"""
Movement command handlers for MUDpy SS13.
This module provides handlers for movement commands like go, sprint, etc.
"""

import logging
from typing import Optional, Dict, Any

# Configure logging
logger = logging.getLogger(__name__)

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
    elif direction == "u":
        direction = "up"
    elif direction == "d":
        direction = "down"

    # Check if the direction is valid
    if direction not in ["north", "south", "east", "west", "up", "down"]:
        return f"'{direction}' is not a valid direction."

    # Get current location
    current_location = interface.get_player_location(client_id)
    if not current_location:
        return "You are nowhere. This is a strange phenomenon indeed."

    # Get exits from current location
    exits = interface.get_exits_from_room(current_location)

    # Check if the direction is a valid exit
    if direction not in exits:
        return f"You can't go {direction} from here."

    # Get target location
    target_location = exits[direction]

    # Check for locked doors or other barriers
    door_is_locked = False  # This would be checked by calling interface.is_door_locked(current_location, direction)
    if door_is_locked:
        return f"The door to the {direction} is locked."

    # Consume energy
    if hasattr(interface, 'modify_player_stat'):
        interface.modify_player_stat(client_id, 'energy', -1)

    # Move the player
    previous_location = current_location
    interface.set_player_location(client_id, target_location)

    # Publish the movement event
    from events import publish
    publish("player_moved",
            player_id=client_id,
            from_location=previous_location,
            to_location=target_location)

    # Return a description of the new location
    return interface._look(client_id)

def sprint_handler(client_id: str, direction: str, **kwargs) -> str:
    """
    Handle the sprint command (move two rooms at once).

    Args:
        client_id: The ID of the client issuing the command.
        direction: The direction to sprint.

    Returns:
        Result of the sprint attempt.
    """
    logger.debug(f"Sprint command called by client {client_id} with direction {direction}")

    # Get the interface from kwargs
    interface = kwargs.get('interface')
    if not interface:
        return "Error: Interface not available"

    # Check energy levels
    stats = interface.get_player_stats(client_id)
    if stats and stats.get('energy', 0) < 10:
        return "You are too tired to sprint. Rest a bit first."

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
    elif direction == "u":
        direction = "up"
    elif direction == "d":
        direction = "down"

    # Move once
    result = move_handler(client_id, direction, **kwargs)

    # If successful, move again
    if not result.startswith("You can't") and not result.startswith("The door"):
        # Get current location after first move
        current_location = interface.get_player_location(client_id)

        # Get exits from current location
        exits = interface.get_exits_from_room(current_location)

        # Check if we can continue in the same direction
        if direction in exits:
            # Consume extra energy
            if hasattr(interface, 'modify_player_stat'):
                interface.modify_player_stat(client_id, 'energy', -5)

            # Move again
            result = move_handler(client_id, direction, **kwargs)

            # Add sprint message
            return f"You sprint {direction} with great speed!\n\n{result}"
        else:
            return f"You sprint {direction} but come to a stop.\n\n{result}"

    return result
