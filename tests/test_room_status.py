import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import world
from world import GameObject
from components.room import RoomComponent
from systems.power import PowerSystem, PowerGrid
from systems.atmos import AtmosphericSystem


def test_room_status_descriptions(monkeypatch):
    # Setup world with a single room
    w = world.get_world()
    w.objects.clear()
    w.rooms.clear()
    room = GameObject(id="r1", name="Room", description="")
    room.add_component("room", RoomComponent())
    w.register(room)

    # Power system
    ps = PowerSystem(tick_interval=0)
    grid = PowerGrid("g1", "Grid")
    grid.add_room("r1")
    ps.register_grid(grid)
    ps.start()
    ps.update()

    desc = ps.describe_room_power("r1")
    assert "power" in desc.lower()

    # Atmos system
    atmos = AtmosphericSystem(tick_interval=0)
    atmos.start()
    atmos.update()

    assert "nominal" in atmos.describe_room_hazards("r1").lower()
