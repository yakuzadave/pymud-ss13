"""Chef role specific commands."""

from engine import register
import world
from systems.kitchen import get_kitchen_system


@register("cook")
def cook_handler(client_id: str, *ingredients, **kwargs):
    """Cook a meal using ingredients from your inventory."""
    player = world.get_world().get_object(f"player_{client_id}")
    if not player:
        return "Player not found."
    comp = player.get_component("player")
    if not comp or comp.role.lower() != "chef":
        return "Only chefs can do that."
    if not ingredients:
        return "Specify ingredients to cook."
    system = get_kitchen_system()
    return system.cook(client_id, list(ingredients))
