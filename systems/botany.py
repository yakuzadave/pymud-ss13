"""Basic botany system for growing plants."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Dict, Set, Tuple
import random

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
    traits: Set[str] = field(default_factory=set)
    autogrow: bool = False
    position: Tuple[int, int] = (0, 0)


class BotanySystem:
    """Manage hydroponic trays and plant growth."""

    def __init__(
        self,
        growth_rate: float = 0.1,
        tick_interval: float = 10.0,
        cross_poll_chance: float = 0.25,
        cross_poll_radius: float = 1.0,
        autogrow_power_cost: float = 1.0,
        power: float = 100.0,
    ) -> None:
        self.growth_rate = growth_rate
        self.tick_interval = tick_interval
        self.last_tick = 0.0
        self.enabled = False
        self.cross_pollination = False
        self.cross_poll_chance = cross_poll_chance
        self.cross_poll_radius = cross_poll_radius
        self.autogrow_power_cost = autogrow_power_cost
        self.power = power
        self.plants: Dict[str, Plant] = {}
        self._counter = 1

    # ------------------------------------------------------------------
    def start(self) -> None:
        self.enabled = True
        self.last_tick = time.time()

    def stop(self) -> None:
        self.enabled = False

    # ------------------------------------------------------------------
    def toggle_autogrow(self, plant_id: str) -> bool:
        plant = self.plants.get(plant_id)
        if not plant:
            return False
        plant.autogrow = not plant.autogrow
        logger.debug("Autogrow for %s set to %s", plant_id, plant.autogrow)
        return plant.autogrow

    def add_power(self, amount: float) -> None:
        self.power += amount

    def toggle_cross_pollination(self, enabled: bool | None = None) -> bool:
        if enabled is None:
            self.cross_pollination = not self.cross_pollination
        else:
            self.cross_pollination = enabled
        logger.debug("Cross pollination set to %s", self.cross_pollination)
        return self.cross_pollination

    def graft(self, target_id: str, donor_id: str) -> bool:
        target = self.plants.get(target_id)
        donor = self.plants.get(donor_id)
        if not target or not donor or not donor.traits:
            return False
        target.traits.update(donor.traits)
        logger.debug("Grafted %s traits onto %s", donor_id, target_id)
        return True

    # ------------------------------------------------------------------
    def plant_seed(
        self, species: str, x: int | None = None, y: int | None = None
    ) -> Plant:
        plant_id = f"plant_{self._counter}"
        self._counter += 1
        if x is None or y is None:
            x = len(self.plants)
            y = 0
        plant = Plant(plant_id=plant_id, species=species, position=(x, y))
        self.plants[plant_id] = plant
        publish("seed_planted", plant_id=plant_id, species=species)
        logger.debug("Planted %s", plant_id)
        return plant

    def harvest(self, plant_id: str) -> bool:
        plant = self.plants.get(plant_id)
        if not plant or plant.growth < 1.0:
            return False
        # Special handling for replica pods which produce a cloning item
        if plant.species == "replica_pod":
            from world import get_world, GameObject
            from components.item import ItemComponent
            from components.replica_pod import ReplicaPodComponent

            pod_id = f"replica_pod_{plant_id}"
            pod = GameObject(
                id=pod_id,
                name="Replica Pod",
                description="A strange plant pod capable of cloning the dead.",
            )
            pod.add_component(
                "item",
                ItemComponent(is_takeable=True, is_usable=True, item_type="botany"),
            )
            pod.add_component("replica_pod", ReplicaPodComponent())
            get_world().register(pod)
            publish("replica_pod_created", object_id=pod_id)

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
            if plant.autogrow and self.power >= self.autogrow_power_cost:
                self.apply_fertilizer(plant.plant_id, "nutriment")
                self.power -= self.autogrow_power_cost
                plant.growth += self.growth_rate / max(1.0, plant.production_time)
            if plant.growth >= 1.0:
                publish("plant_mature", plant_id=plant.plant_id, species=plant.species)

        if self.cross_pollination and len(self.plants) > 1:
            plants = list(self.plants.values())
            for i, plant in enumerate(plants):
                for other in plants[i + 1 :]:
                    dx = plant.position[0] - other.position[0]
                    dy = plant.position[1] - other.position[1]
                    if (
                        dx * dx + dy * dy
                        <= self.cross_poll_radius * self.cross_poll_radius
                    ):
                        if random.random() <= self.cross_poll_chance and other.traits:
                            plant.traits.add(random.choice(list(other.traits)))
                        if random.random() <= self.cross_poll_chance and plant.traits:
                            other.traits.add(random.choice(list(plant.traits)))


BOTANY_SYSTEM = BotanySystem()


def get_botany_system() -> BotanySystem:
    return BOTANY_SYSTEM
