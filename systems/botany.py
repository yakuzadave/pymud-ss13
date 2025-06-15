"""Basic botany system for growing plants."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Dict

from events import publish

logger = logging.getLogger(__name__)


@dataclass
class Plant:
    """Plant record with basic stats used for simple hydroponics."""

    plant_id: str
    species: str
    growth: float = 0.0
    planted_at: float = field(default_factory=time.time)
    nutrient: float = 5.0
    health: float = 5.0
    yield_amount: int = 1
    potency: int = 1
    toxicity: float = 0.0
    production_time: float = 10.0


class BotanySystem:
    """Manage hydroponic trays and plant growth."""

    def __init__(self, growth_rate: float = 0.1, tick_interval: float = 10.0) -> None:
        self.growth_rate = growth_rate
        self.tick_interval = tick_interval
        self.last_tick = 0.0
        self.enabled = False
        self.plants: Dict[str, Plant] = {}
        self._counter = 1

    # ------------------------------------------------------------------
    def start(self) -> None:
        self.enabled = True
        self.last_tick = time.time()

    def stop(self) -> None:
        self.enabled = False

    # ------------------------------------------------------------------
    def plant_seed(self, species: str) -> Plant:
        plant_id = f"plant_{self._counter}"
        self._counter += 1
        plant = Plant(plant_id=plant_id, species=species)
        self.plants[plant_id] = plant
        publish("seed_planted", plant_id=plant_id, species=species)
        logger.debug("Planted %s", plant_id)
        return plant

    def harvest(self, plant_id: str) -> bool:
        plant = self.plants.get(plant_id)
        if not plant or plant.growth < 1.0:
            return False
        del self.plants[plant_id]
        publish("plant_harvested", plant_id=plant_id, species=plant.species)
        logger.debug("Harvested %s", plant_id)
        return True

    def apply_fertilizer(self, plant_id: str, chemical: str) -> None:
        plant = self.plants.get(plant_id)
        if not plant:
            return
        if chemical == "nutriment":
            plant.nutrient += 1
            plant.health += 0.5
        elif chemical == "ammonia":
            plant.nutrient += 1
            plant.yield_amount += 1
        elif chemical == "diethylamine":
            plant.nutrient += 2
            plant.health += 1
            plant.yield_amount += 1
        elif chemical == "saltpetre":
            plant.potency += 1
            plant.production_time = max(1.0, plant.production_time - 1)
            plant.health += 1
        elif chemical == "unstable_mutagen":
            plant.potency += 2
            plant.toxicity += 1
        elif chemical == "ash":
            plant.nutrient += 0.5
            plant.health += 0.25
        elif chemical == "multiver":
            plant.toxicity = max(0.0, plant.toxicity - 1)
        elif chemical == "plant_b_gone":
            plant.health = 0
        # pest_killer and weed_killer not explicitly modelled

    def analyze_plant(self, plant_id: str) -> Dict[str, float]:
        plant = self.plants.get(plant_id)
        if not plant:
            return {}
        return {
            "species": plant.species,
            "growth": round(plant.growth, 2),
            "health": plant.health,
            "nutrient": plant.nutrient,
            "yield": plant.yield_amount,
            "potency": plant.potency,
            "toxicity": plant.toxicity,
        }

    # ------------------------------------------------------------------
    def update(self) -> None:
        if not self.enabled:
            return
        now = time.time()
        if now - self.last_tick < self.tick_interval:
            return
        self.last_tick = now
        for plant in list(self.plants.values()):
            plant.growth += self.growth_rate / max(1.0, plant.production_time)
            if plant.growth >= 1.0:
                publish(
                    "plant_mature", plant_id=plant.plant_id, species=plant.species
                )


BOTANY_SYSTEM = BotanySystem()


def get_botany_system() -> BotanySystem:
    return BOTANY_SYSTEM
