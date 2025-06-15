"""Simple kitchen and cooking mechanics."""

from __future__ import annotations

import logging
from typing import Dict, List

from events import publish

logger = logging.getLogger(__name__)


class KitchenSystem:
    """Handle meal preparation using basic recipes."""

    def __init__(self) -> None:
        self.recipes: Dict[str, List[str]] = {}
        # Example recipe loaded by default
        self.register_recipe("burger", ["bun", "patty"])

    def register_recipe(self, output: str, inputs: List[str]) -> None:
        self.recipes[output] = inputs
        logger.debug("Registered recipe for %s", output)

    def cook(self, ingredients: List[str]) -> str | None:
        for meal, reqs in self.recipes.items():
            if sorted(reqs) == sorted(ingredients):
                publish("meal_cooked", meal=meal)
                return meal
        return None


KITCHEN_SYSTEM = KitchenSystem()


def get_kitchen_system() -> KitchenSystem:
    return KITCHEN_SYSTEM
