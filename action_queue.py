import time
from typing import Dict

class ActionQueue:
    """Simple action queue per player to enforce a delay between actions."""

    def __init__(self, delay: float = 0.5):
        self.delay = delay
        self.next_time: Dict[str, float] = {}

    def can_act(self, player_id: str) -> bool:
        return time.time() >= self.next_time.get(player_id, 0.0)

    def record_action(self, player_id: str) -> None:
        self.next_time[player_id] = time.time() + self.delay
