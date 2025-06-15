import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import world
from world import World, GameObject
from components.player import PlayerComponent
from components.item import ItemComponent
from commands.chef import cook_handler
from systems.kitchen import get_kitchen_system


def test_cook_handler(tmp_path):
    old_world = world.WORLD
    world.WORLD = World(data_dir=str(tmp_path))
    try:
        bun = GameObject(id="bun", name="bun", description="")
        bun.add_component(
            "item", ItemComponent(is_takeable=True, is_usable=False, item_type="food")
        )
        patty = GameObject(id="patty", name="patty", description="")
        patty.add_component(
            "item", ItemComponent(is_takeable=True, is_usable=False, item_type="food")
        )
        world.WORLD.register(bun)
        world.WORLD.register(patty)
        player = GameObject(id="player_test", name="Tester", description="")
        player.add_component(
            "player",
            PlayerComponent(
                role="chef", inventory=["bun", "patty"], stats={"nutrition": 50}
            ),
        )
        world.WORLD.register(player)
        system = get_kitchen_system()
        system.recipes = {"burger": {"inputs": ["bun", "patty"], "nutrition": 25}}
        msg = cook_handler("test", "bun", "patty")
        assert "cook" in msg
        comp = player.get_component("player")
        burger_id = next(i for i in comp.inventory if i.startswith("burger"))
        burger = world.WORLD.get_object(burger_id)
        assert burger is not None
        burger.get_component("item").use("player_test")
        assert comp.stats["nutrition"] > 50
    finally:
        world.WORLD = old_world
