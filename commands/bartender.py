"""Bartender role commands."""

from engine import register
import world
from systems.bar import get_bar_system


@register("mixdrink")
def mixdrink_handler(client_id: str, *ingredients, **kwargs):
    """Mix a cocktail using bar ingredients."""
    player = world.get_world().get_object(f"player_{client_id}")
    if not player:
        return "Player not found."
    comp = player.get_component("player")
    if not comp or comp.role.lower() != "bartender":
        return "Only bartenders can do that."
    if not ingredients:
        return "Specify ingredients to mix."
    system = get_bar_system()
    return system.mix(client_id, list(ingredients))
