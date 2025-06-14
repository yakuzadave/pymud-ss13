import os
import yaml
import logging
from typing import Dict, List, Any

from events import publish
import world

logger = logging.getLogger(__name__)


class ChemistrySystem:
    """Simple chemistry crafting system."""

    def __init__(self, recipe_file: str = "data/chemistry_recipes.yaml"):
        self.recipes: Dict[str, Dict[str, Any]] = {}
        self.recipe_file = recipe_file

    def load_recipes(self) -> int:
        """Load chemistry recipes from YAML."""
        if not os.path.exists(self.recipe_file):
            logger.warning(f"Recipe file not found: {self.recipe_file}")
            return 0
        with open(self.recipe_file, "r") as f:
            data = yaml.safe_load(f) or []
        count = 0
        for recipe in data:
            output = recipe.get("output")
            inputs = recipe.get("inputs", [])
            if not output or not inputs:
                continue
            self.recipes[output] = {"output": output, "inputs": inputs}
            count += 1
        logger.info(f"Loaded {count} chemistry recipes")
        return count

    def register_recipe(self, output: str, inputs: List[str]) -> None:
        """Register a new recipe at runtime."""
        self.recipes[output] = {"output": output, "inputs": inputs}

    def craft(self, player_id: str, inputs: List[str]) -> str:
        """Attempt to craft using the provided inputs."""
        world_instance = world.get_world()
        player = world_instance.get_object(f"player_{player_id}")
        if not player:
            return "Player not found."
        comp = player.get_component("player")
        if not comp:
            return "Player component missing."

        for recipe in self.recipes.values():
            if sorted(recipe["inputs"]) == sorted(inputs):
                # Check inventory
                for item_id in recipe["inputs"]:
                    if not comp.has_item(item_id):
                        return "You lack some of the required chemicals."
                # Remove inputs
                for item_id in recipe["inputs"]:
                    comp.remove_from_inventory(item_id)
                # Add output if defined in world
                output_id = recipe["output"]
                if world_instance.get_object(output_id):
                    comp.add_to_inventory(output_id)
                publish(
                    "chemical_synthesized",
                    player_id=player_id,
                    output=output_id,
                )
                return f"You synthesize {output_id}."
        return "No known recipe for that combination."


CHEMISTRY_SYSTEM = ChemistrySystem()
CHEMISTRY_SYSTEM.load_recipes()


def get_chemistry_system() -> ChemistrySystem:
    return CHEMISTRY_SYSTEM
