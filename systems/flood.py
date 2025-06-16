from typing import Dict
from components.player import PlayerComponent


class FloodSystem:
    """Manage water levels in rooms and slow player movement when flooded."""

    def __init__(self) -> None:
        self.levels: Dict[str, float] = {}

    def add_water(self, room_id: str, amount: float = 0.1) -> None:
        level = self.levels.get(room_id, 0.0) + amount
        self.levels[room_id] = min(1.0, level)

    def remove_water(self, room_id: str, amount: float = 0.1) -> None:
        level = max(0.0, self.levels.get(room_id, 0.0) - amount)
        if level == 0.0:
            self.levels.pop(room_id, None)
        else:
            self.levels[room_id] = level

    def get_level(self, room_id: str) -> float:
        return self.levels.get(room_id, 0.0)

    def affect_player(self, player: PlayerComponent, room_id: str) -> None:
        level = self.levels.get(room_id, 0.0)
        player.move_speed = 2.0 if level > 0.5 else 1.0
