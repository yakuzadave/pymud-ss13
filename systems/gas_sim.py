"""Simple atmospheric simulation core for MUDpy SS13.

This module provides a basic gas mixture representation, a tile
based atmosphere grid and a minimal pipe network.  It is intentionally
lightweight but serves as a foundation for more advanced simulation
in the future.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple, Optional, Iterable


@dataclass
class GasMixture:
    """Representation of a gas mixture."""

    pressure: float = 101.3
    temperature: float = 20.0
    composition: Dict[str, float] = field(
        default_factory=lambda: {
            "oxygen": 21.0,
            "nitrogen": 78.0,
            "co2": 0.04,
            "smoke": 0.0,
        }
    )

    def copy(self) -> "GasMixture":
        return GasMixture(
            pressure=self.pressure,
            temperature=self.temperature,
            composition=dict(self.composition),
        )

    def add_gas(self, gas: str, amount: float) -> None:
        self.composition[gas] = self.composition.get(gas, 0.0) + amount

    def remove_gas(self, gas: str, amount: float) -> float:
        current = self.composition.get(gas, 0.0)
        removed = min(current, amount)
        if removed > 0:
            self.composition[gas] = current - removed
        return removed

    def mix(self, other: "GasMixture", ratio: float) -> None:
        """Mix another mixture into this one."""
        ratio = max(0.0, min(1.0, ratio))
        for gas in set(self.composition) | set(other.composition):
            a = self.composition.get(gas, 0.0)
            b = other.composition.get(gas, 0.0)
            self.composition[gas] = a * (1 - ratio) + b * ratio
        self.pressure = self.pressure * (1 - ratio) + other.pressure * ratio
        self.temperature = self.temperature * (1 - ratio) + other.temperature * ratio


@dataclass
class AtmosTile:
    """Single tile of the atmosphere grid."""

    x: int
    y: int
    gas: GasMixture = field(default_factory=GasMixture)


class AtmosGrid:
    """Tile-based grid for atmospheric simulation."""

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.tiles: Dict[Tuple[int, int], AtmosTile] = {}
        for x in range(width):
            for y in range(height):
                self.tiles[(x, y)] = AtmosTile(x, y)

    def get_tile(self, x: int, y: int) -> Optional[AtmosTile]:
        return self.tiles.get((x, y))

    def neighbours(self, tile: AtmosTile) -> Iterable[AtmosTile]:
        offsets = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        for dx, dy in offsets:
            n = self.get_tile(tile.x + dx, tile.y + dy)
            if n:
                yield n

    def step(self, rate: float = 0.25) -> None:
        """Advance the simulation one tick."""
        exchanges: Dict[Tuple[int, int], GasMixture] = {}
        for tile in self.tiles.values():
            for nbr in self.neighbours(tile):
                if tile.gas.pressure <= nbr.gas.pressure:
                    continue
                diff = tile.gas.pressure - nbr.gas.pressure
                flow = diff * rate
                if flow <= 0:
                    continue
                ratio = flow / tile.gas.pressure if tile.gas.pressure else 0
                exchange = tile.gas.copy()
                exchange.pressure = flow
                tile.gas.pressure -= flow
                for gas in exchange.composition:
                    exchange.composition[gas] *= ratio
                    tile.gas.composition[gas] -= exchange.composition[gas]
                key = (nbr.x, nbr.y)
                if key not in exchanges:
                    exchanges[key] = exchange
                else:
                    # accumulate
                    ex = exchanges[key]
                    ex.mix(
                        exchange, exchange.pressure / (ex.pressure + exchange.pressure)
                    )
                    ex.pressure += exchange.pressure
        for key, mix in exchanges.items():
            tile = self.tiles[key]
            total = tile.gas.pressure + mix.pressure
            if total == 0:
                continue
            ratio = mix.pressure / total
            tile.gas.mix(mix, ratio)
            tile.gas.pressure = total

    def explosive_decompress(self, src: Tuple[int, int], dst: Tuple[int, int]) -> float:
        """Instantly equalize pressure between two tiles and return pressure wave magnitude."""
        s = self.get_tile(*src)
        d = self.get_tile(*dst)
        if not s or not d:
            return 0.0
        diff = s.gas.pressure - d.gas.pressure
        if abs(diff) < 20:
            return 0.0
        avg = (s.gas.pressure + d.gas.pressure) / 2
        s.gas.pressure = avg
        d.gas.pressure = avg
        return abs(diff)


@dataclass
class Pipe:
    src: Tuple[int, int]
    dst: Tuple[int, int]
    rate: float = 1.0
    active: bool = True


class PipeNetwork:
    """Simple network of pipes for moving gas."""

    def __init__(self, grid: AtmosGrid) -> None:
        self.grid = grid
        self.pipes: Dict[Tuple[int, int, int, int], Pipe] = {}

    def add_pipe(
        self, src: Tuple[int, int], dst: Tuple[int, int], rate: float = 1.0
    ) -> None:
        self.pipes[(src[0], src[1], dst[0], dst[1])] = Pipe(src, dst, rate)

    def step(self) -> None:
        for pipe in self.pipes.values():
            if not pipe.active:
                continue
            src_tile = self.grid.get_tile(*pipe.src)
            dst_tile = self.grid.get_tile(*pipe.dst)
            if not src_tile or not dst_tile:
                continue
            flow = min(pipe.rate, src_tile.gas.pressure)
            if flow <= 0:
                continue
            ratio = flow / src_tile.gas.pressure if src_tile.gas.pressure else 0
            transfer = src_tile.gas.copy()
            transfer.pressure = flow
            for gas in transfer.composition:
                transfer.composition[gas] *= ratio
                src_tile.gas.composition[gas] -= transfer.composition[gas]
            src_tile.gas.pressure -= flow
            total = dst_tile.gas.pressure + flow
            mix_ratio = flow / total if total else 0
            dst_tile.gas.mix(transfer, mix_ratio)
            dst_tile.gas.pressure = total
