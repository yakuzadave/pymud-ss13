import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from systems.power import PowerSystem, PowerGrid, get_power_system
import components.power_consumer as pc
from components.power_consumer import PowerConsumerComponent
from world import GameObject


def test_consumer_reacts_to_power_events(monkeypatch):
    ps = PowerSystem(tick_interval=0)
    monkeypatch.setattr(pc, "get_power_system", lambda: ps)
    grid = PowerGrid("g1", "Test Grid")
    grid.add_room("room1")
    ps.register_grid(grid)
    ps.register_generator("gen1", "g1", capacity=50)

    obj = GameObject(id="device", name="Device", description="", location="room1")
    comp = PowerConsumerComponent(grid_id="g1", power_usage=10)
    obj.add_component("power_consumer", comp)

    ps.start()
    ps.update()
    assert comp.active is True

    ps.cause_power_failure("g1")
    assert comp.active is False

    grid.power_on()
    assert comp.active is True


def test_smes_discharges_when_needed(monkeypatch):
    ps = PowerSystem(tick_interval=0)
    monkeypatch.setattr(pc, "get_power_system", lambda: ps)
    grid = PowerGrid("g2", "Grid")
    grid.add_room("room2")
    ps.register_grid(grid)
    ps.register_smes("s1", "g2", capacity=100, charge=50, output_rate=50)

    obj = GameObject(id="machine", name="Machine", description="", location="room2")
    comp = PowerConsumerComponent(grid_id="g2", power_usage=30)
    obj.add_component("power_consumer", comp)

    ps.start()
    ps.update()

    assert grid.is_powered is True
    assert ps.smes_units["s1"]["charge"] < 50
