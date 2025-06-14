"""
System commands for MUDpy SS13.
These include quitting, saving, admin commands, etc.
"""

import logging
from engine import register
from events import publish

logger = logging.getLogger(__name__)


@register("quit")
def cmd_quit(interface, client_id, args):
    """
    Quit the game and disconnect.

    Args:
        interface: The MUDpy interface instance.
        client_id: The ID of the client.
        args: Additional arguments (unused).

    Returns:
        str: Quit message.
    """
    # Get the client's session data
    session = interface.client_sessions.get(client_id, {})
    player_name = session.get("player_name", "Unknown")

    # Publish an event for this quit
    publish("player_quit", client_id=client_id, player_name=player_name)

    # Clean up the client session
    interface.disconnect_client(client_id)

    return "You have disconnected from Space Station Alpha. Safe travels."


@register("save")
def cmd_save(interface, client_id, args):
    """
    Save the current game state.

    Args:
        interface: The MUDpy interface instance.
        client_id: The ID of the client.
        args: Additional arguments (unused).

    Returns:
        str: Save confirmation message.
    """
    # This is a placeholder that should be enhanced to use the world system

    # Get the client's session data
    session = interface.client_sessions.get(client_id, {})
    player_name = session.get("player_name", "Unknown")

    # Save the configuration (this should be expanded to use the world system)
    interface.save_config()

    # Publish an event for this save
    publish("game_saved", client_id=client_id, player_name=player_name)

    return "Game state saved."


@register("shutdown")
def cmd_shutdown(interface, client_id, args):
    """
    Shut down the server (admin only).

    Args:
        interface: The MUDpy interface instance.
        client_id: The ID of the client.
        args: Additional arguments (unused).

    Returns:
        str: Shutdown confirmation or denial message.
    """
    # Get the client's session data
    session = interface.client_sessions.get(client_id, {})
    is_admin = session.get("is_admin", False)

    if not is_admin:
        return "You do not have permission to shut down the server."

    # This is a placeholder - in a real implementation, you would:
    # 1. Broadcast a shutdown message to all clients
    # 2. Save the game state
    # 3. Gracefully shut down the server

    publish("server_shutdown", client_id=client_id, reason="admin command")

    return "Server shutdown initiated."


@register("event")
def cmd_event(interface, client_id, args):
    """List or trigger random events."""
    session = interface.client_sessions.get(client_id, {})
    is_admin = session.get("is_admin", False)

    from systems.random_events import get_random_event_system

    system = get_random_event_system()
    if not system.events:
        system.load_events()

    if not args or args.strip().lower() in {"list", "ls"}:
        events = system.list_events()
        if not events:
            return "No random events are defined."
        return "Available events: " + ", ".join(events)

    parts = args.split(maxsplit=1)
    cmd = parts[0].lower()
    if cmd in {"trigger", "run", "fire"}:
        if not is_admin:
            return "You do not have permission to trigger events."
        if len(parts) < 2:
            return "Usage: event trigger <event_id>"
        event_id = parts[1]
        if system.trigger_event(event_id, client_id=client_id):
            # Notify subscribers that a manual event has fired.
            # Useful for logging or debugging purposes.
            publish(
                "manual_event_triggered",
                event_id=event_id,
                client_id=client_id,
            )
            return f"Event {event_id} triggered."
        else:
            return f"Unknown event: {event_id}"
    else:
        return f"Unknown event command '{cmd}'."


@register("who")
def cmd_who(interface, client_id, args=None):
    """Return a list of currently connected players."""
    sessions = getattr(interface, "client_sessions", {})
    if not sessions:
        return "No players are currently online."

    names = []
    for session in sessions.values():
        name = session.get("character") or session.get("player_name")
        if name:
            names.append(name)

    if not names:
        return "No players are currently online."

    return "Players online: " + ", ".join(sorted(names))
