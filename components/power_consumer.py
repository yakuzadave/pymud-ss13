"""Power consumer component for MUDpy SS13.
Represents equipment that requires electrical power."""

from typing import Any, List
import logging
from events import subscribe, publish
from systems.power import get_power_system

logger = logging.getLogger(__name__)


class PowerConsumerComponent:
    """Component representing a powered piece of equipment."""

    def __init__(
        self, grid_id: str, power_usage: float = 5.0, active: bool = True
    ) -> None:
        self.owner = None
        self.grid_id = grid_id
        self.power_usage = power_usage
        self.active = active
        self.damaged = False

        subscribe("power_loss", self._on_power_loss)
        subscribe("power_restored", self._on_power_restored)
        subscribe("electrical_hazard", self._on_electrical_hazard)

    def on_added(self) -> None:
        """Register this consumer with the global power system."""
        get_power_system().register_consumer(
            self.owner.id, self.grid_id, self.power_usage, self.active
        )

    def _room_in_list(self, rooms: List[str]) -> bool:
        room_id = self.owner.location or self.owner.id
        return room_id in rooms

    def _on_power_loss(
        self, grid_id: str, affected_rooms: List[str] | None = None, **_: Any
    ) -> None:
        if grid_id != self.grid_id:
            return
        if affected_rooms is None or self._room_in_list(affected_rooms):
            self.active = False
            get_power_system().update_consumer_status(self.owner.id, False)
            publish("equipment_power_off", object_id=self.owner.id)

    def _on_power_restored(
        self, grid_id: str, affected_rooms: List[str] | None = None, **_: Any
    ) -> None:
        if grid_id != self.grid_id:
            return
        if affected_rooms is None or self._room_in_list(affected_rooms):
            self.active = True
            get_power_system().update_consumer_status(self.owner.id, True)
            publish("equipment_power_on", object_id=self.owner.id)

    def _on_electrical_hazard(
        self, grid_id: str, affected_rooms: List[str] | None = None, **_: Any
    ) -> None:
        if grid_id != self.grid_id:
            return
        if affected_rooms is None or self._room_in_list(affected_rooms):
            self.damaged = True
            publish("equipment_damaged", object_id=self.owner.id)

    def to_dict(self) -> dict:
        return {
            "grid_id": self.grid_id,
            "power_usage": self.power_usage,
            "active": self.active,
            "damaged": self.damaged,
        }
