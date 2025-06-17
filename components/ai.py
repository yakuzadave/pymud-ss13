"""AI component and law system for MUDpy SS13."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import List, Dict, Optional

from events import publish

logger = logging.getLogger(__name__)


@dataclass(order=True)
class Law:
    """Represents a single AI law."""

    priority: int
    directive: str


class AIComponent:
    """AI core component storing laws and linked cyborgs."""

    def __init__(self, laws: Optional[List[Law]] = None) -> None:
        self.owner = None
        self.laws: List[Law] = sorted(laws or [])
        # key -> CyborgComponent
        self.cyborgs: Dict[str, "CyborgComponent"] = {}

    def add_law(self, priority: int, directive: str) -> None:
        """Add a new law with the given priority."""
        self.laws.append(Law(priority, directive))
        self.laws.sort()
        publish(
            "ai_law_added",
            ai_id=self.owner.id if self.owner else None,
            priority=priority,
            directive=directive,
        )

    def get_laws(self) -> List[str]:
        """Return directives ordered by priority."""
        return [law.directive for law in sorted(self.laws)]

    def register_cyborg(self, cyborg: "CyborgComponent") -> None:
        """Register a cyborg under this AI."""
        self.cyborgs[cyborg.owner.id] = cyborg
        cyborg.ai = self
        publish(
            "cyborg_registered",
            ai_id=self.owner.id if self.owner else None,
            cyborg_id=cyborg.owner.id,
        )

    def issue_command(self, cyborg_id: str, command: str) -> str:
        """Send a command to a cyborg if it exists."""
        cyb = self.cyborgs.get(cyborg_id)
        if not cyb:
            return "Cyborg not found."
        if not self.check_action(command):
            return "Unable to comply. Command conflicts with my laws."
        return cyb.receive_command(command)

    def check_action(self, action: str) -> bool:
        """Very simple conflict resolution for demonstration."""
        for law in self.get_laws():
            if (
                "harm" in action.lower()
                and "harm" in law.lower()
                and "never" in law.lower()
            ):
                return False
        return True

    def to_dict(self) -> Dict[str, List[Dict[str, int]]]:
        """Serialize this component."""
        return {
            "laws": [
                {"priority": l.priority, "directive": l.directive} for l in self.laws
            ]
        }


class CyborgComponent:
    """Component for robotic units controlled by an AI."""

    def __init__(self, modules: Optional[List[str]] = None, unit_id: Optional[str] = None) -> None:
        self.owner = None
        self.modules = modules or []
        self.ai: Optional[AIComponent] = None
        # optional id linking to RoboticsSystem
        self.unit_id = unit_id
        # fallback local power level when not using RoboticsSystem
        self.power = 100

    def receive_command(self, command: str) -> str:
        """Handle a command from the AI, enforcing its laws."""
        if self.ai and not self.ai.check_action(command):
            publish("cyborg_command_blocked", cyborg_id=self.owner.id, command=command)
            return f"{self.owner.name} refuses to execute '{command}'"

        from systems.robotics import get_robotics_system

        robo = get_robotics_system()
        if self.unit_id and self.unit_id in robo.units:
            robo.remote_command(self.unit_id, command)

        publish("cyborg_command", cyborg_id=self.owner.id, command=command)
        return f"{self.owner.name} executes '{command}'"

    def remote_control(self, module_id: str, active: bool) -> bool:
        """Toggle a module via the robotics system if possible."""
        from systems.robotics import get_robotics_system

        robo = get_robotics_system()
        if self.unit_id and self.unit_id in robo.units:
            return robo.remote_control(self.unit_id, module_id, active)
        return False

    def report_status(self) -> Dict[str, object]:
        """Return a diagnostic dictionary for the AI."""
        from systems.robotics import get_robotics_system

        robo = get_robotics_system()
        if self.unit_id and self.unit_id in robo.units:
            info = robo.diagnose_unit(self.unit_id)
        else:
            info = {
                "unit": self.unit_id or self.owner.id,
                "power": self.power,
                "modules": {m: True for m in self.modules},
            }
        publish("cyborg_status", cyborg_id=self.owner.id, info=info)
        return info

    def to_dict(self) -> Dict[str, object]:
        return {"modules": self.modules, "unit_id": self.unit_id, "power": self.power}
