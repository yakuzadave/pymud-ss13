"""Antagonist management system for MUDpy SS13."""

import random
import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any

from events import publish

logger = logging.getLogger(__name__)


@dataclass
class Antagonist:
    """Represents a player assigned as an antagonist."""

    player_id: str
    role: str = "traitor"
    objectives: List[str] = field(default_factory=list)
    gear: List[str] = field(default_factory=list)
    completed: bool = False


class AntagonistSystem:
    """System that tracks antagonists and their objectives."""

    def __init__(self) -> None:
        self.antagonists: Dict[str, Antagonist] = {}

    # ------------------------------------------------------------------
    def assign_antagonist(
        self,
        player_id: str,
        role: str = "traitor",
        objectives: Optional[List[str]] = None,
        gear: Optional[List[str]] = None,
    ) -> Antagonist:
        """Assign a player as an antagonist."""
        antag = Antagonist(
            player_id=player_id,
            role=role,
            objectives=objectives or [],
            gear=gear or [],
        )
        self.antagonists[player_id] = antag
        publish(
            "antagonist_assigned",
            player_id=player_id,
            role=role,
            objectives=antag.objectives,
        )
        return antag

    # ------------------------------------------------------------------
    def remove_antagonist(self, player_id: str) -> bool:
        """Remove an antagonist assignment."""
        antag = self.antagonists.pop(player_id, None)
        if not antag:
            return False
        publish("antagonist_removed", player_id=player_id, role=antag.role)
        return True

    # ------------------------------------------------------------------
    def list_antagonists(self) -> List[Antagonist]:
        return list(self.antagonists.values())

    # ------------------------------------------------------------------
    def complete_objective(self, player_id: str, objective: str) -> None:
        """Mark an objective as completed for a player."""
        antag = self.antagonists.get(player_id)
        if not antag:
            return
        if objective in antag.objectives:
            antag.objectives.remove(objective)
            if not antag.objectives:
                antag.completed = True
                publish(
                    "antagonist_objectives_completed",
                    player_id=player_id,
                    role=antag.role,
                )

    # ------------------------------------------------------------------
    def choose_random_antagonists(
        self,
        player_ids: List[str],
        count: int = 1,
        objectives: Optional[List[str]] = None,
        gear: Optional[List[str]] = None,
    ) -> List[str]:
        """Randomly select players to become antagonists."""
        if not player_ids or count <= 0:
            return []
        chosen = random.sample(player_ids, min(count, len(player_ids)))
        for pid in chosen:
            self.assign_antagonist(pid, "traitor", objectives, gear)
        publish("antagonists_selected", player_ids=chosen)
        return chosen

    # ------------------------------------------------------------------
    def round_end_check(self) -> Dict[str, Any]:
        """Check round win/loss conditions."""
        winners = [a.player_id for a in self.antagonists.values() if a.completed]
        publish("round_end", winners=winners, antagonists=self.antagonists)
        return {"winners": winners}


_ANTAGONIST_SYSTEM = AntagonistSystem()


def get_antagonist_system() -> AntagonistSystem:
    """Return the global antagonist system instance."""
    return _ANTAGONIST_SYSTEM
