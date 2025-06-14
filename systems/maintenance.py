"""Maintenance system managing equipment wear and repairs."""

from __future__ import annotations

import logging
import time
from typing import Dict

from events import publish

logger = logging.getLogger(__name__)


class MaintenanceSystem:
    """Track maintainable equipment and schedule upkeep."""

    def __init__(self, tick_interval: float = 60.0) -> None:
        self.tick_interval = tick_interval
        self.last_tick = 0.0
        self.enabled = False
        self.equipment: Dict[str, "MaintainableComponent"] = {}

    def register(self, obj_id: str, comp: "MaintainableComponent") -> None:
        self.equipment[obj_id] = comp

    def start(self) -> None:
        self.enabled = True
        self.last_tick = time.time()

    def stop(self) -> None:
        self.enabled = False

    def update(self) -> None:
        if not self.enabled:
            return
        now = time.time()
        if now - self.last_tick < self.tick_interval:
            return
        self.last_tick = now
        for obj_id, comp in list(self.equipment.items()):
            if comp.condition > comp.failure_threshold:
                comp.apply_usage(intensity=0.1)
                if comp.condition <= comp.failure_threshold:
                    publish("equipment_failed", object_id=obj_id)
            if now >= comp.next_service_due:
                publish("maintenance_due", object_id=obj_id)


MAINTENANCE_SYSTEM = MaintenanceSystem()


def get_maintenance_system() -> MaintenanceSystem:
    """Return the global maintenance system."""

    return MAINTENANCE_SYSTEM
