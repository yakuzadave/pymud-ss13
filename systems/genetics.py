"""Simple genetics system for handling mutations and DNA profiles."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import logging

from events import publish

logger = logging.getLogger(__name__)


@dataclass
class GeneticProfile:
    """Genetic traits and mutation tracking for a player."""

    genes: Dict[str, int] = field(default_factory=dict)
    mutations: List[str] = field(default_factory=list)
    instability: float = 0.0

    def add_gene(self, gene: str, value: int) -> None:
        self.genes[gene] = value
        logger.debug("Gene %s set to %s", gene, value)

    def apply_mutation(self, mutation: str, severity: float) -> None:
        if mutation not in self.mutations:
            self.mutations.append(mutation)
        self.instability += severity
        logger.debug("Applied mutation %s (severity %.2f)", mutation, severity)

    def stabilize(self, amount: float) -> None:
        self.instability = max(0.0, self.instability - amount)
        logger.debug("Stability improved by %.2f", amount)
        if self.instability == 0:
            self.mutations.clear()

    def tick(self) -> None:
        if self.instability <= 0:
            return
        self.instability = max(0.0, self.instability - 0.1)
        if self.instability == 0:
            self.mutations.clear()
            logger.debug("Mutations cleared due to stability")


class GeneticsSystem:
    """Manage DNA profiles and genetic experimentation."""

    def __init__(self) -> None:
        self.profiles: Dict[str, GeneticProfile] = {}
        self.scanned_dna: Dict[str, GeneticProfile] = {}
        logger.info("Genetics system initialized")

    def get_profile(self, player_id: str) -> GeneticProfile:
        profile = self.profiles.setdefault(player_id, GeneticProfile())
        return profile

    def scan_dna(self, player_id: str, target_id: str) -> Optional[GeneticProfile]:
        target = self.profiles.get(target_id)
        if not target:
            return None
        copy = GeneticProfile(genes=dict(target.genes), mutations=list(target.mutations), instability=target.instability)
        self.scanned_dna[player_id] = copy
        publish("dna_scanned", scanner=player_id, target=target_id)
        logger.debug("%s scanned DNA from %s", player_id, target_id)
        return copy

    def apply_scanned_dna(self, player_id: str) -> bool:
        data = self.scanned_dna.get(player_id)
        if not data:
            return False
        self.profiles[player_id] = GeneticProfile(genes=dict(data.genes), mutations=list(data.mutations), instability=data.instability)
        publish("dna_applied", player=player_id)
        logger.debug("Applied scanned DNA to %s", player_id)
        return True

    def mutate_player(self, player_id: str, mutation: str, severity: float = 1.0) -> None:
        profile = self.get_profile(player_id)
        profile.apply_mutation(mutation, severity)
        publish("player_mutated", player=player_id, mutation=mutation)

    def stabilize_player(self, player_id: str, amount: float = 0.5) -> None:
        profile = self.get_profile(player_id)
        profile.stabilize(amount)
        publish("genetic_stabilized", player=player_id, amount=amount)

    def tick(self) -> None:
        for profile in self.profiles.values():
            profile.tick()


_GENETICS_SYSTEM = GeneticsSystem()


def get_genetics_system() -> GeneticsSystem:
    return _GENETICS_SYSTEM
