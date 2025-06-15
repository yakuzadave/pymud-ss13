"""Simple kitchen and cooking mechanics with recipe support."""

from __future__ import annotations

import logging
from typing import Dict, List, Any

import os
import yaml
import world
from components.item import ItemComponent

from events import publish

logger = logging.getLogger(__name__)


class KitchenSystem:
    """Handle meal preparation using basic recipes."""

    def __init__(self, recipe_file: str = "data/food_recipes.yaml") -> None:
        self.recipes: Dict[str, Dict[str, Any]] = {}
        self.recipe_file = recipe_file
        self.counter = 1
        self.load_recipes()

    def load_recipes(self) -> int:
        """Load recipes from YAML."""
        if not os.path.exists(self.recipe_file):
            logger.warning("Recipe file not found: %s", self.recipe_file)
            return 0
        with open(self.recipe_file, "r") as f:
            data = yaml.safe_load(f) or []
        for rec in data:
            out = rec.get("output")
            inputs = rec.get("inputs", [])
            nutrition = rec.get("nutrition", 10)
            if out and inputs:
                self.register_recipe(out, inputs, nutrition)
        logger.info("Loaded %d kitchen recipes", len(self.recipes))
        return len(self.recipes)

    def register_recipe(self, output: str, inputs: List[str], nutrition: int = 10) -> None:
        self.recipes[output] = {"inputs": inputs, "nutrition": nutrition}
        logger.debug("Registered recipe for %s", output)

    def cook(self, player_id: str, ingredients: List[str]) -> str:
        """Attempt to cook using player's inventory."""
        world_instance = world.get_world()
        player = world_instance.get_object(f"player_{player_id}")
        if not player:
            return "Player not found."
        comp = player.get_component("player")
        if not comp:
            return "Player component missing."

        for meal, rec in self.recipes.items():
            if sorted(rec["inputs"]) == sorted(ingredients):
                for itm in rec["inputs"]:
                    if not comp.has_item(itm):
                        return "You lack some ingredients."
                for itm in rec["inputs"]:
                    comp.remove_from_inventory(itm)
                    obj = world_instance.get_object(itm)
                    if obj:
                        obj.location = None
                meal_id = f"{meal}_{self.counter}"
                self.counter += 1
                obj = world.GameObject(id=meal_id, name=meal, description=f"a {meal}")
                obj.add_component(
                    "item",
                    ItemComponent(
                        is_takeable=True,
                        is_usable=True,
                        item_type="food",
                        item_properties={"nutrition": rec["nutrition"]},
                    ),
                )
                world_instance.register(obj)
                comp.add_to_inventory(meal_id)
                publish("meal_cooked", meal=meal, player_id=player_id)
                return f"You cook a {meal}."
        return "No known recipe for those ingredients."


KITCHEN_SYSTEM = KitchenSystem()


def get_kitchen_system() -> KitchenSystem:
    return KITCHEN_SYSTEM
