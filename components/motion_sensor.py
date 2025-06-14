"""Motion sensor component."""

import logging
from typing import Dict, Any

from systems.security import get_security_system

logger = logging.getLogger(__name__)


class MotionSensorComponent:
    """Motion sensor sending events to the security system."""

    def __init__(self, location: str, sensitivity: float = 1.0) -> None:
        self.owner = None
        self.location = location
        self.sensitivity = sensitivity
        self.active = True

    def on_added(self) -> None:
        get_security_system().register_sensor(self.owner.id, self.location, self.sensitivity)

    def to_dict(self) -> Dict[str, Any]:
        return {"location": self.location, "sensitivity": self.sensitivity, "active": self.active}
