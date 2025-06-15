"""
Debug commands for MUDpy SS13.
These include script management, world inspection, etc.
They should be disabled in production.
"""

import logging
from engine import register
from events import publish
from systems.script_engine import get_script_engine

logger = logging.getLogger(__name__)


@register("addverb")
def cmd_addverb(interface, client_id, args):
    """
    Add a custom verb to an object.

    Args:
        interface: The MUDpy interface instance.
        client_id: The ID of the client.
        args: Arguments in the format "object_id verb_name code".

    Returns:
        str: Result of adding the verb.
    """
    # Get the client's session data
    session = interface.client_sessions.get(client_id, {})
    is_admin = session.get("is_admin", False)
    player_name = session.get("player_name", "Unknown")

    # Only admins can add verbs for now
    if not is_admin:
        return "You do not have permission to add verbs."

    # Parse arguments
    parts = args.split(maxsplit=2)
    if len(parts) < 3:
        return "Usage: addverb <object_id> <verb_name> <code>"

    obj_id, verb_name, code = parts

    # Add the verb to the object
    engine = get_script_engine()
    script_id = engine.add_verb(obj_id, verb_name, code, owner_id=client_id)

    if script_id:
        return f"Added verb '{verb_name}' to object {obj_id}."
    else:
        return f"Failed to add verb '{verb_name}' to object {obj_id}."


@register("listscripts")
def cmd_listscripts(interface, client_id, args):
    """
    List registered scripts.

    Args:
        interface: The MUDpy interface instance.
        client_id: The ID of the client.
        args: Optional owner ID to filter by.

    Returns:
        str: List of scripts.
    """
    # Get the client's session data
    session = interface.client_sessions.get(client_id, {})
    is_admin = session.get("is_admin", False)

    # Only admins can list all scripts
    if args and not is_admin:
        return "You do not have permission to list scripts for other users."

    owner_id = args if args and is_admin else client_id
    engine = get_script_engine()
    scripts = engine.list_scripts(owner_id if args else None)

    if not scripts:
        return "No scripts found."

    script_list = []
    for script_id, info in scripts.items():
        owner = info.get("owner_id", "unknown")
        script_list.append(f"{script_id} (by {owner})")

    return "Registered scripts:\n" + "\n".join(script_list)


@register("delscript")
def cmd_delscript(interface, client_id, args):
    """
    Delete a registered script.

    Args:
        interface: The MUDpy interface instance.
        client_id: The ID of the client.
        args: The ID of the script to delete.

    Returns:
        str: Result of deleting the script.
    """
    if not args:
        return "Usage: delscript <script_id>"

    script_id = args

    # Get script info
    engine = get_script_engine()
    script_info = engine.get_script_info(script_id)
    if not script_info:
        return f"Script '{script_id}' not found."

    # Get the client's session data
    session = interface.client_sessions.get(client_id, {})
    is_admin = session.get("is_admin", False)

    # Check if the client is allowed to delete this script
    if script_info["owner_id"] != client_id and not is_admin:
        return "You do not have permission to delete this script."

    # Delete the script
    success = engine.remove_script(script_id)

    if success:
        return f"Script '{script_id}' deleted."
    else:
        return f"Failed to delete script '{script_id}'."


@register("runscript")
def cmd_runscript(interface, client_id, args):
    """
    Run a registered script.

    Args:
        interface: The MUDpy interface instance.
        client_id: The ID of the client.
        args: The ID of the script to run.

    Returns:
        str: Result of running the script.
    """
    if not args:
        return "Usage: runscript <script_id>"

    script_id = args

    # Get script info
    engine = get_script_engine()
    script_info = engine.get_script_info(script_id)
    if not script_info:
        return f"Script '{script_id}' not found."

    # Get the client's session data
    session = interface.client_sessions.get(client_id, {})

    # Create a context for the script
    context = {
        "player_id": client_id,
        "player_name": session.get("player_name", "Unknown"),
        "location": session.get("location", "nowhere"),
        "result": None,
    }

    # Run the script
    result = engine.execute_script(script_id, context)

    if result is None:
        return f"Failed to run script '{script_id}'."
    else:
        # Return the script's result if set, otherwise a generic success message
        return result.get("result", f"Script '{script_id}' ran successfully.")


@register("debug")
def cmd_debug(interface, client_id, args):
    """
    Debug command for inspecting the game state.

    Args:
        interface: The MUDpy interface instance.
        client_id: The ID of the client.
        args: What to debug.

    Returns:
        str: Debug information.
    """
    # Get the client's session data
    session = interface.client_sessions.get(client_id, {})
    is_admin = session.get("is_admin", False)

    # Only admins can use debug commands
    if not is_admin:
        return "You do not have permission to use debug commands."

    if not args:
        return "Usage: debug <target> [args]"

    parts = args.split(maxsplit=1)
    target = parts[0].lower()
    target_args = parts[1] if len(parts) > 1 else ""

    if target == "session":
        # Debug the client's session
        return f"Session data for client {client_id}:\n" + "\n".join(
            [f"{k}: {v}" for k, v in session.items()]
        )
    elif target == "clients":
        # List all connected clients
        clients = interface.client_sessions.keys()
        return f"Connected clients ({len(clients)}):\n" + "\n".join(
            [str(c) for c in clients]
        )
    elif target == "world":
        # Debug the world state (simple placeholder)
        return "World state debugging not implemented yet."
    else:
        return f"Unknown debug target '{target}'."
