from __future__ import annotations

"""Simple robotics lab and cyborg management."""

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from events import publish

logger = logging.getLogger(__name__)


@dataclass
class RobotChassis:
    """Defines module slots and power capacity for a cyborg."""

    chassis_id: str
    name: str
    slots: int = 2
    power_capacity: int = 100


@dataclass
class RobotModule:
    """Equipment that consumes power when installed."""

    module_id: str
    name: str
    power_usage: int = 1


@dataclass
class DockingStation:
    """Location where cyborgs can recharge."""

    station_id: str
    location: str
    recharge_rate: int = 5


@dataclass
class CyborgUnit:
    """A chassis with installed modules and a power cell."""

    unit_id: str
    chassis: RobotChassis
    modules: List[RobotModule] = field(default_factory=list)
    power: int = 0
    location: Optional[str] = None
    docked_at: Optional[str] = None

    def install_module(self, module: RobotModule) -> bool:
        if len(self.modules) >= self.chassis.slots:
            return False
        self.modules.append(module)
        logger.debug(
            "Installed module %s on %s",
            module.module_id,
            self.unit_id,
        )
        return True

    def recharge(self, amount: Optional[int] = None) -> None:
        """Recharge the cyborg's power cell."""
        if amount is None:
            self.power = self.chassis.power_capacity
        else:
            self.power = min(self.chassis.power_capacity, self.power + amount)
        if self.power == self.chassis.power_capacity:
            publish("cyborg_recharged", unit_id=self.unit_id)

    def dock(self, station: DockingStation) -> None:
        """Move to a docking station and begin recharging."""
        self.location = station.location
        self.docked_at = station.station_id

    def tick(self) -> None:
        for mod in self.modules:
            self.power = max(0, self.power - mod.power_usage)
        if self.power == 0:
            publish("cyborg_out_of_power", unit_id=self.unit_id)


class RoboticsSystem:
    """Tracks parts and builds cyborg units."""

    def __init__(self) -> None:
        self.parts: Dict[str, int] = {}
        self.recipes: Dict[str, Dict[str, int]] = {}
        self.units: Dict[str, CyborgUnit] = {}
        self.docking_stations: Dict[str, DockingStation] = {}

    # ------------------------------------------------------------------
    def add_parts(self, part_id: str, amount: int) -> None:
        self.parts[part_id] = self.parts.get(part_id, 0) + amount
        logger.debug("Added %d of %s", amount, part_id)

    # ------------------------------------------------------------------
    def define_recipe(self, chassis_id: str, required: Dict[str, int]) -> None:
        self.recipes[chassis_id] = dict(required)
        logger.debug("Defined recipe for %s", chassis_id)

    # ------------------------------------------------------------------
    def add_docking_station(self, station: DockingStation) -> None:
        """Register a new docking station."""
        self.docking_stations[station.station_id] = station
        logger.debug("Added docking station %s", station.station_id)

    # ------------------------------------------------------------------
    def build_cyborg(
        self, unit_id: str, chassis: RobotChassis
    ) -> Optional[CyborgUnit]:

        req = self.recipes.get(chassis.chassis_id, {})
        for part, qty in req.items():
            if self.parts.get(part, 0) < qty:
                logger.info("Missing part %s for cyborg %s", part, unit_id)
                return None
        for part, qty in req.items():
            self.parts[part] -= qty
        unit = CyborgUnit(unit_id, chassis)
        unit.recharge()
        self.units[unit_id] = unit
        publish("cyborg_built", unit_id=unit_id, chassis=chassis.chassis_id)
        return unit

    # ------------------------------------------------------------------
    def tick(self) -> None:
        for unit in list(self.units.values()):
            unit.tick()

            if unit.docked_at:
                station = self.docking_stations.get(unit.docked_at)
                if station:
                    unit.recharge(station.recharge_rate)
                continue

            if unit.power <= unit.chassis.power_capacity * 0.2:
                if self.docking_stations:
                    station = next(iter(self.docking_stations.values()))
                    unit.dock(station)
                    unit.recharge(station.recharge_rate)
                    publish(
                        "cyborg_docking",
                        unit_id=unit.unit_id,
                        station_id=station.station_id,
                    )


_ROBOTICS_SYSTEM = RoboticsSystem()


def get_robotics_system() -> RoboticsSystem:
    return _ROBOTICS_SYSTEM
