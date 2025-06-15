from __future__ import annotations

"""CircuitSystem manages circuits and USB links."""

from dataclasses import dataclass
from typing import Dict, Optional

from components.circuit import CircuitComponent


@dataclass
class CircuitRecipe:
    """Recipe for assembling a circuit."""

    shell_type: str
    parts: Dict[str, int]


class CircuitSystem:
    """Tracks circuit parts, assemblies and power usage."""

    def __init__(self) -> None:
        self.parts: Dict[str, int] = {}
        self.recipes: Dict[str, CircuitRecipe] = {}
        self.circuits: Dict[str, CircuitComponent] = {}
        self.connections: Dict[str, str] = {}

    # ------------------------------------------------------------------
    def add_parts(self, part_id: str, amount: int) -> None:
        self.parts[part_id] = self.parts.get(part_id, 0) + amount

    # ------------------------------------------------------------------
    def define_recipe(self, recipe_id: str, shell_type: str, required: Dict[str, int]) -> None:
        self.recipes[recipe_id] = CircuitRecipe(shell_type, dict(required))

    # ------------------------------------------------------------------
    def assemble(self, circuit_id: str, recipe_id: str) -> Optional[CircuitComponent]:
        recipe = self.recipes.get(recipe_id)
        if not recipe:
            return None
        for part, qty in recipe.parts.items():
            if self.parts.get(part, 0) < qty:
                return None
        for part, qty in recipe.parts.items():
            self.parts[part] -= qty
        circuit = CircuitComponent(shell_type=recipe.shell_type, power=100)
        self.circuits[circuit_id] = circuit
        return circuit

    # ------------------------------------------------------------------
    def insert_component(self, circuit_id: str, component: str) -> bool:
        circuit = self.circuits.get(circuit_id)
        if not circuit:
            return False
        return circuit.insert(component)

    # ------------------------------------------------------------------
    def toggle(self, circuit_id: str, state: bool) -> bool:
        circuit = self.circuits.get(circuit_id)
        if not circuit:
            return False
        circuit.toggle(state)
        return True

    # ------------------------------------------------------------------
    def connect_device(self, circuit_id: str, device_id: str) -> None:
        self.connections[circuit_id] = device_id

    # ------------------------------------------------------------------
    def disconnect_device(self, circuit_id: str) -> None:
        self.connections.pop(circuit_id, None)

    # ------------------------------------------------------------------
    def tick(self) -> None:
        for circuit in self.circuits.values():
            if circuit.active and circuit.power > 0:
                usage = len(circuit.components)
                circuit.power = max(0, circuit.power - usage)
                if circuit.power == 0:
                    circuit.active = False


_CIRCUIT_SYSTEM = CircuitSystem()


def get_circuit_system() -> CircuitSystem:
    """Return the global circuit system instance."""

    return _CIRCUIT_SYSTEM
