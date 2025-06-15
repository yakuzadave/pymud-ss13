"""Advanced antagonist roles for MUDpy SS13.

This module introduces basic data structures for complex antagonist roles such
as cults, changelings, revolutionary cells, gangs and sleeper agents. The
systems here are intentionally lightweight and largely self contained so they
can evolve independently of the core AntagonistSystem.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
import random

from events import publish


# ---------------------------------------------------------------------------
# Data classes for individual antagonist role types
# ---------------------------------------------------------------------------


@dataclass
class Cult:
    """Simple representation of a cult."""

    name: str
    leader: str
    members: Set[str] = field(default_factory=set)

    def add_member(self, player_id: str) -> None:
        self.members.add(player_id)
        publish("cult_member_added", cult=self.name, player_id=player_id)

    def perform_ritual(self, ritual: str, participants: Set[str]) -> bool:
        if not participants.issubset(self.members | {self.leader}):
            return False
        publish(
            "cult_ritual_performed",
            cult=self.name,
            ritual=ritual,
            participants=list(participants),
        )
        return True


@dataclass
class Changeling:
    """Represents a shapeshifting antagonist."""

    player_id: str
    absorbed_dna: Dict[str, str] = field(default_factory=dict)
    abilities: Set[str] = field(default_factory=lambda: {"absorb"})

    def absorb_identity(self, target_id: str, dna_sample: str) -> None:
        self.absorbed_dna[target_id] = dna_sample
        publish("changeling_absorbed", player_id=self.player_id, target=target_id)

    def mimic_identity(self, target_id: str) -> bool:
        if target_id not in self.absorbed_dna:
            return False
        publish(
            "changeling_mimic",
            player_id=self.player_id,
            target=target_id,
        )
        return True


@dataclass
class RevolutionaryCell:
    """Group aiming to overthrow station leadership."""

    leader: str
    members: Set[str] = field(default_factory=set)
    propaganda: List[str] = field(default_factory=list)
    uprising: bool = False

    def recruit(self, player_id: str) -> None:
        self.members.add(player_id)
        publish("revolutionary_recruited", cell_leader=self.leader, player_id=player_id)

    def create_propaganda(self, text: str) -> None:
        self.propaganda.append(text)
        publish("revolutionary_propaganda", cell_leader=self.leader, text=text)


@dataclass
class Gang:
    """Territory based antagonist faction."""

    name: str
    members: Set[str] = field(default_factory=set)
    territory: Set[str] = field(default_factory=set)

    def add_member(self, player_id: str) -> None:
        self.members.add(player_id)
        publish("gang_member_added", gang=self.name, player_id=player_id)

    def claim_territory(self, area: str) -> None:
        self.territory.add(area)
        publish("gang_territory_claimed", gang=self.name, area=area)


@dataclass
class SleeperAgent:
    """Agent that activates later in the round."""

    player_id: str
    mission: Optional[str] = None
    activated: bool = False

    def assign_mission(self, mission: str) -> None:
        self.mission = mission
        publish("sleeper_mission_assigned", player_id=self.player_id, mission=mission)

    def activate(self) -> None:
        self.activated = True
        publish("sleeper_activated", player_id=self.player_id, mission=self.mission)


# ---------------------------------------------------------------------------
# Manager that keeps track of all advanced antagonist roles
# ---------------------------------------------------------------------------


class AdvancedAntagonistSystem:
    """Container for advanced antagonist role instances."""

    def __init__(self) -> None:
        self.cults: Dict[str, Cult] = {}
        self.changelings: Dict[str, Changeling] = {}
        self.cells: Dict[str, RevolutionaryCell] = {}
        self.gangs: Dict[str, Gang] = {}
        self.sleepers: Dict[str, SleeperAgent] = {}

    # Cult management -----------------------------------------------------
    def create_cult(self, name: str, leader: str) -> Cult:
        cult = Cult(name=name, leader=leader)
        self.cults[name] = cult
        publish("cult_created", cult=name, leader=leader)
        return cult

    def convert_to_cult(self, cult_name: str, player_id: str) -> bool:
        cult = self.cults.get(cult_name)
        if not cult:
            return False
        cult.add_member(player_id)
        return True

    # Changeling management -----------------------------------------------
    def spawn_changeling(self, player_id: str) -> Changeling:
        ling = Changeling(player_id=player_id)
        self.changelings[player_id] = ling
        publish("changeling_spawned", player_id=player_id)
        return ling

    # Revolutionary cell management --------------------------------------
    def create_cell(self, leader: str) -> RevolutionaryCell:
        cell = RevolutionaryCell(leader=leader)
        self.cells[leader] = cell
        publish("revolutionary_cell_created", leader=leader)
        return cell

    # Gang management -----------------------------------------------------
    def create_gang(self, name: str) -> Gang:
        gang = Gang(name=name)
        self.gangs[name] = gang
        publish("gang_created", gang=name)
        return gang

    # Sleeper agent management -------------------------------------------
    def assign_sleeper(
        self, player_id: str, mission: Optional[str] = None
    ) -> SleeperAgent:
        agent = SleeperAgent(player_id=player_id, mission=mission)
        self.sleepers[player_id] = agent
        publish("sleeper_assigned", player_id=player_id)
        return agent

    # Dynamic generation --------------------------------------------------
    def generate_antagonist_role(self, player_id: str) -> str:
        roles = ["cultist", "changeling", "revolutionary", "gangster", "sleeper"]
        role = random.choice(roles)
        publish("antagonist_role_generated", player_id=player_id, role=role)
        return role


_ADVANCED_ANTAGONIST_SYSTEM = AdvancedAntagonistSystem()


def get_advanced_antagonist_system() -> AdvancedAntagonistSystem:
    """Return the global advanced antagonist system instance."""

    return _ADVANCED_ANTAGONIST_SYSTEM
