import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import world
from world import World, GameObject
from mudpy_interface import MudpyInterface
from components.item import ItemComponent
import integration


def test_take_and_drop_sync(tmp_path):
    old_world = world.WORLD
    world.WORLD = World(data_dir=str(tmp_path))
    try:
        interface = MudpyInterface()
        integ = integration.MudpyIntegration(interface)
        integ._on_client_connected("1")
        player_obj = world.WORLD.get_object("player_1")
        pc = player_obj.get_component("player")

        item = GameObject(id="tool", name="Tool", description="", location="start")
        item.add_component("item", ItemComponent(is_takeable=True))
        world.WORLD.register(item)

        interface.world["items"]["tool"] = {"name": "Tool", "description": ""}
        interface.world["rooms"].setdefault("start", {"name": "Start", "description": "", "exits": {}})
        interface.world["rooms"]["start"].setdefault("items", []).append("tool")
        interface.player_locations["1"] = "start"
        interface.player_inventories["1"] = []

        resp = interface._take("1", "tool")
        assert "take" in resp
        assert "tool" in pc.inventory
        assert item.location is None
        assert "tool" in interface.player_inventories["1"]

        resp = interface._drop("1", "tool")
        assert "drop" in resp
        assert "tool" not in pc.inventory
        assert item.location == "start"
        assert "tool" not in interface.player_inventories["1"]
    finally:
        world.WORLD = old_world

