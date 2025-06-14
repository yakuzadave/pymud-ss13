from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Iterable, Optional


@dataclass
class SpatialGrid:
    """Simple tile-based grid to track object positions."""

    tiles: Dict[Tuple[int, int], List[str]] = field(default_factory=dict)
    positions: Dict[str, Tuple[int, int]] = field(default_factory=dict)

    def add_object(self, obj_id: str, x: int, y: int) -> None:
        self.positions[obj_id] = (x, y)
        self.tiles.setdefault((x, y), []).append(obj_id)

    def move_object(self, obj_id: str, x: int, y: int) -> None:
        old = self.positions.get(obj_id)
        if old:
            if obj_id in self.tiles.get(old, []):
                self.tiles[old].remove(obj_id)
                if not self.tiles[old]:
                    del self.tiles[old]
        self.add_object(obj_id, x, y)

    def remove_object(self, obj_id: str) -> None:
        pos = self.positions.pop(obj_id, None)
        if pos and obj_id in self.tiles.get(pos, []):
            self.tiles[pos].remove(obj_id)
            if not self.tiles[pos]:
                del self.tiles[pos]

    def objects_at(self, x: int, y: int) -> List[str]:
        return list(self.tiles.get((x, y), []))

    def objects_near(self, x: int, y: int, radius: float) -> List[str]:
        result = []
        r2 = radius * radius
        for obj_id, pos in self.positions.items():
            dx = pos[0] - x
            dy = pos[1] - y
            if dx * dx + dy * dy <= r2:
                result.append(obj_id)
        return result

    def line_of_sight(self, start: Tuple[int, int], end: Tuple[int, int], opaque: Optional[Iterable[str]] = None) -> bool:
        """Simple Bresenham line check; returns False if an opaque object blocks."""
        opaque = set(opaque or [])
        x0, y0 = start
        x1, y1 = end
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            if (x0, y0) != start and (x0, y0) != end:
                for obj in self.tiles.get((x0, y0), []):
                    if obj in opaque:
                        return False
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy
        return True
