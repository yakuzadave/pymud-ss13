"""
Interaction commands for MUDpy SS13.
These include interacting with objects, NPCs, etc.
"""

import logging
from engine import register
from events import publish

logger = logging.getLogger(__name__)

@register("open")
def cmd_open(interface, client_id, args):
    """
    Open a door or container.

    Args:
        interface: The MUDpy interface instance.
        client_id: The ID of the client.
        args: The direction or object to open.

    Returns:
        str: Result of the open attempt.
    """
    if not args:
        return "Open what? Specify a direction (e.g., 'open north') or an object."

    # This is a placeholder that should be enhanced to use the world and component system
    return f"You try to open {args}, but it doesn't seem to work."

@register("close")
def cmd_close(interface, client_id, args):
    """
    Close a door or container.

    Args:
        interface: The MUDpy interface instance.
        client_id: The ID of the client.
        args: The direction or object to close.

    Returns:
        str: Result of the close attempt.
    """
    if not args:
        return "Close what? Specify a direction (e.g., 'close north') or an object."

    # This is a placeholder that should be enhanced to use the world and component system
    return f"You try to close {args}, but it doesn't seem to work."

@register("lock")
def cmd_lock(interface, client_id, args):
    """
    Lock a door or container.

    Args:
        interface: The MUDpy interface instance.
        client_id: The ID of the client.
        args: The direction or object to lock.

    Returns:
        str: Result of the lock attempt.
    """
    if not args:
        return "Lock what? Specify a direction (e.g., 'lock north') or an object."

    # This is a placeholder that should be enhanced to use the world and component system
    return f"You try to lock {args}, but you don't have the proper key or access code."

@register("unlock")
def cmd_unlock(interface, client_id, args):
    """
    Unlock a door or container.

    Args:
        interface: The MUDpy interface instance.
        client_id: The ID of the client.
        args: The direction or object to unlock.

    Returns:
        str: Result of the unlock attempt.
    """
    if not args:
        return "Unlock what? Specify a direction (e.g., 'unlock north') or an object."

    # This is a placeholder that should be enhanced to use the world and component system
    return f"You try to unlock {args}, but you don't have the proper key or access code."

@register("push")
def cmd_push(interface, client_id, args):
    """
    Push an object or button.

    Args:
        interface: The MUDpy interface instance.
        client_id: The ID of the client.
        args: The object to push.

    Returns:
        str: Result of the push attempt.
    """
    if not args:
        return "Push what? Specify an object to push."

    # This is a placeholder that should be enhanced to use the world and component system
    return f"You push {args}, but nothing happens."

@register("pull")
def cmd_pull(interface, client_id, args):
    """
    Pull an object or lever.

    Args:
        interface: The MUDpy interface instance.
        client_id: The ID of the client.
        args: The object to pull.

    Returns:
        str: Result of the pull attempt.
    """
    if not args:
        return "Pull what? Specify an object to pull."

    # This is a placeholder that should be enhanced to use the world and component system
    return f"You pull {args}, but nothing happens."

@register("turn")
def cmd_turn(interface, client_id, args):
    """
    Turn an object, dial, or valve.

    Args:
        interface: The MUDpy interface instance.
        client_id: The ID of the client.
        args: The object to turn and possibly a direction.

    Returns:
        str: Result of the turn attempt.
    """
    if not args:
        return "Turn what? Specify an object to turn."

    # This is a placeholder that should be enhanced to use the world and component system
    return f"You turn {args}, but nothing happens."
