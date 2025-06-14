from components.structure import StructureComponent
from world import GameObject, get_world
from systems.physics import get_physics_system


def test_environment_damage():
    world = get_world()
    wall = GameObject(id="w1", name="Wall", description="")
    comp = StructureComponent(kind="wall", integrity=100, material="glass")
    wall.add_component("structure", comp)
    world.register(wall)

    get_physics_system().apply_environment("w1", pressure=80.0, temperature=600.0)
    assert comp.integrity < 100
