"""Simplified physics helpers for structural damage and environment effects."""

from dataclasses import dataclass
from typing import Dict
from events import subscribe
from world import get_world


@dataclass
class Material:
    """Basic material properties."""

    name: str
    yield_strength: float  # pressure in kPa the material withstands
    heat_resistance: float  # temperature in Celsius before damage


# Default material library
MATERIALS: Dict[str, Material] = {
    "steel": Material("steel", yield_strength=250.0, heat_resistance=1000.0),
    "glass": Material("glass", yield_strength=50.0, heat_resistance=500.0),
}


class PhysicsSystem:
    """Apply environmental effects and propagate damage."""

    def __init__(self) -> None:
        subscribe("structure_destroyed", self._on_structure_destroyed)

    def apply_environment(
        self, structure_id: str, pressure: float, temperature: float
    ) -> None:
        world = get_world()
        obj = world.get_object(structure_id)
        if not obj:
            return
        comp = obj.get_component("structure")
        if not comp:
            return
        comp.apply_environment(pressure, temperature)

    def _on_structure_destroyed(self, structure_id: str | None, **_: Dict) -> None:
        if not structure_id:
            return
        world = get_world()
        obj = world.get_object(structure_id)
        if not obj or obj.position is None:
            return
        x, y = obj.position
        for nx, ny in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            for oid in world.grid.objects_at(nx, ny):
                neighbor = world.get_object(oid)
                if not neighbor:
                    continue
                comp = neighbor.get_component("structure")
                if comp:
                    comp.damage(5)


PHYSICS_SYSTEM = PhysicsSystem()


def get_physics_system() -> PhysicsSystem:
    return PHYSICS_SYSTEM
