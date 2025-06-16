from typing import Tuple
from events import publish
from .gas_sim import AtmosGrid


class HullBreachSystem:
    """Handle hull breaches causing rapid decompression."""

    def __init__(self, grid: AtmosGrid) -> None:
        self.grid = grid

    def breach(self, interior: Tuple[int, int], exterior: Tuple[int, int]) -> float:
        """Simulate a hull breach between two tiles."""
        diff = self.grid.explosive_decompress(interior, exterior)
        if diff:
            publish(
                "hull_breach",
                interior=interior,
                exterior=exterior,
                pressure_wave=diff,
            )
        return diff
