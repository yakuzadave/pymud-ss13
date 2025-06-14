"""
Atmospheric system for MUDpy SS13.
Handles gas mixtures, pressure, temperature, and related hazards.
"""

import logging
from typing import Dict, List, Any, Optional
import random
import time
from events import subscribe, publish
import world

logger = logging.getLogger(__name__)

# Constants for atmospheric simulation
NORMAL_PRESSURE = 101.3  # kPa
NORMAL_OXYGEN = 21.0  # percent
NORMAL_NITROGEN = 78.0  # percent
NORMAL_CO2 = 0.04  # percent

# Thresholds for hazardous conditions
LOW_OXYGEN_THRESHOLD = 10.0  # percent
HIGH_CO2_THRESHOLD = 5.0  # percent
LOW_PRESSURE_THRESHOLD = 80.0  # kPa
HIGH_PRESSURE_THRESHOLD = 120.0  # kPa

class AtmosphericSystem:
    """
    System that manages atmospheric conditions throughout the station.
    """

    def __init__(self, tick_interval: float = 10.0):
        """
        Initialize the atmospheric system.

        Args:
            tick_interval (float): Time between atmospheric updates in seconds.
        """
        self.tick_interval = tick_interval
        self.last_tick_time = 0
        self.enabled = False
        self.vents: Dict[str, Dict[str, Any]] = {}  # room_id -> vent data
        self.leaks: List[Dict[str, Any]] = []  # List of active leaks

        # Register event handlers
        subscribe("power_loss", self.on_power_loss)
        subscribe("power_restored", self.on_power_restored)
        subscribe("breach", self.on_breach)
        subscribe("vent_toggle", self.on_vent_toggle)

        logger.info("Atmospheric system initialized")

    def register_vent(self, room_id: str, output_rate: float = 1.0, is_active: bool = True) -> None:
        """
        Register a ventilation system for a room.

        Args:
            room_id (str): The ID of the room.
            output_rate (float): The rate at which the vent normalizes atmosphere.
            is_active (bool): Whether the vent is currently active.
        """
        self.vents[room_id] = {
            "output_rate": output_rate,
            "is_active": is_active
        }
        logger.debug(f"Registered vent for room {room_id}")

    def start(self) -> None:
        """
        Start the atmospheric system.
        """
        self.enabled = True
        self.last_tick_time = time.time()
        logger.info("Atmospheric system started")

    def stop(self) -> None:
        """
        Stop the atmospheric system.
        """
        self.enabled = False
        logger.info("Atmospheric system stopped")

    def update(self) -> None:
        """
        Update atmospheric conditions throughout the station.
        Should be called regularly from the main game loop.
        """
        if not self.enabled:
            return

        current_time = time.time()
        if current_time - self.last_tick_time < self.tick_interval:
            return

        self.last_tick_time = current_time
        logger.debug("Processing atmospheric update cycle")

        # Get the world instance
        world_instance = world.get_world()

        # Update atmosphere for each room
        for room_id, room_obj in world_instance.rooms.items():
            room_comp = room_obj.get_component('room')
            if not room_comp:
                continue

            # Apply vent normalization if active
            if room_id in self.vents and self.vents[room_id]["is_active"]:
                self._normalize_atmosphere(room_comp, self.vents[room_id]["output_rate"])

            # Apply effects of any leaks affecting this room
            for leak in self.leaks:
                if leak["room_id"] == room_id:
                    self._apply_leak_effects(room_comp, leak)

            # Update hazards based on current atmospheric conditions
            self._update_hazards(room_comp)

            # Publish atmospheric update event for this room
            publish("atmos_updated", room_id=room_id, atmosphere=room_comp.atmosphere, hazards=room_comp.hazards)

    def _normalize_atmosphere(self, room_comp: Any, rate: float) -> None:
        """
        Normalize the atmosphere in a room toward standard conditions.

        Args:
            room_comp: The room component.
            rate (float): The rate of normalization.
        """
        # Adjust each gas toward normal values
        if "atmosphere" in room_comp.__dict__:
            atmos = room_comp.atmosphere

            # Adjust oxygen
            if "oxygen" in atmos:
                diff = NORMAL_OXYGEN - atmos["oxygen"]
                atmos["oxygen"] += diff * rate * 0.1
            else:
                atmos["oxygen"] = NORMAL_OXYGEN

            # Adjust nitrogen
            if "nitrogen" in atmos:
                diff = NORMAL_NITROGEN - atmos["nitrogen"]
                atmos["nitrogen"] += diff * rate * 0.1
            else:
                atmos["nitrogen"] = NORMAL_NITROGEN

            # Adjust CO2
            if "co2" in atmos:
                diff = NORMAL_CO2 - atmos["co2"]
                atmos["co2"] += diff * rate * 0.1
            else:
                atmos["co2"] = NORMAL_CO2

            # Adjust pressure
            if "pressure" in atmos:
                diff = NORMAL_PRESSURE - atmos["pressure"]
                atmos["pressure"] += diff * rate * 0.1
            else:
                atmos["pressure"] = NORMAL_PRESSURE

    def _apply_leak_effects(self, room_comp: Any, leak: Dict[str, Any]) -> None:
        """
        Apply the effects of a leak to a room's atmosphere.

        Args:
            room_comp: The room component.
            leak (Dict[str, Any]): Data about the leak.
        """
        if "atmosphere" in room_comp.__dict__:
            atmos = room_comp.atmosphere

            # Reduce oxygen
            if "oxygen" in atmos:
                atmos["oxygen"] -= leak["rate"] * 0.5
                atmos["oxygen"] = max(0, atmos["oxygen"])

            # Reduce pressure
            if "pressure" in atmos:
                atmos["pressure"] -= leak["rate"] * 2.0
                atmos["pressure"] = max(0, atmos["pressure"])

    def _update_hazards(self, room_comp: Any) -> None:
        """
        Update the hazards in a room based on atmospheric conditions.

        Args:
            room_comp: The room component.
        """
        if not hasattr(room_comp, "atmosphere") or not hasattr(room_comp, "hazards"):
            return

        atmos = room_comp.atmosphere

        # Check for low oxygen
        if atmos.get("oxygen", NORMAL_OXYGEN) < LOW_OXYGEN_THRESHOLD:
            if "low_oxygen" not in room_comp.hazards:
                room_comp.hazards.append("low_oxygen")
                logger.debug(f"Low oxygen hazard added to room {room_comp.owner.id}")
        elif "low_oxygen" in room_comp.hazards:
            room_comp.hazards.remove("low_oxygen")

        # Check for high CO2
        if atmos.get("co2", NORMAL_CO2) > HIGH_CO2_THRESHOLD:
            if "high_co2" not in room_comp.hazards:
                room_comp.hazards.append("high_co2")
                logger.debug(f"High CO2 hazard added to room {room_comp.owner.id}")
        elif "high_co2" in room_comp.hazards:
            room_comp.hazards.remove("high_co2")

        # Check for low pressure
        if atmos.get("pressure", NORMAL_PRESSURE) < LOW_PRESSURE_THRESHOLD:
            if "low_pressure" not in room_comp.hazards:
                room_comp.hazards.append("low_pressure")
                logger.debug(f"Low pressure hazard added to room {room_comp.owner.id}")
        elif "low_pressure" in room_comp.hazards:
            room_comp.hazards.remove("low_pressure")

        # Check for high pressure
        if atmos.get("pressure", NORMAL_PRESSURE) > HIGH_PRESSURE_THRESHOLD:
            if "high_pressure" not in room_comp.hazards:
                room_comp.hazards.append("high_pressure")
                logger.debug(f"High pressure hazard added to room {room_comp.owner.id}")
        elif "high_pressure" in room_comp.hazards:
            room_comp.hazards.remove("high_pressure")

    def create_leak(self, room_id: str, rate: float = 1.0, duration: Optional[float] = None) -> None:
        """
        Create a leak in a room that will affect its atmosphere.

        Args:
            room_id (str): The ID of the room with the leak.
            rate (float): The rate of the leak.
            duration (float, optional): How long the leak will last in seconds.
                                       If None, the leak is permanent until fixed.
        """
        leak = {
            "room_id": room_id,
            "rate": rate,
            "created_at": time.time(),
            "duration": duration
        }

        self.leaks.append(leak)
        logger.info(f"Created leak in room {room_id} with rate {rate}")
        publish("leak_started", room_id=room_id, rate=rate)

    def fix_leak(self, room_id: str) -> bool:
        """
        Fix all leaks in a room.

        Args:
            room_id (str): The ID of the room.

        Returns:
            bool: True if any leaks were fixed, False otherwise.
        """
        fixed = False
        leaks_to_remove = []

        for leak in self.leaks:
            if leak["room_id"] == room_id:
                leaks_to_remove.append(leak)
                fixed = True

        for leak in leaks_to_remove:
            self.leaks.remove(leak)
            logger.info(f"Fixed leak in room {room_id}")
            publish("leak_fixed", room_id=room_id)

        return fixed

    def on_power_loss(self, affected_rooms: Optional[List[str]] = None, **_: Any) -> None:
        """
        Handle power loss event by disabling vents in affected rooms.

        Args:
            affected_rooms (List[str], optional): List of affected room IDs.
                                                If None, all rooms are affected.
        """
        if affected_rooms is None:
            # Disable all vents
            for room_id in self.vents:
                self.vents[room_id]["is_active"] = False
            logger.info("All vents disabled due to power loss")
        else:
            # Disable vents in affected rooms
            for room_id in affected_rooms:
                if room_id in self.vents:
                    self.vents[room_id]["is_active"] = False
            logger.info(f"Vents disabled in {len(affected_rooms)} rooms due to power loss")

    def on_power_restored(self, affected_rooms: Optional[List[str]] = None, **_: Any) -> None:
        """
        Handle power restored event by re-enabling vents in affected rooms.

        Args:
            affected_rooms (List[str], optional): List of affected room IDs.
                                                If None, all rooms are affected.
        """
        if affected_rooms is None:
            # Enable all vents
            for room_id in self.vents:
                self.vents[room_id]["is_active"] = True
            logger.info("All vents re-enabled due to power restoration")
        else:
            # Enable vents in affected rooms
            for room_id in affected_rooms:
                if room_id in self.vents:
                    self.vents[room_id]["is_active"] = True
            logger.info(f"Vents re-enabled in {len(affected_rooms)} rooms due to power restoration")

    def on_breach(self, room_id: str, severity: float = 1.0) -> None:
        """
        Handle a breach event by creating a leak.

        Args:
            room_id (str): The ID of the room with the breach.
            severity (float): The severity of the breach (affects leak rate).
        """
        self.create_leak(room_id, rate=severity)
        logger.info(f"Breach detected in room {room_id} with severity {severity}")

    def on_vent_toggle(self, room_id: str, active: bool) -> None:
        """
        Handle a vent being toggled on or off.

        Args:
            room_id (str): The ID of the room.
            active (bool): Whether the vent should be active.
        """
        if room_id in self.vents:
            self.vents[room_id]["is_active"] = active
            status = "activated" if active else "deactivated"
            logger.info(f"Vent in room {room_id} {status}")

# Create a global atmospheric system instance
ATMOS_SYSTEM = AtmosphericSystem()

def get_atmos_system() -> AtmosphericSystem:
    """
    Get the global atmospheric system instance.

    Returns:
        AtmosphericSystem: The global atmospheric system instance.
    """
    return ATMOS_SYSTEM
