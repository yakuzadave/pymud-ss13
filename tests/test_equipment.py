import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from engine import MudEngine, action_queue
from mudpy_interface import MudpyInterface
from world import get_world, GameObject
from components.item import ItemComponent
import time


def setup_engine(tmp_path):
    cfg = tmp_path / "config.yaml"
    interface = MudpyInterface(
        config_file=str(cfg), alias_dir=str(tmp_path / "aliases")
    )
    engine = MudEngine(interface)
    interface.connect_client("1")
    return interface, engine


def test_equip_and_remove(tmp_path):
    interface, engine = setup_engine(tmp_path)
    action_queue.next_time.clear()
    world = get_world()
    player = world.get_object("player_1")
    if player is None:
        from components.player import PlayerComponent

        player = GameObject(id="player_1", name="Player", description="")
        player.add_component("player", PlayerComponent())
        world.register(player)
    item_obj = GameObject(id="helmet1", name="Helmet", description="")
    item_obj.add_component("item", ItemComponent(item_properties={"slot": "head"}))
    world.register(item_obj)
    player_comp = player.get_component("player")
    player_comp.add_to_inventory("helmet1")
    interface.player_inventories["1"].append("helmet1")

    out = engine.process_command("1", "wear helmet1")
    assert "equip" in out
    assert player_comp.equipment.get("head") == "helmet1"

    time.sleep(0.6)
    out = engine.process_command("1", "remove helmet1")
    assert "remove" in out
    assert "helmet1" in interface.player_inventories["1"]
