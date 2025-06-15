"""Simplified circuit component for MUDpy SS13."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict

# Simplified shell capacities inspired by SS13
SHELL_CAPACITY = {
    "Compact Remote": 25,
    "Remote": 25,
    "Drone Shell": 25,
    "Wall-Mounted Case": 50,
    "Bot Shell": 100,
    "BCI Shell": 500,
}

@dataclass
class CircuitComponent:
    """Lightweight representation of an electronic circuit."""

    shell_type: str = "Compact Remote"
    components: List[str] = field(default_factory=list)
    power: int = 0
    active: bool = False

    def __post_init__(self) -> None:
        self.owner = None

    def max_components(self) -> int:
        return SHELL_CAPACITY.get(self.shell_type, 25)

    def insert(self, component: str) -> bool:
        if len(self.components) >= self.max_components():
            return False
        self.components.append(component)
        return True

    def remove(self, component: str) -> bool:
        if component in self.components:
            self.components.remove(component)
            return True
        return False

    def toggle(self, state: bool) -> None:
        self.active = state
