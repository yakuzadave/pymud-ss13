from components.structure import StructureComponent
from world import GameObject


def test_structure_damage_and_repair():
    wall = GameObject(id="wall1", name="Wall", description="")
    struct = StructureComponent(kind="wall", integrity=100)
    wall.add_component("structure", struct)

    destroyed = struct.damage(50)
    assert destroyed is False
    assert struct.integrity == 50

    destroyed = struct.damage(60)
    assert destroyed is True
    assert struct.integrity == 0

    struct.repair(30)
    assert struct.integrity == 30
