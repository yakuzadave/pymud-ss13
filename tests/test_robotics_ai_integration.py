import world
from world import World
from systems.robotics import RoboticsSystem, RobotChassis
from systems.ai import get_ai_law_system


def test_robotics_respects_ai_laws(tmp_path):
    old_world = world.WORLD
    world.WORLD = World(data_dir=str(tmp_path))
    try:
        robo = RoboticsSystem()
        robo.add_parts("frame", 1)
        robo.add_parts("wires", 5)
        robo.define_recipe("basic", {"frame": 1, "wires": 5})
        chassis = RobotChassis("basic", "Basic Frame")
        robo.build_cyborg("borg1", chassis)

        laws = get_ai_law_system()
        laws.clear()
        laws.add_law(1, "Never harm a human")

        allowed = robo.remote_command("borg1", "harm human")
        assert not allowed
    finally:
        world.WORLD = old_world
