import logging
import random
from typing import Dict, List

from events import publish
import world

logger = logging.getLogger(__name__)


class DiseaseSystem:
    """Very simple disease tracking and transmission system."""

    def __init__(self) -> None:
        self.definitions: Dict[str, Dict[str, float]] = {
            "flu": {"damage_per_tick": 1.0, "transmission_chance": 0.5},
            "virus_x": {"damage_per_tick": 2.0, "transmission_chance": 0.3},
        }
        self.infected: Dict[str, List[str]] = {}

    def infect(self, player_id: str, disease: str) -> None:
        if disease not in self.definitions:
            return
        player = world.get_world().get_object(player_id)
        if not player:
            return
        comp = player.get_component("player")
        if not comp:
            return
        comp.contract_disease(disease)
        self.infected.setdefault(player_id, []).append(disease)
        logger.debug(f"{player_id} infected with {disease}")

    def cure(self, player_id: str, disease: str) -> None:
        player = world.get_world().get_object(player_id)
        if not player:
            return
        comp = player.get_component("player")
        if not comp:
            return
        comp.cure_disease(disease)
        if player_id in self.infected and disease in self.infected[player_id]:
            self.infected[player_id].remove(disease)

    def tick(self) -> None:
        for player_id, diseases in list(self.infected.items()):
            player = world.get_world().get_object(player_id)
            if not player:
                continue
            comp = player.get_component("player")
            if not comp:
                continue
            for disease in list(diseases):
                dmg = self.definitions[disease].get("damage_per_tick", 0)
                comp.apply_damage("torso", "toxin", dmg)
                publish(
                    "disease_tick", player_id=player_id, disease=disease, damage=dmg
                )
                if not comp.alive:
                    diseases.remove(disease)

            # Attempt to spread diseases to others in the same location
            location = player.location
            if location:
                others = world.get_world().get_objects_in_location(location)
                for other in others:
                    if other.id == player_id:
                        continue
                    ocomp = other.get_component("player")
                    if not ocomp or ocomp.has_biohazard_protection():
                        continue
                    for disease in diseases:
                        if disease in ocomp.diseases:
                            continue
                        chance = self.definitions[disease].get(
                            "transmission_chance", 0.1
                        )
                        if random.random() < chance:
                            self.infect(other.id, disease)


disease_system = DiseaseSystem()


def get_disease_system() -> DiseaseSystem:
    return disease_system
