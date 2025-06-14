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
        return cyb.receive_command(command)

    def check_action(self, action: str) -> bool:
        """Very simple conflict resolution for demonstration."""
        for law in self.get_laws():
            if "harm" in action.lower() and "harm" in law.lower() and "never" in law.lower():
                return False
        return True

    def to_dict(self) -> Dict[str, List[Dict[str, int]]]:
        """Serialize this component."""
        return {"laws": [{"priority": l.priority, "directive": l.directive} for l in self.laws]}


class CyborgComponent:
    """Component for robotic units controlled by an AI."""

    def __init__(self, modules: Optional[List[str]] = None) -> None:
        self.owner = None
        self.modules = modules or []
        self.ai: Optional[AIComponent] = None

    def receive_command(self, command: str) -> str:
        """Acknowledge a command from the AI."""
        publish("cyborg_command", cyborg_id=self.owner.id, command=command)
        return f"{self.owner.name} executes '{command}'"

    def to_dict(self) -> Dict[str, List[str]]:
        return {"modules": self.modules}
