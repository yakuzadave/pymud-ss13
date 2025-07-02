"""Combat-related commands for attacking and throwing items."""

import logging
from engine import register
from events import publish
from world import get_world

logger = logging.getLogger(__name__)


def _get_player_obj(client_id):
    world = get_world()
    return world.get_object(f"player_{client_id}")


@register("attack")
def cmd_attack(interface, client_id, target: str, item: str = None, **_):
    """Attack another entity with a weapon or bare hands."""
    if not target:
        return "Attack whom?"

    world = get_world()
    attacker = _get_player_obj(client_id)
    if not attacker:
        return "Player not found."

    defender = world.get_object(target)
    if not defender:
        return f"Target '{target}' not found."

    weapon = item or "fists"
    publish(
        "player_attacked",
        attacker_id=client_id,
        target_id=target,
        weapon=weapon,
    )
    return f"You attack {target} with {weapon}."


@register("throw")
def cmd_throw(interface, client_id, item: str, target: str, **_):
    """Throw an item at a target."""
    if not item or not target:
        return "Usage: throw <item> at <target>"

    world = get_world()
    player = _get_player_obj(client_id)
    if not player:
        return "Player not found."
    pcomp = player.get_component("player")
    if not pcomp or item not in pcomp.inventory:
        return f"You aren't carrying {item}."

    tgt_obj = world.get_object(target)
    if not tgt_obj:
        return f"Target '{target}' not found."

    pcomp.remove_from_inventory(item)
    obj = world.get_object(item)
    if obj:
        obj.location = tgt_obj.location
    publish(
        "item_thrown",
        player_id=client_id,
        item_id=item,
        target_id=target,
    )
    return f"You throw {item} at {target}."
