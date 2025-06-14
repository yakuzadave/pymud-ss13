"""Security monitoring system for MUDpy SS13."""

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Any

from events import publish, subscribe

logger = logging.getLogger(__name__)


@dataclass
class Camera:
    """Representation of a security camera."""

    camera_id: str
    location: str
    active: bool = True
    recordings: List[str] = field(default_factory=list)


@dataclass
class MotionSensor:
    """Representation of a motion sensor."""

    sensor_id: str
    location: str
    sensitivity: float = 1.0
    active: bool = True


class SecuritySystem:
    """Central security monitoring system."""

    def __init__(self) -> None:
        self.cameras: Dict[str, Camera] = {}
        self.sensors: Dict[str, MotionSensor] = {}
        self.access_log: List[Dict[str, Any]] = []
        self.alerts: List[Dict[str, Any]] = []

        self.enabled = False
        subscribe("object_moved", self.on_object_moved)
        subscribe("door_opened", self.on_access_event)
        subscribe("door_closed", self.on_access_event)
        logger.info("Security system initialized")

    def register_camera(self, camera_id: str, location: str) -> None:
        self.cameras[camera_id] = Camera(camera_id, location)
        logger.debug(f"Registered camera {camera_id} at {location}")

    def register_sensor(self, sensor_id: str, location: str, sensitivity: float = 1.0) -> None:
        self.sensors[sensor_id] = MotionSensor(sensor_id, location, sensitivity)
        logger.debug(f"Registered sensor {sensor_id} at {location}")

    def start(self) -> None:
        """Activate the security system."""
        self.enabled = True
        logger.info("Security system started")

    def stop(self) -> None:
        """Deactivate the security system."""
        self.enabled = False
        logger.info("Security system stopped")

    def on_object_moved(self, object_id: str, from_location: str | None, to_location: str | None, **_: Any) -> None:
        if not to_location:
            return
        for sensor in self.sensors.values():
            if sensor.active and sensor.location == to_location:
                alert = {"type": "motion", "object": object_id, "location": to_location}
                self.alerts.append(alert)
                publish("security_alert", alert=alert)
                logger.debug(f"Motion detected by {sensor.sensor_id} in {to_location}")

    def on_access_event(self, door_id: str, player_id: str, **_: Any) -> None:
        entry = {"door": door_id, "player": player_id}
        self.access_log.append(entry)
        logger.debug(f"Access event on {door_id} by {player_id}")

    def update(self) -> None:
        """Process pending alerts."""
        if not self.enabled:
            return
        while self.alerts:
            alert = self.alerts.pop(0)
            publish("security_dispatch", alert=alert)

    def get_alerts(self) -> List[Dict[str, Any]]:
        return list(self.alerts)

    def get_access_log(self) -> List[Dict[str, Any]]:
        return list(self.access_log)


SECURITY_SYSTEM = SecuritySystem()


def get_security_system() -> SecuritySystem:
    """Return the global security system instance."""
    return SECURITY_SYSTEM
