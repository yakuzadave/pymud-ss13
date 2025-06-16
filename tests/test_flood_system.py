from systems.flood import FloodSystem
from components.player import PlayerComponent
from world import GameObject


def test_flood_affects_player_movement_speed():
    flood = FloodSystem()
    player_obj = GameObject(id="p1", name="p", description="")
    comp = PlayerComponent()
    player_obj.add_component("player", comp)

    flood.add_water("room1", 1.0)
    flood.affect_player(comp, "room1")
    assert comp.move_speed > 1.0

    flood.remove_water("room1", 1.0)
    flood.affect_player(comp, "room1")
    assert comp.move_speed == 1.0
