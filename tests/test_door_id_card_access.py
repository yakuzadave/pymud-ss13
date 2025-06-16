import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import world
from world import World, GameObject
from components.player import PlayerComponent
from components.item import ItemComponent
from components.door import DoorComponent
from components.id_card import IDCardComponent


def setup_world(tmp_path):
    old = world.WORLD
    world.WORLD = World(data_dir=str(tmp_path))
    return old


def teardown_world(old):
    world.WORLD = old


def test_door_opens_with_id_card(tmp_path):
    old = setup_world(tmp_path)
    try:
        w = world.WORLD
        card = GameObject(id="card1", name="Card", description="")
        card.add_component("item", ItemComponent(item_type="id_card"))
        card.add_component("id_card", IDCardComponent(access_level=30))
        w.register(card)

        player = GameObject(id="player1", name="Tester", description="")
        player.add_component("player", PlayerComponent(inventory=["card1"]))
        w.register(player)

        door_obj = GameObject(id="door1", name="Door", description="")
        door = DoorComponent(is_open=False, is_locked=True, access_level=20)
        door_obj.add_component("door", door)
        msg = door.open(player.id)
        assert door.is_open
        assert "open" in msg.lower()
    finally:
        teardown_world(old)


def test_door_denies_without_access(tmp_path):
    old = setup_world(tmp_path)
    try:
        w = world.WORLD
        card = GameObject(id="card2", name="Card2", description="")
        card.add_component("item", ItemComponent(item_type="id_card"))
        card.add_component("id_card", IDCardComponent(access_level=10))
        w.register(card)

        player = GameObject(id="player2", name="Tester2", description="")
        player.add_component("player", PlayerComponent(inventory=["card2"]))
        w.register(player)

        door_obj = GameObject(id="door2", name="Door2", description="")
        door = DoorComponent(is_open=False, is_locked=True, access_level=50)
        door_obj.add_component("door", door)
        msg = door.open(player.id)
        assert not door.is_open
        assert "locked" in msg.lower()
    finally:
        teardown_world(old)
