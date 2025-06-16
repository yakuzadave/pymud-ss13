import pytest
yaml = pytest.importorskip("yaml")
import world
from world import GameObject, World
from components.player import PlayerComponent
from systems.chemistry import ChemistrySystem, get_chemistry_system
from commands.chemist import mix_handler


def test_load_recipes(tmp_path):
    data = [{"output": "chemical_ab", "inputs": ["chemical_a", "chemical_b"]}]
    recipe_file = tmp_path / "recipes.yaml"
    with open(recipe_file, "w") as f:
        yaml.safe_dump(data, f)
    system = ChemistrySystem(str(recipe_file))
    count = system.load_recipes()
    assert count == 1
    assert "chemical_ab" in system.recipes


def test_mix_handler(tmp_path):
    old_world = world.WORLD
    world.WORLD = World(data_dir=str(tmp_path))
    try:
        items = [
            "chemical_a",
            "chemical_b",
            "chemical_ab",
            "beaker",
            "science_id_card",
        ]
        for item_id in items:
            world.WORLD.register(GameObject(id=item_id, name=item_id, description=""))
        player = GameObject(id="player_test", name="Tester", description="")
        player.add_component(
            "player",
            PlayerComponent(
                role="chemist",
                inventory=["chemical_a", "chemical_b"],
            ),
        )
        world.WORLD.register(player)
        system = get_chemistry_system()
        system.recipes = {
            "chemical_ab": {
                "output": "chemical_ab",
                "inputs": ["chemical_a", "chemical_b"],
            }
        }
        out = mix_handler("test", "chemical_a", "chemical_b")
        assert "chemical_ab" in out
    finally:
        world.WORLD = old_world
