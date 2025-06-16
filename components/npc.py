"""
NPC component for MUDpy SS13.
Represents a non-player character with a role and optional dialogue.
"""

from typing import List, Optional, Dict, Any
import random
from events import publish, subscribe

from pathfinding import find_path
from world import get_world
import logging

logger = logging.getLogger(__name__)


class NPCComponent:
    """Component representing an NPC in the game world."""

    def __init__(
        self,
        role: str = "crew",
        dialogue: Optional[List[str]] = None,
        routine: Optional[List[str]] = None,
        event_dialogue: Optional[Dict[str, List[str]]] = None,
    ):
        self.owner = None
        self.role = role
        self.dialogue = dialogue or []
        self.routine = routine or []
        self._routine_index = 0
        self.event_dialogue = event_dialogue or {}
        self.pending_lines: List[str] = []
        self.goal: Optional[str] = None
        self.path: List[str] = []

    def on_added(self) -> None:
        """Subscribe to relevant events when added to the world."""
        subscribe("random_event", self._on_random_event)
        for evt in self.event_dialogue.keys():
            subscribe(evt, self._make_event_handler(evt))

    # ------------------------------------------------------------------
    def _make_event_handler(self, event_name: str):
        return lambda **kwargs: self._on_specific_event(event_name)

    def _on_specific_event(self, event_name: str) -> None:
        self.queue_event_dialogue(event_name)

    def _on_random_event(self, event_id: str, **kwargs: Any) -> None:
        self.queue_event_dialogue(event_id)

    def queue_event_dialogue(self, event_id: str) -> None:
        lines = self.event_dialogue.get(event_id)
        if lines:
            self.pending_lines.append(random.choice(lines))

    def maybe_chat(self) -> None:
        """Output queued lines or random idle chatter."""
        if self.owner is None or not self.owner.location:
            return
        if self.pending_lines:
            line = self.pending_lines.pop(0)
            publish(
                "npc_said",
                npc_id=self.owner.id,
                location=self.owner.location,
                message=line,
                name=self.owner.name,
            )
            return
        if self.dialogue and random.random() < 0.05:
            line = random.choice(self.dialogue)
            publish(
                "npc_said",
                npc_id=self.owner.id,
                location=self.owner.location,
                message=line,
                name=self.owner.name,
            )

    def to_dict(self) -> Dict[str, Any]:
        """Convert this component to a serializable dict."""

        return {
            "role": self.role,
            "dialogue": self.dialogue,
            "routine": self.routine,
            "event_dialogue": self.event_dialogue,
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
        if not self.path and not self.goal and self.routine:
            self.set_goal(self.routine[self._routine_index])
            self._routine_index = (self._routine_index + 1) % len(self.routine)
            self.compute_path()
        if self.path:
            next_room = self.path.pop(0)
            self.owner.move_to(next_room)
            if not self.path:
                self.goal = None
        self.maybe_chat()
