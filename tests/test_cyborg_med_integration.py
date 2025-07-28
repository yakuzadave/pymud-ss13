import world
from world import World, GameObject
from components.player import PlayerComponent
from systems.robotics import RoboticsSystem, RobotChassis, SpecializedRobotModule
from systems.genetics import get_genetics_system


def test_cyborg_heals_with_genetics(tmp_path):
    old_world = world.WORLD
    world.WORLD = World(data_dir=str(tmp_path))
    try:
        robo = RoboticsSystem()
        robo.add_parts("frame", 1)
        robo.add_parts("wires", 5)
        robo.define_recipe("basic", {"frame": 1, "wires": 5})
        chassis = RobotChassis("basic", "Basic")
        unit = robo.build_cyborg("borg1", chassis)
        unit.install_module(SpecializedRobotModule("med", "Med Probe", functionality="heal", power_usage=0))

        player = GameObject(id="p1", name="Pat", description="")
        comp = PlayerComponent()
        player.add_component("player", comp)
        world.WORLD.register(player)

        genetics = get_genetics_system()
        genetics.profiles.clear()
        genetics.scanned_dna.clear()
        genetics.mutate_player("p1", "regeneration")

        comp.apply_damage("torso", "brute", 20)
        robo.heal_player("borg1", "p1", amount=10)
        assert comp.body_parts["torso"]["brute"] == 5
    finally:
        world.WORLD = old_world
