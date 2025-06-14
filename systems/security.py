"""Security and crime management system."""

import logging
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from events import publish

logger = logging.getLogger(__name__)


@dataclass
class CrimeRecord:
    """Represents a crime report."""

    crime_id: int
    reporter_id: str
    suspect_id: Optional[str]
    description: str
    severity: str
    evidence: List[str] = field(default_factory=list)
    status: str = "open"


@dataclass
class Prisoner:
    """Represents an incarcerated player."""

    player_id: str
    cell_id: Optional[str]
    release_time: float
    parole: bool = False


class SecuritySystem:
    """Tracks crimes, prisoners and security alerts."""

    def __init__(self) -> None:
        self._next_crime_id = 1
        self.crimes: Dict[int, CrimeRecord] = {}
        self.prisoners: Dict[str, Prisoner] = {}

    # ------------------------------------------------------------------
    def report_crime(
        self, reporter_id: str, description: str, suspect_id: Optional[str] = None, severity: str = "minor"
    ) -> CrimeRecord:
        """Record a new crime and return the record."""
        cid = self._next_crime_id
        self._next_crime_id += 1
        record = CrimeRecord(
            crime_id=cid,
            reporter_id=reporter_id,
            suspect_id=suspect_id,
            description=description,
            severity=severity,
        )
        self.crimes[cid] = record
        publish(
            "crime_reported",
            crime_id=cid,
            reporter_id=reporter_id,
            suspect_id=suspect_id,
            severity=severity,
        )
        logger.info(f"Crime reported {cid} by {reporter_id}")
        return record

    # ------------------------------------------------------------------
    def add_evidence(self, crime_id: int, evidence_desc: str) -> bool:
        record = self.crimes.get(crime_id)
        if not record:
            return False
        record.evidence.append(evidence_desc)
        publish("evidence_collected", crime_id=crime_id, description=evidence_desc)
        return True

    # ------------------------------------------------------------------
    def arrest(self, player_id: str, duration: float, cell_id: Optional[str] = None) -> Prisoner:
        """Arrest a player and add them to the prisoner database."""
        release_time = time.time() + duration
        prisoner = Prisoner(player_id=player_id, cell_id=cell_id, release_time=release_time)
        self.prisoners[player_id] = prisoner
        publish("player_arrested", player_id=player_id, cell_id=cell_id, duration=duration)
        logger.info(f"Player {player_id} arrested for {duration} seconds")
        return prisoner

    # ------------------------------------------------------------------
    def release(self, player_id: str) -> bool:
        prisoner = self.prisoners.pop(player_id, None)
        if not prisoner:
            return False
        publish("player_released", player_id=player_id)
        logger.info(f"Player {player_id} released from prison")
        return True

    # ------------------------------------------------------------------
    def check_sentence_expirations(self) -> None:
        """Release prisoners whose sentences have elapsed."""
        now = time.time()
        expired = [pid for pid, p in self.prisoners.items() if p.release_time <= now]
        for pid in expired:
            self.release(pid)


_SECURITY_SYSTEM = SecuritySystem()


def get_security_system() -> SecuritySystem:
    """Return the global security system instance."""
    return _SECURITY_SYSTEM

