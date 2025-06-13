"""Engineer role specific commands."""

from engine import register
from events import publish
import world

@register("repair")
def repair_handler(client_id: str, target: str = None, **kwargs):
    """Repair a subsystem if player is an engineer."""
    player = world.get_world().get_object(f"player_{client_id}")
    if not player:
        return "Player not found."
    comp = player.get_component("player")
    if not comp or comp.role.lower() != "engineer":
        return "Only engineers can do that."
    publish("repair_attempt", player_id=player.id, target=target)
    return f"You repair {target or 'the equipment'}."
