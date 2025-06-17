import os
import sys
from unittest import mock

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from systems.space_exploration import (
    SpaceExplorationSystem,
    EnvironmentalHazard,
    Shuttle,
)


def test_eva_suit_degradation(monkeypatch):
    system = SpaceExplorationSystem()
    shuttle = Shuttle("s1", "Test")
    system.register_shuttle(shuttle)
    hazard = EnvironmentalHazard("radiation pocket", chance=1.0, severity=2)
    system.create_site("site1", "Danger", hazards=[hazard], resources={})

    mock_pub = mock.Mock()
    monkeypatch.setattr("events.publish", mock_pub)

    mission = system.start_mission("m1", "s1", "site1", ["p1"])
    assert mission is not None
    mission.tick()

    suit = mission.suits["p1"]
    assert suit.integrity < 100


def test_resource_return(monkeypatch):
    system = SpaceExplorationSystem()
    shuttle = Shuttle("s2", "Hauler")
    system.register_shuttle(shuttle)
    system.create_site("site2", "Mine", hazards=[], resources={"ore": 3})

    mock_pub = mock.Mock()
    monkeypatch.setattr("events.publish", mock_pub)

    mission = system.start_mission("m2", "s2", "site2", ["c1"])
    assert mission is not None
    harvested = mission.harvest("ore", 2)
    assert harvested == 2
    system.complete_mission("m2")

    assert system.station_resources.get("ore") == 2


def test_resource_spawn(monkeypatch):
    system = SpaceExplorationSystem()
    shuttle = Shuttle("s3", "Rover")
    system.register_shuttle(shuttle)
    system.create_site(
        "site3",
        "Ice Field",
        hazards=[],
        resources={},
    )

    mock_pub = mock.Mock()
    monkeypatch.setattr("events.publish", mock_pub)

    mission = system.start_mission("m3", "s3", "site3", ["p2"])
    assert mission is not None

    # Force resource spawn by setting chance high
    mission.site.resource_chance = 1.0
    system.tick()

    assert mission.site.resources != {}


def test_new_hazards_affect_crew(monkeypatch):
    system = SpaceExplorationSystem()
    shuttle = Shuttle("s4", "Explorer")
    system.register_shuttle(shuttle)
    rad = EnvironmentalHazard("radiation storm", chance=1.0, severity=3)
    breach = EnvironmentalHazard("hull breach", chance=1.0, severity=4)
    system.create_site("site4", "Hazards", hazards=[rad, breach], resources={})

    mock_pub = mock.Mock()
    monkeypatch.setattr("events.publish", mock_pub)

    mission = system.start_mission("m4", "s4", "site4", ["c1"])
    assert mission is not None
    mission.tick()

    status = mission.crew_status["c1"]
    assert status.radiation > 0
    assert status.oxygen_used > 1
    assert mission.suits["c1"].oxygen < 100


def test_cargo_integration(monkeypatch):
    from systems.cargo import CargoSystem, SupplyVendor, get_cargo_system
    import systems.cargo as cargo_mod

    old_cargo = get_cargo_system()
    cargo_mod.CARGO_SYSTEM = CargoSystem()
    cargo_mod.CARGO_SYSTEM.register_vendor(SupplyVendor("central", {"ore": 5}))

    system = SpaceExplorationSystem()
    shuttle = Shuttle("s5", "Hauler")
    system.register_shuttle(shuttle)
    system.create_site("site5", "Mine", hazards=[], resources={"ore": 4})

    mission = system.start_mission("m5", "s5", "site5", ["c2"])
    assert mission is not None
    mission.harvest("ore", 3)
    system.complete_mission("m5")

    assert system.station_resources.get("ore") == 3
    inv = cargo_mod.CARGO_SYSTEM.get_inventory("mining")
    assert inv.get("ore") == 3

    cargo_mod.CARGO_SYSTEM = old_cargo
