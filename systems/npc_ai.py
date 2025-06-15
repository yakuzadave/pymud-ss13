from __future__ import annotations

"""Simple NPC AI system."""

import logging
from typing import List

from world import get_world
from components.npc import NPCComponent

logger = logging.getLogger(__name__)


class NPCSystem:
    """Update NPCs and move them toward their goals."""

    def __init__(self) -> None:
        self.npc_ids: List[str] = []

    # ------------------------------------------------------------------
    def register(self, obj_id: str) -> None:
        if obj_id not in self.npc_ids:
            self.npc_ids.append(obj_id)

    # ------------------------------------------------------------------
    def start(self) -> None:  # placeholder for compatibility
        pass

    # ------------------------------------------------------------------
    def stop(self) -> None:
        pass

    # ------------------------------------------------------------------
    def update(self) -> None:
        world = get_world()
        for oid in list(self.npc_ids):
            obj = world.get_object(oid)
            if not obj:
                self.npc_ids.remove(oid)
                continue
            comp: NPCComponent = obj.get_component("npc")
            if not comp:
                continue
            comp.step()


_NPC_SYSTEM = NPCSystem()


def get_npc_system() -> NPCSystem:
    return _NPC_SYSTEM
