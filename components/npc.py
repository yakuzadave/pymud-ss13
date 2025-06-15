"""
NPC component for MUDpy SS13.
Represents a non-player character with a role and optional dialogue.
"""

from typing import List, Optional, Dict, Any

from pathfinding import find_path
from world import get_world
import logging

logger = logging.getLogger(__name__)


class NPCComponent:
    """Component representing an NPC in the game world."""

    def __init__(self, role: str = "crew", dialogue: Optional[List[str]] = None):
        self.owner = None
        self.role = role
        self.dialogue = dialogue or []
        self.goal: Optional[str] = None
        self.path: List[str] = []

    def to_dict(self) -> Dict[str, Any]:
        """Convert this component to a serializable dict."""

        return {
            "role": self.role,
            "dialogue": self.dialogue,
            "goal": self.goal,
        }

    # ------------------------------------------------------------------
    def set_goal(self, room_id: str) -> None:
        """Set a target room for the NPC."""

        self.goal = room_id
        self.path.clear()

    # ------------------------------------------------------------------
    def compute_path(self) -> None:
        """Compute a path toward the current goal."""

        if not self.goal or not self.owner or not self.owner.location:
            self.path = []
            return
        world = get_world()
        self.path = find_path(world, self.owner.location, self.goal)
        if self.path and self.path[0] == self.owner.location:
            self.path = self.path[1:]

    # ------------------------------------------------------------------
    def step(self) -> None:
        """Move one step along the computed path if available."""

        if not self.path and self.goal:
            self.compute_path()
        if not self.path:
            return
        next_room = self.path.pop(0)
        self.owner.move_to(next_room)
        if not self.path:
            self.goal = None
