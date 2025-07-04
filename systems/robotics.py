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
    """Equipment installed on a cyborg that can be remotely toggled."""

    module_id: str
    name: str
    power_usage: int = 1
    remote_control: bool = False
    active: bool = True

    def set_active(self, active: bool) -> None:
        """Activate or deactivate the module."""
        self.active = active
        publish(
            "module_activated" if active else "module_deactivated",
            module_id=self.module_id,
        )


@dataclass
class SpecializedRobotModule(RobotModule):
    """Module with a specific functionality and custom power usage."""

    functionality: str = ""


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

    def remote_control_module(self, module_id: str, active: bool) -> bool:
        """Toggle a module if it supports remote control."""
        for mod in self.modules:
            if mod.module_id == module_id and mod.remote_control:
                mod.set_active(active)
                return True
        return False

    def diagnostics(self) -> Dict[str, object]:
        """Return a status report for the cyborg."""
        return {
            "unit": self.unit_id,
            "power": self.power,
            "modules": {m.module_id: m.active for m in self.modules},
        }

    def repair(self) -> None:
        """Restore power and reactivate all modules."""
        for mod in self.modules:
            mod.active = True
        self.recharge()
        publish("cyborg_repaired", unit_id=self.unit_id)

    def execute_command(self, command: str) -> bool:
        """Handle remote commands affecting the whole unit."""
        cmd = command.lower()
        if cmd == "shutdown":
            for mod in self.modules:
                mod.active = False
            self.power = 0
            publish("cyborg_shutdown", unit_id=self.unit_id)
            return True
        if cmd == "restart":
            for mod in self.modules:
                mod.active = True
            self.recharge()
            publish("cyborg_restarted", unit_id=self.unit_id)
            return True
        if cmd == "repair":
            self.repair()
            return True
        if cmd == "diagnostics":
            publish("cyborg_diagnostics", unit_id=self.unit_id, info=self.diagnostics())
            return True
        return False

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
            if mod.active:
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

    # ------------------------------------------------------------------
    def remote_control(
        self, unit_id: str, module_id: str, active: bool
    ) -> bool:
        """Remotely toggle a module on a cyborg."""
        unit = self.units.get(unit_id)
        if not unit:
            return False
        return unit.remote_control_module(module_id, active)

    # ------------------------------------------------------------------
    def remote_command(self, unit_id: str, command: str) -> bool:
        """Send a high level command to a cyborg unit."""
        unit = self.units.get(unit_id)
        if not unit:
            return False
        return unit.execute_command(command)

    # ------------------------------------------------------------------
    def diagnose_unit(self, unit_id: str) -> Optional[Dict[str, object]]:
        unit = self.units.get(unit_id)
        if not unit:
            return None
        return unit.diagnostics()

    # ------------------------------------------------------------------
    def repair_unit(self, unit_id: str) -> bool:
        unit = self.units.get(unit_id)
        if not unit:
            return False
        unit.repair()
        return True


_ROBOTICS_SYSTEM = RoboticsSystem()


def get_robotics_system() -> RoboticsSystem:
    return _ROBOTICS_SYSTEM
