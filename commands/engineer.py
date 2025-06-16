"""Engineer role specific commands."""

from engine import register
from events import publish
import world
from systems import get_power_system, get_atmos_system


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


@register("diagnostics")
def diagnostics_handler(client_id: str, system: str = None, **kwargs):
    """Run engineering diagnostics for the current room."""
    player = world.get_world().get_object(f"player_{client_id}")
    if not player:
        return "Player not found."
    comp = player.get_component("player")
    if not comp or comp.role.lower() != "engineer":
        return "Only engineers can do that."

    interface = kwargs.get("interface")
    location = interface.get_player_location(client_id) if interface else None
    if not location:
        return "You are nowhere."

    results = []
    if system in (None, "power"):
        results.append(get_power_system().describe_room_power(location))
    if system in (None, "atmos", "atmosphere"):
        results.append(get_atmos_system().describe_room_hazards(location))

    if not results:
        return "Unknown system."
    return " ".join(results)


@register("reroute")
def reroute_handler(client_id: str, room: str = None, grid: str = None, **kwargs):
    """Reroute power for a room to a different grid."""
    player = world.get_world().get_object(f"player_{client_id}")
    if not player:
        return "Player not found."
    comp = player.get_component("player")
    if not comp or comp.role.lower() != "engineer":
        return "Only engineers can do that."
    if not room or not grid:
        return "Specify a room and grid."

    ps = get_power_system()
    target_grid = ps.grids.get(grid)
    if not target_grid:
        return f"Grid '{grid}' not found."

    current_grid = None
    for g in ps.grids.values():
        if room in g.rooms:
            current_grid = g
            break

    if not current_grid:
        return f"Room '{room}' not found on any grid."
    if current_grid.grid_id == grid:
        return f"{room} is already powered by grid {grid}."

    current_grid.remove_room(room)
    target_grid.add_room(room)
    return f"Rerouted power for {room} to grid {grid}."


@register("seal")
def seal_handler(client_id: str, room: str = None, **kwargs):
    """Seal a hull breach in the specified or current room."""
    player = world.get_world().get_object(f"player_{client_id}")
    if not player:
        return "Player not found."
    comp = player.get_component("player")
    if not comp or comp.role.lower() != "engineer":
        return "Only engineers can do that."

    interface = kwargs.get("interface")
    if not room and interface:
        room = interface.get_player_location(client_id)
    if not room:
        return "Specify a room to seal."

    atmos = get_atmos_system()
    if atmos.fix_leak(room):
        return f"Breach in {room} sealed."
    return f"No breach found in {room}."
