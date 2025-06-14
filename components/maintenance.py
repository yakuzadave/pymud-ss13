"""Maintainable equipment component for MUDpy SS13."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import List, Optional

from events import publish
from systems.maintenance import get_maintenance_system

logger = logging.getLogger(__name__)


@dataclass
class MaintainableComponent:
    """Component that tracks equipment wear and maintenance."""

    wear_rate: float = 1.0
    env_factor: float = 1.0
    failure_threshold: float = 20.0
    next_service_due: float = field(default_factory=lambda: time.time() + 600)
    condition: float = 100.0
    last_service: float = field(default_factory=time.time)
    is_operational: bool = True

    def __post_init__(self) -> None:
        self.owner = None

    def on_added(self) -> None:
        """Register with the global maintenance system."""
        get_maintenance_system().register(self.owner.id, self)

    # ------------------------------------------------------------------
    # Usage handling
    # ------------------------------------------------------------------
    def apply_usage(self, intensity: float = 1.0) -> None:
        """Apply wear based on usage intensity."""
        if not self.is_operational:
            return
        wear = intensity * self.wear_rate * self.env_factor
        self.condition = max(0.0, self.condition - wear)
        logger.debug(
            f"{getattr(self.owner, 'id', 'unknown')} wear {wear}, condition {self.condition}"
        )
        if self.condition <= self.failure_threshold:
            self.is_operational = False
            publish("equipment_failed", object_id=getattr(self.owner, "id", ""))

    # ------------------------------------------------------------------
    # Maintenance
    # ------------------------------------------------------------------
    def service(self, skill: int, tools: Optional[List[str]] = None) -> bool:
        """Service the equipment to restore condition."""
        if skill < 1:
            return False
        self.condition = 100.0
        self.last_service = time.time()
        self.next_service_due = self.last_service + 600
        self.is_operational = True
        publish("equipment_repaired", object_id=getattr(self.owner, "id", ""))
        return True
