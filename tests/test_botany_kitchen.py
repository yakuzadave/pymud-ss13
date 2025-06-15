import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import logging

from systems.botany import BotanySystem
from systems.kitchen import KitchenSystem


def test_botany_growth():
    system = BotanySystem(growth_rate=1.0, tick_interval=0)
    plant = system.plant_seed("tomato")
    system.start()
    system.update()
    assert plant.growth >= 1.0


def test_kitchen_cooking():
    system = KitchenSystem()
    system.register_recipe("burger", ["bun", "patty"])
    meal = system.cook(["patty", "bun"])
    assert meal == "burger"


def test_botany_logging(tmp_path, caplog):
    system = BotanySystem(growth_rate=1.0, tick_interval=0)
    with caplog.at_level(logging.DEBUG):
        plant = system.plant_seed("tomato")
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
    system = KitchenSystem()
    with caplog.at_level(logging.DEBUG):
        system.register_recipe("burger", ["bun", "patty"])
        system.cook(["bun", "patty"])
    log_file = tmp_path / "kitchen.log"
    with log_file.open("w") as f:
        for record in caplog.records:
            f.write(record.getMessage() + "\n")
    assert any("Registered recipe" in r.getMessage() for r in caplog.records)

