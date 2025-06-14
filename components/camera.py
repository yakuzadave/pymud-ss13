"""Camera component for security monitoring."""

import logging
from typing import Dict, Any

from systems.security import get_security_system
from events import publish

logger = logging.getLogger(__name__)


class CameraComponent:
    """Simple camera that reports to the security system."""

    def __init__(self, location: str) -> None:
        self.owner = None
        self.location = location
        self.active = True

    def on_added(self) -> None:
        get_security_system().register_camera(self.owner.id, self.location)
        publish("camera_added", camera_id=self.owner.id, location=self.location)

    def toggle(self, state: bool) -> None:
        self.active = state
        publish("camera_toggle", camera_id=self.owner.id, state=state)

    def to_dict(self) -> Dict[str, Any]:
        return {"location": self.location, "active": self.active}
