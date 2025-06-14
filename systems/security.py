"""Security and crime management system."""

import logging
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any

from events import publish, subscribe

logger = logging.getLogger(__name__)


@dataclass
class CrimeRecord:
    """Represents a crime report."""

    crime_id: int
    reporter_id: str
    suspect_id: Optional[str]
    description: str
    severity: str
    evidence: List[str] = field(default_factory=list)
    status: str = "open"


@dataclass
class Prisoner:
    """Represents an incarcerated player."""

    player_id: str
    cell_id: Optional[str]
    release_time: float
    parole: bool = False


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
    """Central system for crime tracking and security monitoring."""

    def __init__(self) -> None:
        # Crime/prison management
        self._next_crime_id = 1
        self.crimes: Dict[int, CrimeRecord] = {}
        self.prisoners: Dict[str, Prisoner] = {}

        # Monitoring infrastructure
        self.cameras: Dict[str, Camera] = {}
        self.sensors: Dict[str, MotionSensor] = {}
        self.access_log: List[Dict[str, Any]] = []
        self.alerts: List[Dict[str, Any]] = []

        self.enabled = False
        subscribe("object_moved", self.on_object_moved)
        subscribe("door_opened", self.on_access_event)
        subscribe("door_closed", self.on_access_event)
        logger.info("Security system initialized")

    # ------------------------------------------------------------------
    # Crime database
    # ------------------------------------------------------------------
    def report_crime(
        self,
        reporter_id: str,
        description: str,
        suspect_id: Optional[str] = None,
        severity: str = "minor",
    ) -> CrimeRecord:
        """Record a new crime and return the record."""
        cid = self._next_crime_id
        self._next_crime_id += 1
        record = CrimeRecord(
            crime_id=cid,
            reporter_id=reporter_id,
            suspect_id=suspect_id,
            description=description,
            severity=severity,
        )
        self.crimes[cid] = record
        publish(
            "crime_reported",
            crime_id=cid,
            reporter_id=reporter_id,
            suspect_id=suspect_id,
            severity=severity,
        )
        logger.info(f"Crime reported {cid} by {reporter_id}")
        return record

    def add_evidence(self, crime_id: int, evidence_desc: str) -> bool:
        record = self.crimes.get(crime_id)
        if not record:
            return False
        record.evidence.append(evidence_desc)
        publish("evidence_collected", crime_id=crime_id, description=evidence_desc)
        return True

    def arrest(self, player_id: str, duration: float, cell_id: Optional[str] = None) -> Prisoner:
        """Arrest a player and add them to the prisoner database."""
        release_time = time.time() + duration
        prisoner = Prisoner(player_id=player_id, cell_id=cell_id, release_time=release_time)
        self.prisoners[player_id] = prisoner
        publish("player_arrested", player_id=player_id, cell_id=cell_id, duration=duration)
        logger.info(f"Player {player_id} arrested for {duration} seconds")
        return prisoner

    def release(self, player_id: str) -> bool:
        prisoner = self.prisoners.pop(player_id, None)
        if not prisoner:
            return False
        publish("player_released", player_id=player_id)
        logger.info(f"Player {player_id} released from prison")
        return True

    def check_sentence_expirations(self) -> None:
        """Release prisoners whose sentences have elapsed."""
        now = time.time()
        expired = [pid for pid, p in self.prisoners.items() if p.release_time <= now]
        for pid in expired:
            self.release(pid)

    # ------------------------------------------------------------------
    # Monitoring infrastructure
    # ------------------------------------------------------------------
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

_SECURITY_SYSTEM = SecuritySystem()


def get_security_system() -> SecuritySystem:
    """Return the global security system instance."""
    return _SECURITY_SYSTEM
