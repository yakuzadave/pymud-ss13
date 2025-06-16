"""
Interaction commands for MUDpy SS13.
These include interacting with objects, NPCs, etc.
"""

import logging
from engine import register
from world import get_world
from systems.script_engine import get_script_engine


def _find_openable(interface, client_id: str, identifier: str):
    """Locate a DoorComponent or ContainerComponent."""
    world = get_world()
    player = world.get_object(f"player_{client_id}")
    if not player:
        return None, "Player not found."

    pcomp = player.get_component("player")
    if not pcomp:
        return None, "Player data missing."

    current_room_id = pcomp.current_location or interface.get_player_location(client_id)
    if not current_room_id:
        return None, "You are nowhere."

    identifier = identifier.lower()

    # Check if identifier is a direction relative to the current room
    room_obj = world.get_object(current_room_id)
    if room_obj:
        room_comp = room_obj.get_component("room")
        if room_comp:
            dest_id = room_comp.get_exit(identifier)
            if dest_id:
                target_obj = world.get_object(dest_id)
                if target_obj:
                    door_comp = target_obj.get_component("door")
                    if door_comp:
                        return door_comp, "door", None
                    cont_comp = target_obj.get_component("container")
                    if cont_comp:
                        return cont_comp, "container", None

    # Otherwise treat identifier as an object id
    target_obj = world.get_object(identifier)
    if target_obj:
        door_comp = target_obj.get_component("door")
        if door_comp:
            return door_comp, "door", None
        cont_comp = target_obj.get_component("container")
        if cont_comp:
            return cont_comp, "container", None

    return None, "", f"There is no door or container '{identifier}' here."


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

    comp, ctype, err = _find_openable(interface, client_id, args)
    if not comp:
        return err

    world = get_world()
    player = world.get_object(f"player_{client_id}")
    pcomp = player.get_component("player") if player else None
    access = pcomp.access_level if pcomp else 0

    return comp.open(
        player_id=player.id if player else str(client_id), access_code=access
    )


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

    comp, ctype, err = _find_openable(interface, client_id, args)
    if not comp:
        return err

    world = get_world()
    player = world.get_object(f"player_{client_id}")

    return comp.close(player_id=player.id if player else str(client_id))


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

    comp, ctype, err = _find_openable(interface, client_id, args)
    if not comp:
        return err

    world = get_world()
    player = world.get_object(f"player_{client_id}")
    pcomp = player.get_component("player") if player else None
    access = pcomp.access_level if pcomp else 0

    return comp.lock(
        player_id=player.id if player else str(client_id), access_code=access
    )


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

    comp, ctype, err = _find_openable(interface, client_id, args)
    if not comp:
        return err

    world = get_world()
    player = world.get_object(f"player_{client_id}")
    pcomp = player.get_component("player") if player else None
    access = pcomp.access_level if pcomp else 0

    return comp.unlock(
        player_id=player.id if player else str(client_id), access_code=access
    )


@register("hack")
def cmd_hack(interface, client_id, args):
    """Attempt to hack open a door or container."""
    if not args:
        return "Hack what? Specify a target."

    comp, ctype, err = _find_openable(interface, client_id, args)
    if not comp:
        return err

    world = get_world()
    player = world.get_object(f"player_{client_id}")
    pcomp = player.get_component("player") if player else None
    skill = 0
    if pcomp:
        skill = pcomp.skills.get("hacking", 0)

    return comp.hack(player_id=player.id if player else str(client_id), skill=skill)


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


@register("verb")
def cmd_verb(interface, client_id, args):
    """Invoke a custom verb on a game object."""
    if not args:
        return "Usage: verb <object_id> <verb> [args]"

    parts = args.split(maxsplit=2)
    if len(parts) < 2:
        return "Usage: verb <object_id> <verb> [args]"

    obj_id, verb = parts[0], parts[1]
    extra = parts[2] if len(parts) > 2 else ""

    world = get_world()
    obj = world.get_object(obj_id)
    if not obj:
        return f"Object '{obj_id}' not found."

    engine = get_script_engine()
    context = {
        "interface": interface,
        "client_id": client_id,
        "args": extra,
        "object": obj,
        "result": None,
    }

    result = engine.run_verb(obj_id, verb, context)
    if result is None:
        return f"Verb '{verb}' not found on {obj_id}."
    return result.get("result", f"{verb} executed.")
