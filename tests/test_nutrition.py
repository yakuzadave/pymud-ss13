import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import world
from world import GameObject, World
from components.player import PlayerComponent
from components.item import ItemComponent


def test_food_consumption_and_digest(tmp_path):
    w = World(data_dir=str(tmp_path))
    world.WORLD = w
    player_obj = GameObject(id="p1", name="p1", description="p1")
    comp = PlayerComponent(stats={"nutrition": 50})
    player_obj.add_component("player", comp)
    w.register(player_obj)

    apple = GameObject(id="apple1", name="apple", description="juicy")
    apple.add_component(
        "item",
        ItemComponent(
            is_takeable=True,
            is_usable=True,
            item_type="food",
            item_properties={"nutrition": 25},
        ),
    )
    w.register(apple)

    apple.get_component("item").use("p1")
    assert comp.stats["nutrition"] > 50

    comp.digest(10)
    assert comp.stats["nutrition"] < 75
