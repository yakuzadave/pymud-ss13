"""Space exploration and away mission support systems."""

from __future__ import annotations

import logging
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import time

from .cargo import get_cargo_system

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
        publish(
            "shuttle_departed",
            shuttle_id=self.shuttle_id,
            destination=destination,
        )
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


# Default hazards used when creating exploration sites
DEFAULT_HAZARDS = [
    EnvironmentalHazard("radiation pocket", chance=0.1, severity=2),
    EnvironmentalHazard("vacuum section", chance=0.1, severity=3),
    EnvironmentalHazard("micro-meteoroids", chance=0.05, severity=1),
    EnvironmentalHazard("alien spores", chance=0.05, severity=2),
    EnvironmentalHazard("radiation storm", chance=0.05, severity=3),
    EnvironmentalHazard("hull breach", chance=0.03, severity=4),
]


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
                publish(
                    "away_site_hazard",
                    site_id=self.site_id,
                    hazard=hazard.name,
                )
        return hazards

    def harvest(self, resource: str, amount: int) -> int:
        """Collect resources from the site."""
        available = self.resources.get(resource, 0)
        collected = min(amount, available)
        if collected:
            self.resources[resource] -= collected
        return collected

    def spawn_resources(self) -> Dict[str, int]:
        """Randomly generate new resource deposits."""
        spawned: Dict[str, int] = {}
        for res_name in ["ore", "crystal", "ice"]:
            if random.random() < self.resource_chance:
                amount = random.randint(1, 3)
                self.resources[res_name] = self.resources.get(res_name, 0) + amount
                spawned[res_name] = spawned.get(res_name, 0) + amount
                publish(
                    "away_site_resource_spawned",
                    site_id=self.site_id,
                    resource=res_name,
                    amount=amount,
                )
        return spawned


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
class CrewStatus:
    """Tracks per-crew condition during a mission."""

    oxygen_used: int = 0
    radiation: int = 0


@dataclass
class ShuttleSchedule:
    """Scheduled flight for a shuttle."""

    destination: str
    departure: float


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
    crew_status: Dict[str, CrewStatus] = field(default_factory=dict)

    def launch(self) -> bool:
        if self.active:
            return False
        if not self.shuttle.navigate(self.site.site_id):
            return False
        self.active = True
        self.suits = {cid: EVASuit(cid) for cid in self.crew}
        self.crew_status = {cid: CrewStatus() for cid in self.crew}
        self.collected_resources.clear()
        publish(
            "mission_started",
            mission_id=self.mission_id,
            site=self.site.site_id,
        )
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
                for cid, suit in self.suits.items():
                    suit.apply_hazard(hazard)
                    status = self.crew_status.get(cid)
                    if status:
                        if "radiation" in hazard.name:
                            status.radiation += hazard.severity * 5
                        if "hull breach" in hazard.name or "vacuum" in hazard.name:
                            loss = min(suit.oxygen, hazard.severity * 2)
                            suit.oxygen -= loss
                            status.oxygen_used += loss
        for cid, suit in self.suits.items():
            before = suit.oxygen
            suit.tick()
            self.crew_status[cid].oxygen_used += before - suit.oxygen

    def return_to_base(self, dock_id: str = "station") -> None:
        self.shuttle.dock(dock_id)
        self.active = False
        publish(
            "mission_completed",
            mission_id=self.mission_id,
            site=self.site.site_id,
            resources=self.collected_resources,
            crew_status=self.crew_status,
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
        self.schedules: Dict[str, List[ShuttleSchedule]] = {}

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
            hazards = random.sample(
                DEFAULT_HAZARDS,
                k=random.randint(2, min(3, len(DEFAULT_HAZARDS))),
            )
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
            mission.site.spawn_resources()

        # Check scheduled flights
        now = time.time()
        for shuttle_id, schedules in list(self.schedules.items()):
            while schedules and schedules[0].departure <= now:
                sched = schedules.pop(0)
                shuttle = self.shuttles.get(shuttle_id)
                if shuttle:
                    shuttle.navigate(sched.destination)

    # ------------------------------------------------------------------
    def complete_mission(self, mission_id: str, dock_id: str = "station") -> None:
        mission = self.missions.pop(mission_id, None)
        if not mission:
            return
        mission.return_to_base(dock_id)
        for res, qty in mission.collected_resources.items():
            self.station_resources[res] = self.station_resources.get(res, 0) + qty
            cargo = get_cargo_system()
            inv = cargo.get_inventory("mining")
            inv[res] = inv.get(res, 0) + qty
        publish(
            "mission_resources_returned",
            mission_id=mission_id,
            resources=mission.collected_resources,
            crew_status=mission.crew_status,
        )

    # ------------------------------------------------------------------
    def schedule_shuttle(
        self, shuttle_id: str, destination: str, departure: float
    ) -> bool:
        shuttle = self.shuttles.get(shuttle_id)
        if not shuttle:
            return False
        entries = self.schedules.setdefault(shuttle_id, [])
        entries.append(ShuttleSchedule(destination, departure))
        entries.sort(key=lambda s: s.departure)
        return True

    def get_schedule(self, shuttle_id: str) -> List[ShuttleSchedule]:
        return list(self.schedules.get(shuttle_id, []))
