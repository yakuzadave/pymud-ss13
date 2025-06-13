"""Doctor role specific commands."""

from engine import register
from events import publish
import world

@register("heal")
def heal_handler(client_id: str, target: str = None, **kwargs):
    """Heal a player if you are a doctor."""
    player = world.get_world().get_object(f"player_{client_id}")
    if not player:
        return "Player not found."
    comp = player.get_component("player")
    if not comp or comp.role.lower() != "doctor":
        return "Only doctors can do that."
    publish("heal_attempt", player_id=player.id, target=target)
    return f"You heal {target or 'the patient'}."
