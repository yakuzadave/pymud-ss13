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

