import os
import sys
import pytest
yaml = pytest.importorskip("yaml")
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import world
from world import GameObject, World
from components.player import PlayerComponent
from systems.chemistry import ChemistrySystem, get_chemistry_system
from commands.chemist import mix_handler, dispense_handler, transfer_handler, react_handler
from systems.advanced_chemistry import ReactionStep, ReactionChain
from systems.chemical_reactions import ChemicalContainerComponent
from pathlib import Path


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


def test_reaction_chain_from_yaml():
    path = Path(__file__).resolve().parents[1] / "data" / "chemistry_recipes.yaml"
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    rec = next(r for r in data if r.get("output") == "stimulant")
    steps = [ReactionStep(**s) for s in rec["chain"]]
    chain = ReactionChain(steps=steps)
    container = ChemicalContainerComponent(capacity=5)
    available = {"chemical_a": 1, "chemical_b": 2}
    produced = chain.process(available, container)
    assert "stimulant" in produced


def test_equipment_usage(tmp_path):
    old_world = world.WORLD
    world.WORLD = World(data_dir=str(tmp_path))
    try:
        player = GameObject(id="player_test", name="Tester", description="")
        player.add_component("player", PlayerComponent(role="chemist"))
        world.WORLD.register(player)

        beaker = GameObject(id="beaker", name="Beaker", description="")
        beaker.add_component("chemical_container", ChemicalContainerComponent(capacity=10))
        world.WORLD.register(beaker)

        dispenser = GameObject(id="chemical_dispenser", name="Disp", description="")
        dcomp = ChemicalContainerComponent(capacity=20)
        dcomp.add_reagent("chemical_a", 1)
        dcomp.add_reagent("chemical_b", 2)
        dispenser.add_component("chemical_container", dcomp)
        world.WORLD.register(dispenser)

        chamber = GameObject(id="reaction_chamber", name="Chamber", description="")
        chamber.add_component("chemical_container", ChemicalContainerComponent(capacity=20))
        world.WORLD.register(chamber)

        dispense_handler("test", reagent="chemical_a", target="beaker")
        dispense_handler("test", reagent="chemical_b", target="beaker")
        dispense_handler("test", reagent="chemical_b", target="beaker")

        transfer_handler("test", source="beaker", dest="reaction_chamber")

        chain = ReactionChain([
            ReactionStep(inputs=["chemical_a", "chemical_b"], output="base_med"),
            ReactionStep(inputs=["base_med", "chemical_b"], output="stimulant"),
        ])
        msg = react_handler("test", chain=chain)
        assert "stimulant" in msg
    finally:
        world.WORLD = old_world
