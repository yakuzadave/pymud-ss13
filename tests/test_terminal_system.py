import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import world
from world import World, GameObject
from components.terminal import TerminalComponent
from systems import get_terminal_system, get_power_system, get_cargo_system
from systems.power import PowerGrid


def setup(tmp_path):
    old_world = world.WORLD
    world.WORLD = World(data_dir=str(tmp_path))
    return old_world


def teardown(old_world):
    world.WORLD = old_world
    get_terminal_system().terminals.clear()


def test_engineering_terminal(tmp_path):
    old = setup(tmp_path)
    try:
        ps = get_power_system()
        ps.grids.clear()
        ps.register_grid(PowerGrid("g1", "Alpha"))

        obj = GameObject(id="term1", name="Eng Terminal", description="")
        obj.add_component("terminal", TerminalComponent("engineering"))
        world.get_world().register(obj)

        out = get_terminal_system().execute("term1", "power")
        assert "g1" in out
    finally:
        teardown(old)


def test_cargo_terminal(tmp_path):
    old = setup(tmp_path)
    try:
        cargo = get_cargo_system()
        cargo.department_credits.clear()
        cargo.set_credits("science", 20)

        obj = GameObject(id="term2", name="Cargo Terminal", description="")
        obj.add_component("terminal", TerminalComponent("cargo"))
        world.get_world().register(obj)

        out = get_terminal_system().execute("term2", "budgets")
        assert "science" in out
    finally:
        teardown(old)
