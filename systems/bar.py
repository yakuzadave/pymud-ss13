"""Basic bartender drink mixing system."""

from __future__ import annotations

import logging
import os
from typing import Dict, List, Any

import yaml
import world
from components.item import ItemComponent
from events import publish

logger = logging.getLogger(__name__)


class BarSystem:
    """Handle drink preparation using recipes."""

    def __init__(self, recipe_file: str = "data/drink_recipes.yaml") -> None:
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
            if out and inputs:
                self.register_recipe(out, inputs)
        logger.info("Loaded %d drink recipes", len(self.recipes))
        return len(self.recipes)

    def register_recipe(self, output: str, inputs: List[str]) -> None:
        self.recipes[output] = {"inputs": inputs}
        logger.debug("Registered recipe for %s", output)

    def mix(self, player_id: str, ingredients: List[str]) -> str:
        """Attempt to mix a drink using player's inventory."""
        world_instance = world.get_world()
        player = world_instance.get_object(f"player_{player_id}")
        if not player:
            return "Player not found."
        comp = player.get_component("player")
        if not comp:
            return "Player component missing."

        for drink, rec in self.recipes.items():
            if sorted(rec["inputs"]) == sorted(ingredients):
                for itm in rec["inputs"]:
                    if not comp.has_item(itm):
                        return "You lack some ingredients."
                for itm in rec["inputs"]:
                    comp.remove_from_inventory(itm)
                    obj = world_instance.get_object(itm)
                    if obj:
                        obj.location = None
                drink_id = f"{drink}_{self.counter}"
                self.counter += 1
                obj = world.GameObject(
                    id=drink_id,
                    name=drink.replace("_", " ").title(),
                    description=f"a {drink.replace('_', ' ')}",
                )
                obj.add_component(
                    "item",
                    ItemComponent(
                        is_takeable=True,
                        is_usable=True,
                        item_type="drink",
                        use_effect=f"You drink the {drink.replace('_', ' ')}.",
                        item_properties={"nutrition": 1},
                    ),
                )
                world_instance.register(obj)
                comp.add_to_inventory(drink_id)
                publish("drink_mixed", drink=drink, player_id=player_id)
                return f"You mix a {drink.replace('_', ' ')}."
        return "No known recipe for those ingredients."


BAR_SYSTEM = BarSystem()


def get_bar_system() -> BarSystem:
    return BAR_SYSTEM
