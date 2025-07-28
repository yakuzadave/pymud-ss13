import world
from world import World
from systems.robotics import RoboticsSystem, RobotChassis, SpecializedRobotModule


def test_cyborg_requires_maintenance(tmp_path):
    old_world = world.WORLD
    world.WORLD = World(data_dir=str(tmp_path))
    try:
        robo = RoboticsSystem()
        robo.add_parts("frame", 1)
        robo.add_parts("wires", 5)
        robo.define_recipe("basic", {"frame": 1, "wires": 5})
        chassis = RobotChassis("basic", "Basic")
        unit = robo.build_cyborg("borg1", chassis)
        unit.install_module(SpecializedRobotModule("mod", "Drill"))

        # accelerate wear
        unit.maintenance.wear_rate = 10.0
        for _ in range(3):
            unit.tick()
        assert unit.maintenance.condition < 100.0

        unit.maintenance.condition = unit.maintenance.failure_threshold - 1
        unit.tick()
        assert not unit.maintenance.is_operational

        robo.repair_unit("borg1")
        assert unit.maintenance.is_operational
        assert unit.maintenance.condition == 100.0
    finally:
        world.WORLD = old_world
