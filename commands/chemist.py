"""Chemist role specific commands."""

from engine import register
import world
from systems.chemistry import get_chemistry_system


@register("mix")
def mix_handler(client_id: str, *chemicals, **kwargs):
    """Mix chemicals if player is a chemist."""
    player = world.get_world().get_object(f"player_{client_id}")
    if not player:
        return "Player not found."
    comp = player.get_component("player")
    if not comp or comp.role.lower() != "chemist":
        return "Only chemists can do that."
    if not chemicals:
        return "Specify chemicals to mix."
    system = get_chemistry_system()
    return system.craft(client_id, list(chemicals))
