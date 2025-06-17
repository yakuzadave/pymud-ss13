"""
Power system for MUDpy SS13.
Handles power grids, generators, and power failures.
"""

import logging
from typing import Dict, List, Any, Optional, Set
import random
import time
from events import subscribe, publish
import world

logger = logging.getLogger(__name__)


class PowerGrid:
    """
    Represents a power grid in the station.

    A power grid is a collection of connected rooms that share power.
    If the grid fails, all connected rooms lose power.
    """

    def __init__(self, grid_id: str, name: str):
        """
        Initialize a power grid.

        Args:
            grid_id (str): Unique identifier for this grid.
            name (str): Human-readable name for this grid.
        """
        self.grid_id = grid_id
        self.name = name
        self.rooms: Set[str] = set()
        self.is_powered = True
        self.power_source: Optional[str] = (
            None  # ID of the power source (generator, battery, etc.)
        )
        self.current_load = 0.0  # Current power load (0-100%)
        self.capacity = 100.0  # Maximum power capacity

    def add_room(self, room_id: str) -> None:
        """
        Add a room to this power grid.

        Args:
            room_id (str): The ID of the room to add.
        """
        self.rooms.add(room_id)
        logger.debug(f"Added room {room_id} to power grid {self.grid_id}")

    def remove_room(self, room_id: str) -> bool:
        """
        Remove a room from this power grid.

        Args:
            room_id (str): The ID of the room to remove.

        Returns:
            bool: True if the room was removed, False if it wasn't in the grid.
        """
        if room_id in self.rooms:
            self.rooms.remove(room_id)
            logger.debug(f"Removed room {room_id} from power grid {self.grid_id}")
            return True
        return False

    def set_power_source(self, source_id: str) -> None:
        """
        Set the power source for this grid.

        Args:
            source_id (str): The ID of the power source.
        """
        self.power_source = source_id
        logger.debug(f"Set power source for grid {self.grid_id} to {source_id}")

    def update_load(self, load: float) -> None:
        """
        Update the current power load.

        Args:
            load (float): The new power load (0-100%).
        """
        old_load = self.current_load
        self.current_load = max(0, min(100, load))
        logger.debug(
            f"Updated power load for grid {self.grid_id} from {old_load}% to {self.current_load}%"
        )

    def is_overloaded(self) -> bool:
        """
        Check if the grid is overloaded.

        Returns:
            bool: True if the current load exceeds capacity, False otherwise.
        """
        return self.current_load > self.capacity

    def power_off(self) -> None:
        """
        Turn off power to this grid.
        """
        if self.is_powered:
            self.is_powered = False
            logger.info(f"Power grid {self.grid_id} ({self.name}) powered down")
            publish("power_loss", grid_id=self.grid_id, affected_rooms=list(self.rooms))

    def power_on(self) -> None:
        """
        Turn on power to this grid.
        """
        if not self.is_powered:
            self.is_powered = True
            logger.info(f"Power grid {self.grid_id} ({self.name}) powered up")
            publish(
                "power_restored", grid_id=self.grid_id, affected_rooms=list(self.rooms)
            )


