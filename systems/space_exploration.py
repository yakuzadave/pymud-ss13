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

    def sample_hazards(self) -> List[str]:
        """Roll for environmental hazards occurring this tick."""
        hazards = []
        for hazard in self.environment:
            if random.random() < hazard.chance:
                hazards.append(hazard.name)
                publish("away_site_hazard", site_id=self.site_id, hazard=hazard.name)
        return hazards


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


@dataclass
class AwayMission:
    """Tracks the state of an off-station mission."""

    mission_id: str
    shuttle: Shuttle
    site: AwaySite
    crew: List[str] = field(default_factory=list)
    active: bool = False

    def launch(self) -> bool:
        if self.active:
            return False
        if not self.shuttle.navigate(self.site.site_id):
            return False
        self.active = True
        publish("mission_started", mission_id=self.mission_id, site=self.site.site_id)
        return True

    def tick(self) -> None:
        if not self.active:
            return
        hazards = self.site.sample_hazards()
        if hazards:
            publish("mission_hazard", mission_id=self.mission_id, hazards=hazards)

    def return_to_base(self, dock_id: str = "station") -> None:
        self.shuttle.dock(dock_id)
        self.active = False
        publish("mission_completed", mission_id=self.mission_id, site=self.site.site_id)


class SpaceExplorationSystem:
    """High level manager for shuttles and missions."""

    def __init__(self) -> None:
        self.shuttles: Dict[str, Shuttle] = {}
        self.sites: Dict[str, AwaySite] = {}
        self.missions: Dict[str, AwayMission] = {}

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
        site = AwaySite(site_id, name, hazards or [], resources or {})
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
