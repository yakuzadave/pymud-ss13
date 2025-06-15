import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from systems.robotics import (  # noqa: E402
    RoboticsSystem,
    RobotChassis,
    RobotModule,
    DockingStation,
)


def test_build_and_power_usage():
    system = RoboticsSystem()
    system.add_parts("frame", 1)
    system.add_parts("wires", 5)
    system.define_recipe("basic", {"frame": 1, "wires": 5})
    chassis = RobotChassis("basic", "Basic Frame", slots=2, power_capacity=10)
    borg = system.build_cyborg("borg1", chassis)
    assert borg is not None
    tool = RobotModule("welder", "Welder", power_usage=2)
    assert borg.install_module(tool)
    borg.tick()
    assert borg.power == 8


def test_missing_parts_block_build():
    system = RoboticsSystem()
    system.define_recipe("basic", {"frame": 1})
    chassis = RobotChassis("basic", "Basic Frame")
    borg = system.build_cyborg("borg1", chassis)
    assert borg is None


def test_auto_docking_recharges_unit():
    system = RoboticsSystem()
    system.add_parts("frame", 1)
    system.add_parts("wires", 5)
    system.define_recipe("basic", {"frame": 1, "wires": 5})
    station = DockingStation("dock1", location="robotics", recharge_rate=5)
    system.add_docking_station(station)
    chassis = RobotChassis("basic", "Basic Frame", power_capacity=10)
    borg = system.build_cyborg("borg1", chassis)
    assert borg is not None
    borg.power = 2
    system.tick()  # should move to dock and recharge
    assert borg.docked_at == "dock1"
    assert borg.power == 7
    system.tick()
    assert borg.power == 10
