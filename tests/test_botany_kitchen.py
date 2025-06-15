import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import logging
import world
from world import World, GameObject
from components.player import PlayerComponent
from components.item import ItemComponent
from systems.botany import BotanySystem
from systems.kitchen import KitchenSystem


def test_botany_growth():
    system = BotanySystem(growth_rate=1.0, tick_interval=0)
    plant = system.plant_seed("tomato")
    plant.production_time = 1
    system.start()
    system.update()
    assert plant.growth >= 1.0


def test_kitchen_cooking(tmp_path):
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
            "player", PlayerComponent(role="chef", inventory=["bun", "patty"])
        )
        world.WORLD.register(player)
        system = KitchenSystem(recipe_file="")
        system.register_recipe("burger", ["bun", "patty"], nutrition=25)
        msg = system.cook("test", ["bun", "patty"])
        assert "burger" in msg
        comp = player.get_component("player")
        assert any(itm.startswith("burger") for itm in comp.inventory)
    finally:
        world.WORLD = old_world


def test_botany_logging(tmp_path, caplog):
    system = BotanySystem(growth_rate=1.0, tick_interval=0)
    with caplog.at_level(logging.DEBUG):
        plant = system.plant_seed("tomato")
        plant.production_time = 1
        system.start()
        system.update()
        system.harvest(plant.plant_id)
    log_file = tmp_path / "botany.log"
    with log_file.open("w") as f:
        for record in caplog.records:
            f.write(record.getMessage() + "\n")
    assert any("Planted" in r.getMessage() for r in caplog.records)
    assert any("Harvested" in r.getMessage() for r in caplog.records)


def test_kitchen_logging(tmp_path, caplog):
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
            "player", PlayerComponent(role="chef", inventory=["bun", "patty"])
        )
        world.WORLD.register(player)
        system = KitchenSystem(recipe_file="")
        with caplog.at_level(logging.DEBUG):
            system.register_recipe("burger", ["bun", "patty"], nutrition=25)
            system.cook("test", ["bun", "patty"])
        log_file = tmp_path / "kitchen.log"
        with log_file.open("w") as f:
            for record in caplog.records:
                f.write(record.getMessage() + "\n")
        assert any("Registered recipe" in r.getMessage() for r in caplog.records)
    finally:
        world.WORLD = old_world
