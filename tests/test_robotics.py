import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from systems.robotics import RoboticsSystem, RobotChassis, RobotModule


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
