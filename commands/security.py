"""Security role commands."""

from engine import register
from events import publish
import world

@register("restrain")
def restrain_handler(client_id: str, target: str = None, **kwargs):
    """Restrain a target if player is security."""
    player = world.get_world().get_object(f"player_{client_id}")
    if not player:
        return "Player not found."
    comp = player.get_component("player")
    if not comp or comp.role.lower() != "security":
        return "Only security officers can do that."
    publish("restrain_attempt", player_id=player.id, target=target)
    return f"You restrain {target or 'the suspect'}."
