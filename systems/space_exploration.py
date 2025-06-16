"""Space exploration and away mission support systems."""

from __future__ import annotations

import logging
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from events import publish

logger = logging.getLogger(__name__)


@dataclass
class Shuttle:
    """Simple shuttle representation with basic flight controls."""

    shuttle_id: str
    name: str
    fuel: int = 100
    location: str = "station"
    docked: bool = True

    def navigate(self, destination: str) -> bool:
        """Travel to a new location if fuel is available."""
        if self.fuel <= 0:
            logger.info("Shuttle %s is out of fuel", self.shuttle_id)
            return False
        self.fuel -= 10
        self.location = destination
        self.docked = False
        publish("shuttle_departed", shuttle_id=self.shuttle_id, destination=destination)
        return True

    def dock(self, dock_id: str) -> None:
        """Dock the shuttle at a station or outpost."""
        self.location = dock_id
        self.docked = True
        publish("shuttle_docked", shuttle_id=self.shuttle_id, dock_id=dock_id)

    def refuel(self, amount: int) -> None:
        """Refuel the shuttle up to its maximum capacity."""
        self.fuel = min(self.fuel + amount, 100)
        publish("shuttle_refueled", shuttle_id=self.shuttle_id, fuel=self.fuel)


@dataclass
class EnvironmentalHazard:
    """Represents a potential danger at an away site."""

    name: str
    chance: float  # Probability each tick (0.0-1.0)
    severity: int = 1


@dataclass
class AwaySite:
    """Procedurally generated exploration site."""

    site_id: str
    name: str
    environment: List[EnvironmentalHazard] = field(default_factory=list)
    resources: Dict[str, int] = field(default_factory=dict)

    def sample_hazards(self) -> List[EnvironmentalHazard]:
        """Roll for environmental hazards occurring this tick."""
        hazards = []
        for hazard in self.environment:
            if random.random() < hazard.chance:
                hazards.append(hazard)
                publish("away_site_hazard", site_id=self.site_id, hazard=hazard.name)
        return hazards

    def harvest(self, resource: str, amount: int) -> int:
        """Collect resources from the site."""
        available = self.resources.get(resource, 0)
        collected = min(amount, available)
        if collected:
            self.resources[resource] -= collected
        return collected


@dataclass
class EVASuit:
    """Basic environmental suit with limited life support."""

    wearer_id: str
    oxygen: int = 100
    integrity: int = 100

    def tick(self) -> None:
        if self.oxygen > 0:
            self.oxygen -= 1
        if self.oxygen <= 0:
            publish("suit_out_of_oxygen", wearer=self.wearer_id)

    def apply_hazard(self, hazard: EnvironmentalHazard) -> None:
        """Damage the suit if a severe hazard is encountered."""
        if hazard.severity >= 2:
            self.integrity = max(0, self.integrity - hazard.severity * 10)
            publish(
                "suit_damaged",
                wearer=self.wearer_id,
                hazard=hazard.name,
                integrity=self.integrity,
            )


@dataclass
class AwayMission:
    """Tracks the state of an off-station mission."""

    mission_id: str
    shuttle: Shuttle
    site: AwaySite
    crew: List[str] = field(default_factory=list)
    active: bool = False
    suits: Dict[str, EVASuit] = field(default_factory=dict)
    collected_resources: Dict[str, int] = field(default_factory=dict)

    def launch(self) -> bool:
        if self.active:
            return False
        if not self.shuttle.navigate(self.site.site_id):
            return False
        self.active = True
        self.suits = {cid: EVASuit(cid) for cid in self.crew}
        self.collected_resources.clear()
        publish("mission_started", mission_id=self.mission_id, site=self.site.site_id)
        return True

    def tick(self) -> None:
        if not self.active:
            return
        hazards = self.site.sample_hazards()
        if hazards:
            publish(
                "mission_hazard",
                mission_id=self.mission_id,
                hazards=[h.name for h in hazards],
            )
            for hazard in hazards:
                for suit in self.suits.values():
                    suit.apply_hazard(hazard)
        for suit in self.suits.values():
            suit.tick()

    def return_to_base(self, dock_id: str = "station") -> None:
        self.shuttle.dock(dock_id)
        self.active = False
        publish(
            "mission_completed",
            mission_id=self.mission_id,
            site=self.site.site_id,
            resources=self.collected_resources,
        )

    def harvest(self, resource: str, amount: int) -> int:
        """Harvest resources from the site and store them."""
        gathered = self.site.harvest(resource, amount)
        if gathered:
            self.collected_resources[resource] = (
                self.collected_resources.get(resource, 0) + gathered
            )
        return gathered


class SpaceExplorationSystem:
    """High level manager for shuttles and missions."""

    def __init__(self) -> None:
        self.shuttles: Dict[str, Shuttle] = {}
        self.sites: Dict[str, AwaySite] = {}
        self.missions: Dict[str, AwayMission] = {}
        self.station_resources: Dict[str, int] = {}

    # ------------------------------------------------------------------
    def register_shuttle(self, shuttle: Shuttle) -> None:
        self.shuttles[shuttle.shuttle_id] = shuttle

    # ------------------------------------------------------------------
    def create_site(
        self,
        site_id: str,
        name: str,
        hazards: Optional[List[EnvironmentalHazard]] = None,
        resources: Optional[Dict[str, int]] = None,
    ) -> AwaySite:
        if hazards is None:
            hazards = [
                EnvironmentalHazard("radiation pocket", chance=0.1, severity=2),
                EnvironmentalHazard("vacuum section", chance=0.1, severity=3),
            ]
        if resources is None:
            resources = {}
            for res_name in ["ore", "crystal", "ice"]:
                if random.random() < 0.5:
                    resources[res_name] = random.randint(1, 5)
        site = AwaySite(site_id, name, hazards, resources)
        self.sites[site_id] = site
        return site

    # ------------------------------------------------------------------
    def start_mission(
        self, mission_id: str, shuttle_id: str, site_id: str, crew: List[str]
    ) -> Optional[AwayMission]:
        shuttle = self.shuttles.get(shuttle_id)
        site = self.sites.get(site_id)
        if not shuttle or not site:
            return None
        mission = AwayMission(mission_id, shuttle, site, crew)
        if mission.launch():
            self.missions[mission_id] = mission
            return mission
        return None

    # ------------------------------------------------------------------
    def tick(self) -> None:
        for mission in list(self.missions.values()):
            mission.tick()

    # ------------------------------------------------------------------
    def complete_mission(self, mission_id: str, dock_id: str = "station") -> None:
        mission = self.missions.pop(mission_id, None)
        if not mission:
            return
        mission.return_to_base(dock_id)
        for res, qty in mission.collected_resources.items():
            self.station_resources[res] = self.station_resources.get(res, 0) + qty
        publish(
            "mission_resources_returned",
            mission_id=mission_id,
            resources=mission.collected_resources,
        )
