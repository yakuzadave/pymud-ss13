"""AI related helpers and systems."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Dict, List, Optional, Any

from events import publish, subscribe
from components.ai import Law
from systems.jobs import get_job_system

logger = logging.getLogger(__name__)


def is_ai_client(client_id: str) -> bool:
    """Return True if the given client is assigned the AI job."""
    player_id = client_id
    if not player_id.startswith("player_"):
        player_id = f"player_{client_id}"
    job = get_job_system().get_player_job(player_id)
    return bool(job and job.job_id == "ai")


class CameraNetwork:
    """Track security camera feeds for AI clients."""

    def __init__(self) -> None:
        self.cameras: Dict[str, str] = {}
        subscribe("camera_added", self._on_camera_added)
        subscribe("camera_toggle", self._on_camera_toggle)

    # ------------------------------------------------------------------
    def _on_camera_added(self, camera_id: str, location: str, **_: Any) -> None:
        self.cameras[camera_id] = location
        logger.debug("Camera %s registered at %s", camera_id, location)

    def _on_camera_toggle(self, camera_id: str, state: bool, **_: Any) -> None:
        if not state and camera_id in self.cameras:
            logger.debug("Camera %s disabled", camera_id)

    # ------------------------------------------------------------------
    def register_camera(self, camera_id: str, location: str) -> None:
        self.cameras[camera_id] = location

    def list_feeds(self) -> Dict[str, str]:
        return dict(self.cameras)

    def get_feed(self, camera_id: str) -> Optional[str]:
        return self.cameras.get(camera_id)


class AILawSystem:
    """Central repository of AI and cyborg laws."""

    def __init__(self) -> None:
        self.laws: List[Law] = []

    # ------------------------------------------------------------------
    def add_law(self, priority: int, directive: str) -> None:
        self.laws.append(Law(priority, directive))
        self.laws.sort()
        publish("ai_law_added", priority=priority, directive=directive)

    def get_laws(self) -> List[str]:
        return [law.directive for law in self.laws]

    def clear(self) -> None:
        self.laws.clear()

    def check_action(self, action: str) -> bool:
        for law in self.laws:
            if (
                "harm" in action.lower()
                and "harm" in law.directive.lower()
                and "never" in law.directive.lower()
            ):
                return False
        return True


_CAMERA_NETWORK = CameraNetwork()
_AI_LAW_SYSTEM = AILawSystem()


def get_camera_network() -> CameraNetwork:
    return _CAMERA_NETWORK


def get_ai_law_system() -> AILawSystem:
    return _AI_LAW_SYSTEM
