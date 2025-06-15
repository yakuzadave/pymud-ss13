"""Botanist role specific commands."""

from engine import register
import world
from systems.botany import get_botany_system


def _check_role(client_id: str) -> world.GameObject:
    player = world.get_world().get_object(f"player_{client_id}")
    if not player:
        return None
    comp = player.get_component("player")
    if not comp or comp.role.lower() != "botanist":
        return None
    return player


@register("plant")
def plant_handler(client_id: str, species: str = None, **kwargs):
    """Plant a seed into a tray."""
    player = _check_role(client_id)
    if not player:
        return "Only botanists can do that."
    if not species:
        return "Specify a seed species."
    system = get_botany_system()
    plant = system.plant_seed(species)
    return f"You plant {species} ({plant.plant_id})."


@register("harvest")
def harvest_handler(client_id: str, plant_id: str = None, **kwargs):
    """Harvest a mature plant."""
    player = _check_role(client_id)
    if not player:
        return "Only botanists can do that."
    if not plant_id:
        return "Specify a plant id."
    system = get_botany_system()
    if system.harvest(plant_id):
        return f"You harvest {plant_id}."
    return "That plant is not ready."


@register("fertilize")
def fertilize_handler(client_id: str, plant_id: str = None, chemical: str = None, **kwargs):
    """Apply a chemical to a plant."""
    player = _check_role(client_id)
    if not player:
        return "Only botanists can do that."
    if not plant_id or not chemical:
        return "Specify plant id and chemical."
    system = get_botany_system()
    system.apply_fertilizer(plant_id, chemical)
    return f"You apply {chemical} to {plant_id}."


@register("autogrow")
def autogrow_handler(client_id: str, plant_id: str = None, **kwargs):
    """Toggle autogrow on a tray."""
    player = _check_role(client_id)
    if not player:
        return "Only botanists can do that."
    if not plant_id:
        return "Specify a plant id."
    system = get_botany_system()
    status = system.toggle_autogrow(plant_id)
    return "Autogrow on." if status else "Autogrow off."


@register("graft")
def graft_handler(client_id: str, target_id: str = None, donor_id: str = None, **kwargs):
    """Graft traits from one plant to another."""
    player = _check_role(client_id)
    if not player:
        return "Only botanists can do that."
    if not target_id or not donor_id:
        return "Specify target and donor plant ids."
    system = get_botany_system()
    if system.graft(target_id, donor_id):
        return f"You graft {donor_id} onto {target_id}."
    return "Grafting failed."


@register("analyze")
def analyze_handler(client_id: str, plant_id: str = None, **kwargs):
    """Analyze a plant for its statistics."""
    player = _check_role(client_id)
    if not player:
        return "Only botanists can do that."
    if not plant_id:
        return "Specify a plant id."
    system = get_botany_system()
    stats = system.analyze_plant(plant_id)
    if not stats:
        return "No such plant."
    return ", ".join(f"{k}: {v}" for k, v in stats.items())

