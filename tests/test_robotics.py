import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from systems.robotics import (  # noqa: E402
    RoboticsSystem,
    RobotChassis,
    RobotModule,
    SpecializedRobotModule,
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


def test_remote_control_module():
    system = RoboticsSystem()
    system.add_parts("frame", 1)
    system.add_parts("wires", 5)
    system.define_recipe("basic", {"frame": 1, "wires": 5})
    chassis = RobotChassis("basic", "Basic Frame", power_capacity=10)
    borg = system.build_cyborg("borg1", chassis)
    assert borg is not None
    tool = RobotModule(
        "flashlight",
        "Flashlight",
        power_usage=1,
        remote_control=True,
    )
    borg.install_module(tool)
    # turn off via remote so no power used
    assert system.remote_control("borg1", "flashlight", False)
    borg.tick()
    assert borg.power == 10
    # reactivate and ensure usage
    assert system.remote_control("borg1", "flashlight", True)
    borg.tick()
    assert borg.power == 9


def test_remote_unit_commands_and_maintenance():
    system = RoboticsSystem()
    system.add_parts("frame", 1)
    system.add_parts("wires", 5)
    system.define_recipe("basic", {"frame": 1, "wires": 5})
    chassis = RobotChassis("basic", "Basic Frame", power_capacity=10)
    borg = system.build_cyborg("borg1", chassis)
    assert borg is not None
    borg.power = 5
    assert system.remote_command("borg1", "shutdown")
    assert borg.power == 0
    assert all(not m.active for m in borg.modules)

    # issue diagnostics while offline
    borg.power = 1
    diag = system.remote_command("borg1", "diagnostics")
    assert diag is True
    diag_info = system.diagnose_unit("borg1")
    assert diag_info["power"] == 1

    # restart should restore power and re-enable modules
    assert system.remote_command("borg1", "restart")
    assert borg.power == 10
    assert all(m.active for m in borg.modules)

    # repair acts as an alias for recharge and activation
    borg.power = 5
    assert system.remote_command("borg1", "repair")
    assert borg.power == 10


def test_specialized_robot_module_usage():
    system = RoboticsSystem()
    system.add_parts("frame", 1)
    system.add_parts("wires", 5)
    system.define_recipe("basic", {"frame": 1, "wires": 5})
    chassis = RobotChassis("basic", "Basic Frame", power_capacity=10)
    borg = system.build_cyborg("borg1", chassis)
    assert borg is not None
    med_probe = SpecializedRobotModule(
        "med_probe", "Medical Probe", power_usage=3, functionality="heal"
    )
    borg.install_module(med_probe)
    borg.tick()
    assert borg.power == 7
