import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import world
from world import World, GameObject
from components.player import PlayerComponent
from components.item import ItemComponent
from systems.bar import BarSystem
from commands.bartender import mixdrink_handler


def test_mixdrink_creates_item(tmp_path):
    old_world = world.WORLD
    world.WORLD = World(data_dir=str(tmp_path))
    try:
        rum = GameObject(id="rum", name="rum", description="")
        rum.add_component(
            "item", ItemComponent(is_takeable=True, is_usable=True, item_type="drink")
        )
        cola = GameObject(id="cola", name="cola", description="")
        cola.add_component(
            "item", ItemComponent(is_takeable=True, is_usable=True, item_type="drink")
        )
        world.WORLD.register(rum)
        world.WORLD.register(cola)
        player = GameObject(id="player_test", name="Tester", description="")
        player.add_component(
            "player", PlayerComponent(role="bartender", inventory=["rum", "cola"])
        )
        world.WORLD.register(player)
        system = BarSystem(recipe_file="")
        system.register_recipe("cuba_libre", ["cola", "rum"])
        msg = mixdrink_handler("test", "cola", "rum")
        assert "mix" in msg
        comp = player.get_component("player")
        created = next(i for i in comp.inventory if i.startswith("cuba_libre"))
        obj = world.WORLD.get_object(created)
        assert obj is not None
    finally:
        world.WORLD = old_world
