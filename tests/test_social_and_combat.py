import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import world
from world import GameObject
from components.player import PlayerComponent
from components.item import ItemComponent
from engine import MudEngine
from mudpy_interface import MudpyInterface



def setup_engine(tmp_path):
    cfg = tmp_path / "config.yaml"
    interface = MudpyInterface(config_file=str(cfg), alias_dir=str(tmp_path / "aliases"))
    engine = MudEngine(interface)
    interface.connect_client("1")
    return interface, engine


def setup_world_player():
    w = world.get_world()
    obj = GameObject(id="player_1", name="Tester", description="")
    obj.add_component("player", PlayerComponent())
    w.register(obj)
    return obj


def teardown_world():
    w = world.get_world()
    w.objects.clear()
    w.rooms.clear()
    w.items.clear()
    w.npcs.clear()


def test_emote_command(tmp_path):
    interface, engine = setup_engine(tmp_path)
    setup_world_player()
    out = engine.process_command("1", "emote waves happily")
    assert "waves happily" in out
    teardown_world()


def test_wave_command(tmp_path):
    interface, engine = setup_engine(tmp_path)
    setup_world_player()
    out = engine.process_command("1", "wave")
    assert "wave" in out.lower()
    teardown_world()


def test_attack_command(tmp_path):
    interface, engine = setup_engine(tmp_path)
    player = setup_world_player()
    target = GameObject(id="player_target", name="Target", description="")
    target.add_component("player", PlayerComponent())
    world.get_world().register(target)
    out = engine.process_command("1", "attack player_target")
    assert "attack" in out
    teardown_world()


def test_throw_command(tmp_path):
    interface, engine = setup_engine(tmp_path)
    player = setup_world_player()
    rock = GameObject(id="rock", name="Rock", description="")
    rock.add_component("item", ItemComponent())
    world.get_world().register(rock)
    pc = player.get_component("player")
    pc.add_to_inventory("rock")
    target = GameObject(id="player_target", name="Target", description="")
    target.add_component("player", PlayerComponent())
    world.get_world().register(target)
    out = engine.process_command("1", "throw rock at player_target")
    assert "throw" in out
    teardown_world()

