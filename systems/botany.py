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
    """Simple plant record."""

    plant_id: str
    species: str
    growth: float = 0.0
    planted_at: float = field(default_factory=time.time)


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

    # ------------------------------------------------------------------
    def update(self) -> None:
        if not self.enabled:
            return
        now = time.time()
        if now - self.last_tick < self.tick_interval:
            return
        self.last_tick = now
        for plant in list(self.plants.values()):
            plant.growth += self.growth_rate
            if plant.growth >= 1.0:
                publish(
                    "plant_mature", plant_id=plant.plant_id, species=plant.species
                )


BOTANY_SYSTEM = BotanySystem()


def get_botany_system() -> BotanySystem:
    return BOTANY_SYSTEM
