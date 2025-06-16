import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from systems.research import ResearchSystem, ResearchTechnology, Prototype


def setup_system():
    system = ResearchSystem()
    system.register_technology(
        ResearchTechnology(
            tech_id="basic_tools",
            name="Basic Tools",
            points_required=10,
        )
    )
    system.register_technology(
        ResearchTechnology(
            tech_id="advanced_tools",
            name="Advanced Tools",
            prerequisites=["basic_tools"],
            points_required=15,
        )
    )
    system.register_prototype(
        Prototype(
            proto_id="proto_drill",
            name="Power Drill",
            technology="advanced_tools",
            required_materials=["metal", "circuits"],
            required_equipment=["workbench"],
        )
    )
    system.register_technology(
        ResearchTechnology(
            tech_id="device_fab",
            name="Device Fabrication",
            points_required=20,
        )
    )
    system.register_prototype(
        Prototype(
            proto_id="autolathe_blueprint",
            name="Autolathe",
            technology="device_fab",
            required_materials=["metal"],
            required_equipment=["workbench"],
            object_id="autolathe",
        )
    )
    system.register_prototype(
        Prototype(
            proto_id="protolathe_blueprint",
            name="Protolathe",
            technology="device_fab",
            required_materials=["glass", "metal"],
            required_equipment=["workbench"],
            object_id="protolathe",
        )
    )
    return system


def test_research_progression():
    system = setup_system()
    system.add_points("science", 10)
    assert system.research("science", "basic_tools")
    system.add_points("science", 15)
    assert system.research("science", "advanced_tools")
    assert system.has_technology("science", "advanced_tools")


def test_transfer_and_prototype():
    system = setup_system()
    system.add_points("science", 25)
    system.research("science", "basic_tools")
    system.research("science", "advanced_tools")
    assert system.transfer_technology("advanced_tools", "science", "engineering")
    assert system.has_technology("engineering", "advanced_tools")
    assert system.build_prototype(
        "engineering",
        "proto_drill",
        ["metal", "circuits"],
        ["workbench"],
    )


def test_lathe_blueprints(tmp_path):
    import world
    from world import World

    old_world = world.WORLD
    world.WORLD = World(data_dir="data")
    try:
        system = setup_system()
        system.add_points("science", 20)
        assert system.research("science", "device_fab")
        assert system.build_prototype(
            "science",
            "autolathe_blueprint",
            ["metal"],
            ["workbench"],
        )
        assert world.WORLD.get_object("autolathe") is not None
        assert system.build_prototype(
            "science",
            "protolathe_blueprint",
            ["glass", "metal"],
            ["workbench"],
        )
        assert world.WORLD.get_object("protolathe") is not None
    finally:
        world.WORLD = old_world