class PowerSystem:
    """
    System that manages power throughout the station.
    """

    def __init__(self, tick_interval: float = 30.0):
        """
        Initialize the power system.

        Args:
            tick_interval (float): Time between power updates in seconds.
        """
        self.tick_interval = tick_interval
        self.last_tick_time = 0
        self.enabled = False
        self.grids: Dict[str, PowerGrid] = {}
        self.generators: Dict[str, Dict[str, Any]] = {}
        self.solar_panels: Dict[str, Dict[str, Any]] = {}
        self.batteries: Dict[str, Dict[str, Any]] = {}
        self.smes_units: Dict[str, Dict[str, Any]] = {}
        self.consumers: Dict[str, Dict[str, Any]] = {}
        self.room_power_status: Dict[str, bool] = {}
        self.usage_history: Dict[str, List[float]] = {}

        # Register event handlers
        subscribe("generator_toggle", self.on_generator_toggle)
        subscribe("battery_depleted", self.on_battery_depleted)
        subscribe("solar_panel_efficiency_change", self.on_solar_efficiency_change)
        subscribe("grid_breaker_toggle", self.on_grid_breaker_toggle)

        logger.info("Power system initialized")

    def register_grid(self, grid: PowerGrid) -> None:
        """
        Register a power grid with the system.

        Args:
            grid (PowerGrid): The power grid to register.
        """
        self.grids[grid.grid_id] = grid
        for room_id in grid.rooms:
            self.room_power_status[room_id] = grid.is_powered
        logger.debug(f"Registered power grid {grid.grid_id} ({grid.name})")

    def register_generator(
        self, gen_id: str, grid_id: str, capacity: float = 100.0, is_active: bool = True
    ) -> None:
        """
        Register a generator with the system.

        Args:
            gen_id (str): The ID of the generator.
            grid_id (str): The ID of the grid this generator powers.
            capacity (float): The power capacity of this generator.
            is_active (bool): Whether the generator is currently active.
        """
        self.generators[gen_id] = {
            "grid_id": grid_id,
            "capacity": capacity,
            "is_active": is_active,
            "fuel_level": 100.0,
        }

        # Set the generator as the power source for the grid
        if grid_id in self.grids:
            self.grids[grid_id].set_power_source(gen_id)

        logger.debug(f"Registered generator {gen_id} for grid {grid_id}")

    def register_battery(
        self,
        battery_id: str,
        grid_id: str,
        capacity: float = 50.0,
        charge: float = 100.0,
    ) -> None:
        """
        Register a backup battery with the system.

        Args:
            battery_id (str): The ID of the battery.
            grid_id (str): The ID of the grid this battery can power.
            capacity (float): The power capacity of this battery.
            charge (float): The current charge level (0-100%).
        """
        self.batteries[battery_id] = {
            "grid_id": grid_id,
            "capacity": capacity,
            "charge": charge,
            "is_active": False,
        }
        logger.debug(f"Registered battery {battery_id} for grid {grid_id}")

    def register_solar_panel(
        self,
        panel_id: str,
        grid_id: str,
        efficiency: float = 80.0,
        is_active: bool = True,
    ) -> None:
        """
        Register a solar panel with the system.

        Args:
            panel_id (str): The ID of the solar panel.
            grid_id (str): The ID of the grid this panel powers.
            efficiency (float): The efficiency of the panel (0-100%).
            is_active (bool): Whether the panel is currently active.
        """
        self.solar_panels[panel_id] = {
            "grid_id": grid_id,
            "efficiency": efficiency,
            "is_active": is_active,
        }
        logger.debug(f"Registered solar panel {panel_id} for grid {grid_id}")

    def register_smes(
        self,
        smes_id: str,
        grid_id: str,
        capacity: float = 100.0,
        charge: float = 0.0,
        input_rate: float = 20.0,
        output_rate: float = 20.0,
    ) -> None:
        """Register an SMES unit for energy storage."""
        self.smes_units[smes_id] = {
            "grid_id": grid_id,
            "capacity": capacity,
            "charge": charge,
            "input_rate": input_rate,
            "output_rate": output_rate,
        }
        logger.debug(f"Registered SMES {smes_id} for grid {grid_id}")

    def register_consumer(
        self, consumer_id: str, grid_id: str, load: float, active: bool = True
    ) -> None:
        """Register a power consumer device."""
        self.consumers[consumer_id] = {
            "grid_id": grid_id,
            "load": load,
            "active": active,
        }

    def update_consumer_status(self, consumer_id: str, active: bool) -> None:
        if consumer_id in self.consumers:
            self.consumers[consumer_id]["active"] = active

    def update_consumer_load(self, consumer_id: str, load: float) -> None:
        if consumer_id in self.consumers:
            self.consumers[consumer_id]["load"] = load

    def remove_consumer(self, consumer_id: str) -> None:
        self.consumers.pop(consumer_id, None)

    def start(self) -> None:
        """
        Start the power system.
        """
        self.enabled = True
        self.last_tick_time = time.time()
        logger.info("Power system started")

    def stop(self) -> None:
        """
        Stop the power system.
        """
        self.enabled = False
        logger.info("Power system stopped")

    def update(self) -> None:
        """
        Update power conditions throughout the station.
        Should be called regularly from the main game loop.
        """
        if not self.enabled:
            return

        current_time = time.time()
        if current_time - self.last_tick_time < self.tick_interval:
            return

        self.last_tick_time = current_time
        logger.debug("Processing power update cycle")

        # Update each grid
        for grid_id, grid in self.grids.items():
            load = self.get_grid_load(grid_id)

            total_power = 0.0

            for gen_id, gen_data in self.generators.items():
                if gen_data["grid_id"] == grid_id and gen_data["is_active"]:
                    if gen_data["fuel_level"] > 0:
                        gen_data["fuel_level"] -= random.uniform(0.5, 1.5)
                        gen_data["fuel_level"] = max(0, gen_data["fuel_level"])
                        if gen_data["fuel_level"] <= 0:
                            gen_data["is_active"] = False
                            logger.info(f"Generator {gen_id} ran out of fuel")
                            publish("generator_out_of_fuel", generator_id=gen_id)
                        else:
                            total_power += gen_data["capacity"]

            for panel_id, panel_data in self.solar_panels.items():
                if panel_data["grid_id"] == grid_id and panel_data["is_active"]:
                    total_power += panel_data["efficiency"] * 0.5

            # SMES discharge if needed
            for smes_id, smes in self.smes_units.items():
                if smes["grid_id"] == grid_id:
                    if total_power < load and smes["charge"] > 0:
                        needed = min(
                            load - total_power, smes["output_rate"], smes["charge"]
                        )
                        smes["charge"] -= needed
                        total_power += needed
                    elif total_power > load and smes["charge"] < smes["capacity"]:
                        surplus = min(
                            total_power - load,
                            smes["input_rate"],
                            smes["capacity"] - smes["charge"],
                        )
                        smes["charge"] += surplus
                        total_power -= surplus

            grid.capacity = total_power
            grid.update_load(load)
            hist = self.usage_history.setdefault(grid_id, [])
            hist.append(grid.current_load)
            if len(hist) > 20:
                del hist[0]

            if total_power <= 0:
                # No power available, check for batteries
                battery_power = self._activate_backup_batteries(grid_id)

                if battery_power > 0:
                    grid.capacity = battery_power
                    if not grid.is_powered:
                        grid.power_on()
                elif grid.is_powered:
                    grid.power_off()
            elif grid.is_overloaded():
                grid.power_off()
                logger.warning(
                    f"Power grid {grid_id} overloaded (load: {grid.current_load}%, capacity: {grid.capacity}%)"
                )
                publish(
                    "grid_overload",
                    grid_id=grid_id,
                    load=grid.current_load,
                    capacity=grid.capacity,
                )
                self.cause_electrical_hazard(grid_id)
            elif not grid.is_powered:
                # Power is available and grid is not overloaded, restore power
                grid.power_on()

            # Update room power status for this grid
            self._update_rooms_for_grid(grid)

            publish(
                "power_status_update",
                grid_id=grid_id,
                is_powered=grid.is_powered,
                load=grid.current_load,
                capacity=grid.capacity,
            )

    def _activate_backup_batteries(self, grid_id: str) -> float:
        """
        Activate backup batteries for a grid with no primary power.

        Args:
            grid_id (str): The ID of the grid.

        Returns:
            float: The amount of power provided by batteries.
        """
        total_battery_power = 0.0

        for battery_id, battery_data in self.batteries.items():
            if battery_data["grid_id"] == grid_id and battery_data["charge"] > 0:
                if not battery_data["is_active"]:
                    battery_data["is_active"] = True
                    logger.info(f"Battery {battery_id} activated for grid {grid_id}")
                    publish("battery_activated", battery_id=battery_id, grid_id=grid_id)

                # Batteries drain when in use
                battery_data["charge"] -= random.uniform(2, 5)
                battery_data["charge"] = max(0, battery_data["charge"])

                if battery_data["charge"] <= 0:
                    battery_data["is_active"] = False
                    logger.info(f"Battery {battery_id} depleted")
                    publish("battery_depleted", battery_id=battery_id, grid_id=grid_id)
                else:
                    total_battery_power += battery_data["capacity"] * (
                        battery_data["charge"] / 100.0
                    )

        return total_battery_power

    def cause_power_failure(
        self, grid_id: str, duration: Optional[float] = None
    ) -> None:
        """
        Cause a power failure in a grid.

        Args:
            grid_id (str): The ID of the grid to affect.
            duration (float, optional): How long the failure will last in seconds.
                                       If None, the failure is permanent until fixed.
        """
        if grid_id in self.grids:
            grid = self.grids[grid_id]
            grid.power_off()
            self.cause_electrical_hazard(grid_id)

            # Deactivate power sources
            for gen_id, gen_data in self.generators.items():
                if gen_data["grid_id"] == grid_id:
                    gen_data["is_active"] = False

            logger.info(f"Caused power failure in grid {grid_id}")
            publish("manual_power_failure", grid_id=grid_id, duration=duration)

            # If duration is specified, schedule power restoration
            if duration is not None:
                # In a real implementation, you'd use a timer or scheduler
                # For now, we'll just log that it would be restored
                logger.info(
                    f"Power will be restored to grid {grid_id} after {duration} seconds"
                )

    def on_generator_toggle(self, generator_id: str, active: bool) -> None:
        """
        Handle a generator being toggled on or off.

        Args:
            generator_id (str): The ID of the generator.
            active (bool): Whether the generator should be active.
        """
        if generator_id in self.generators:
            self.generators[generator_id]["is_active"] = active
            status = "activated" if active else "deactivated"
            logger.info(f"Generator {generator_id} {status}")

    def on_battery_depleted(self, battery_id: str, grid_id: str) -> None:
        """
        Handle a battery being depleted.

        Args:
            battery_id (str): The ID of the depleted battery.
            grid_id (str): The ID of the grid.
        """
        # Check if the grid is now without power
        if grid_id in self.grids:
            grid = self.grids[grid_id]

            # Check if there are any other power sources
            has_power = False
            for gen_id, gen_data in self.generators.items():
                if (
                    gen_data["grid_id"] == grid_id
                    and gen_data["is_active"]
                    and gen_data["fuel_level"] > 0
                ):
                    has_power = True
                    break

            for panel_id, panel_data in self.solar_panels.items():
                if panel_data["grid_id"] == grid_id and panel_data["is_active"]:
                    has_power = True
                    break

            # Check if there are other batteries
            other_batteries = False
            for b_id, b_data in self.batteries.items():
                if (
                    b_id != battery_id
                    and b_data["grid_id"] == grid_id
                    and b_data["is_active"]
                    and b_data["charge"] > 0
                ):
                    other_batteries = True
                    break

            if not has_power and not other_batteries and grid.is_powered:
                grid.power_off()

    def on_solar_efficiency_change(self, panel_id: str, efficiency: float) -> None:
        """
        Handle a change in solar panel efficiency.

        Args:
            panel_id (str): The ID of the solar panel.
            efficiency (float): The new efficiency (0-100%).
        """
        if panel_id in self.solar_panels:
            self.solar_panels[panel_id]["efficiency"] = max(0, min(100, efficiency))
            logger.info(f"Solar panel {panel_id} efficiency changed to {efficiency}%")

    def on_grid_breaker_toggle(self, grid_id: str, active: bool) -> None:
        """
        Handle a grid breaker being toggled on or off.

        Args:
            grid_id (str): The ID of the grid.
            active (bool): Whether the breaker should be active (closed).
        """
        if grid_id in self.grids:
            grid = self.grids[grid_id]
            if active:
                if not grid.is_powered:
                    grid.power_on()
                logger.info(f"Grid breaker closed for {grid_id}, power restored")
            else:
                if grid.is_powered:
                    grid.power_off()
                logger.info(f"Grid breaker opened for {grid_id}, power cut")

    def get_grid_load(self, grid_id: str) -> float:
        return sum(
            data["load"]
            for data in self.consumers.values()
            if data["grid_id"] == grid_id and data["active"]
        )

    def _update_rooms_for_grid(self, grid: PowerGrid) -> None:
        for room_id in grid.rooms:
            prev = self.room_power_status.get(room_id)
            if prev is None or prev != grid.is_powered:
                self.room_power_status[room_id] = grid.is_powered
                publish(
                    "room_power_changed",
                    room_id=room_id,
                    powered=grid.is_powered,
                )

    def get_room_power_status(self, room_id: str) -> bool:
        return self.room_power_status.get(room_id, True)

    def describe_room_power(self, room_id: str) -> str:
        """Return a short text description of power in ``room_id``."""
        powered = self.get_room_power_status(room_id)
        return (
            f"Power is flowing normally in {room_id}."
            if powered
            else f"{room_id} is without power."
        )

    def get_usage_graph(self, grid_id: str, width: int = 10) -> str:
        """Return a simple ASCII graph of recent power usage for a grid."""
        history = self.usage_history.get(grid_id, [])
        if not history:
            return "No data"
        points = history[-width:]
        return " ".join(f"{int(v):3d}" for v in points)

    def cause_electrical_hazard(self, grid_id: str) -> None:
        if grid_id in self.grids:
            rooms = list(self.grids[grid_id].rooms)
            publish("electrical_hazard", grid_id=grid_id, affected_rooms=rooms)


# Create a global power system instance
POWER_SYSTEM = PowerSystem()


def get_power_system() -> PowerSystem:
    """
    Get the global power system instance.

    Returns:
        PowerSystem: The global power system instance.
    """
    return POWER_SYSTEM
