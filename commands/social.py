"""
Social command handlers for MUDpy SS13.
This module provides handlers for communication commands like say, shout, whisper, etc.
"""

import logging
from typing import Optional, Dict, Any
from engine import register

# Configure logging
logger = logging.getLogger(__name__)


@register("say")
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
    interface = kwargs.get("interface")
    if not interface:
        return "Error: Interface not available"

    # Get player location
    player_location = interface.get_player_location(client_id)

    if not player_location:
        return "You are nowhere. Your words echo into the void."

    # Get player name
    player_name = "Unknown"
    session = interface.get_session(client_id)
    if session and "character" in session:
        player_name = session["character"]

    # Publish event for this message
    from events import publish

    publish(
        "player_said",
        client_id=client_id,
        location=player_location,
        message=message,
        name=player_name,
    )

    return f"You say: {message}"


@register("shout")
def shout_handler(client_id: str, message: str, **kwargs) -> str:
    """
    Handle the shout command.

    Args:
        client_id: The ID of the client issuing the command.
        message: The message to shout.

    Returns:
        Confirmation of the message.
    """
    logger.debug(f"Shout command called by client {client_id} with message: {message}")

    # Get the interface from kwargs
    interface = kwargs.get("interface")
    if not interface:
        return "Error: Interface not available"

    # Get player location
    player_location = interface.get_player_location(client_id)

    if not player_location:
        return "You are nowhere. Your shouts echo into the void."

    # Get player name
    player_name = "Unknown"
    session = interface.get_session(client_id)
    if session and "character" in session:
        player_name = session["character"]

    # Get adjacent rooms
    adjacent_rooms = interface.get_adjacent_rooms(player_location)

    # Publish event for shouting to current and adjacent rooms
    from events import publish

    publish(
        "player_shouted",
        client_id=client_id,
        location=player_location,
        adjacent_rooms=adjacent_rooms,
        message=message,
        name=player_name,
    )

    # Consume some energy for shouting
    if hasattr(interface, "modify_player_stat"):
        interface.modify_player_stat(client_id, "energy", -5)

    return f"You shout: {message.upper()}!"


@register("whisper")
def whisper_handler(client_id: str, player: str, message: str, **kwargs) -> str:
    """
    Handle the whisper command.

    Args:
        client_id: The ID of the client issuing the command.
        player: The player to whisper to.
        message: The message to whisper.

    Returns:
        Confirmation of the message.
    """
    logger.debug(
        f"Whisper command called by client {client_id} to {player} with message: {message}"
    )

    # Get the interface from kwargs
    interface = kwargs.get("interface")
    if not interface:
        return "Error: Interface not available"

    # Get player location
    player_location = interface.get_player_location(client_id)

    if not player_location:
        return "You are nowhere. There is no one to whisper to."

    # Get player name
    whisperer_name = "Unknown"
    session = interface.get_session(client_id)
    if session and "character" in session:
        whisperer_name = session["character"]

    # Find the target player
    target_id = None
    for other_id in interface.get_clients():
        other_session = interface.get_session(other_id)
        if other_session and "character" in other_session:
            if other_session["character"].lower() == player.lower():
                # Check if in same location
                other_location = interface.get_player_location(other_id)
                if other_location == player_location:
                    target_id = other_id
                    break

    if not target_id:
        return f"There is no one named '{player}' here."

    # Send a message to the target player
    from events import publish

    publish(
        "player_whispered",
        source_id=client_id,
        target_id=target_id,
        message=message,
        source_name=whisperer_name,
    )

    return f"You whisper to {player}: {message}"


@register("tell")
def tell_handler(client_id: str, player: str, message: str, **kwargs) -> str:
    """
    Handle the tell command (private message).

    Args:
        client_id: The ID of the client issuing the command.
        player: The player to message.
        message: The message to send.

    Returns:
        Confirmation of the message.
    """
    logger.debug(
        f"Tell command called by client {client_id} to {player} with message: {message}"
    )

    # Get the interface from kwargs
    interface = kwargs.get("interface")
    if not interface:
        return "Error: Interface not available"

    # Get player name
    sender_name = "Unknown"
    session = interface.get_session(client_id)
    if session and "character" in session:
        sender_name = session["character"]

    # Find the target player anywhere on the station
    target_id = None
    for other_id in interface.get_clients():
        other_session = interface.get_session(other_id)
        if other_session and "character" in other_session:
            if other_session["character"].lower() == player.lower():
                target_id = other_id
                break

    if not target_id:
        return f"There is no one named '{player}' online."

    # Check if sender has a communications device
    inventory = interface.get_player_inventory(client_id)
    has_comms = False
    for item_id in inventory:
        if item_id == "comms_device":
            has_comms = True
            break

    if not has_comms:
        return "You need a communications device to send private messages."

    # Send a message to the target player
    from events import publish

    publish(
        "player_tell",
        source_id=client_id,
        target_id=target_id,
        message=message,
        source_name=sender_name,
    )

    return f"You tell {player}: {message}"


@register("emote")
def emote_handler(client_id: str, action: str, **kwargs) -> str:
    """Perform a custom emote action."""
    world_obj = None
    try:
        from world import get_world

        world_obj = get_world().get_object(f"player_{client_id}")
    except Exception:
        world_obj = None
    name = world_obj.name if world_obj else f"Player_{client_id}"
    from events import publish
    publish("player_emoted", client_id=client_id, action=action, name=name)
    return f"You {action}"


def _simple_emote(client_id: str, action: str, target: Optional[str]) -> str:
    full = action if not target else f"{action} at {target}"
    return emote_handler(client_id, full)


@register("wave")
def wave_handler(client_id: str, target: Optional[str] = None, **_kwargs) -> str:
    return _simple_emote(client_id, "wave", target)


@register("smile")
def smile_handler(client_id: str, target: Optional[str] = None, **_kwargs) -> str:
    return _simple_emote(client_id, "smile", target)


@register("nod")
def nod_handler(client_id: str, target: Optional[str] = None, **_kwargs) -> str:
    return _simple_emote(client_id, "nod", target)


@register("ooc")
def ooc_handler(client_id: str, message: str, **kwargs) -> str:
    """
    Handle the out-of-character (OOC) command.

    Args:
        client_id: The ID of the client issuing the command.
        message: The OOC message.

    Returns:
        Confirmation of the message.
    """
    logger.debug(f"OOC command called by client {client_id} with message: {message}")

    # Get the interface from kwargs
    interface = kwargs.get("interface")
    if not interface:
        return "Error: Interface not available"

    # Get player name
    player_name = "Unknown"
    session = interface.get_session(client_id)
    if session and "character" in session:
        player_name = session["character"]

    # Publish event for OOC message to all players
    from events import publish

    publish("player_ooc", client_id=client_id, message=message, name=player_name)

    return f"OOC: {message}"
