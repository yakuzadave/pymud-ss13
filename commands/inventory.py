"""
Inventory command handlers for MUDpy SS13.
Provides basic item manipulation and container interactions.
"""

import logging
import os
from typing import Optional, List

from engine import register
from world import get_world
from persistence import save_game_object

logger = logging.getLogger(__name__)


def _find_object_by_name(name: str, objects: List) -> Optional:
    """Return the first object whose id or name contains ``name``."""
    if not name:
        return None
    name = name.lower()
    for obj in objects:
        if name in obj.id.lower() or name in obj.name.lower():
            return obj
    return None


def _save_container(obj):
    world = get_world()
    path = os.path.join(world.data_dir, "world", f"{obj.id}.yaml")
    try:
        save_game_object(obj, path)
    except Exception as exc:
        logger.error(f"Failed to save container {obj.id}: {exc}")


@register("inventory")
def cmd_inventory(interface, client_id, **_):
    """List items in a player's inventory."""
    return interface._inventory(client_id)


@register("i")
def cmd_i(interface, client_id, **kwargs):
    return cmd_inventory(interface, client_id, **kwargs)


@register("get")
def cmd_get(interface, client_id, item: str, container: Optional[str] = None, **_):
    """Take an item from the room or from a container."""
    if not item:
        return "Get what?"

    if not container:
        return interface._take(client_id, item)

    world = get_world()
    player = world.get_object(f"player_{client_id}")
    if not player:
        return "Player not found."
    player_comp = player.get_component("player")
    location = player.location
    room_objs = world.get_objects_in_location(location)
    inv_objs = [world.get_object(i) for i in player_comp.inventory if world.get_object(i)]

    cont_obj = _find_object_by_name(container, room_objs + inv_objs)
    if not cont_obj or not cont_obj.get_component("container"):
        return f"You don't see a '{container}'."

    cont_comp = cont_obj.get_component("container")
    item_objs = [world.get_object(i) for i in cont_comp.items if world.get_object(i)]
    itm_obj = _find_object_by_name(item, item_objs)
    if not itm_obj:
        return f"There is no {item} in {cont_obj.name}."

    if not player_comp.add_to_inventory(itm_obj.id):
        return "Your inventory is full."

    cont_comp.remove_item(itm_obj.id)
    itm_obj.location = None
    _save_container(cont_obj)
    return f"You take the {itm_obj.name} from {cont_obj.name}."


@register("take")
def cmd_take(interface, client_id, item: str, container: Optional[str] = None, **kwargs):
    return cmd_get(interface, client_id, item, container, **kwargs)


@register("drop")
def cmd_drop(interface, client_id, item: str, **_):
    if not item:
        return "Drop what?"
    return interface._drop(client_id, item)


@register("put")
def cmd_put(interface, client_id, item: str, container: str, **_):
    """Place an item from inventory into a container."""
    if not item or not container:
        return "Usage: put <item> in <container>"

    world = get_world()
    player = world.get_object(f"player_{client_id}")
    if not player:
        return "Player not found."
    player_comp = player.get_component("player")

    if item not in player_comp.inventory:
        # try fuzzy match
        itm_obj = _find_object_by_name(item, [world.get_object(i) for i in player_comp.inventory if world.get_object(i)])
        if not itm_obj:
            return f"You aren't carrying {item}."
        item_id = itm_obj.id
    else:
        item_id = item
        itm_obj = world.get_object(item_id)

    location = player.location
    room_objs = world.get_objects_in_location(location)
    inv_objs = [world.get_object(i) for i in player_comp.inventory if world.get_object(i)]

    cont_obj = _find_object_by_name(container, room_objs + inv_objs)
    if not cont_obj or not cont_obj.get_component("container"):
        return f"You don't see a '{container}'."

    cont_comp = cont_obj.get_component("container")
    if not cont_comp.add_item(item_id):
        return f"{cont_obj.name} can't hold any more items."

    player_comp.remove_from_inventory(item_id)
    if itm_obj:
        itm_obj.location = cont_obj.id
    _save_container(cont_obj)
    return f"You put the {itm_obj.name if itm_obj else item_id} in {cont_obj.name}."


@register("use")
def cmd_use(interface, client_id, item: str, **_):
    if not item:
        return "Use what? Specify an item to use."
    return interface._use(client_id, item)


@register("examine")
def cmd_examine(interface, client_id, item: str, **_):
    if not item:
        return "Examine what? Specify an item to examine."
    return interface._examine(client_id, item)


@register("x")
def cmd_x(interface, client_id, item: str, **kwargs):
    return cmd_examine(interface, client_id, item, **kwargs)
