"""Fluid container component for the PlumbingSystem."""

from __future__ import annotations

from typing import Dict


class FluidContainerComponent:
    """Simple fluid container that stores multiple fluid types."""

    def __init__(self, capacity: float = 100.0) -> None:
        self.owner = None
        self.capacity = capacity
        self.contents: Dict[str, float] = {}

    def current_volume(self) -> float:
        return sum(self.contents.values())

    # ------------------------------------------------------------------
    def add_fluid(self, kind: str, amount: float) -> bool:
        if amount <= 0:
            return False
        if self.current_volume() + amount > self.capacity:
            return False
        self.contents[kind] = self.contents.get(kind, 0.0) + amount
        return True

    def remove_fluid(self, kind: str, amount: float) -> bool:
        if amount <= 0:
            return False
        if self.contents.get(kind, 0.0) < amount:
            return False
        self.contents[kind] -= amount
        if self.contents[kind] <= 0:
            del self.contents[kind]
        return True

    def transfer_to(self, other: "FluidContainerComponent") -> None:
        for kind, amt in list(self.contents.items()):
            move = min(amt, other.capacity - other.current_volume())
            if move <= 0:
                continue
            other.add_fluid(kind, move)
            self.remove_fluid(kind, move)

    def to_dict(self) -> Dict[str, float]:
        return {"capacity": self.capacity, "contents": dict(self.contents)}
