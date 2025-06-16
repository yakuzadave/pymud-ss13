"""Medical equipment and utilities."""

import logging
from typing import Dict, Any

from events import publish

logger = logging.getLogger(__name__)


class MedicalScannerComponent:
    """Component that records vital signs and body part damage."""

    def __init__(self) -> None:
        self.owner = None
        self.records: Dict[str, Dict[str, Any]] = {}

    def scan_player(self, player_comp) -> Dict[str, Any]:
        """Record vitals and injuries from ``player_comp``."""
        stats = dict(player_comp.stats)
        damage = {part: dict(vals) for part, vals in player_comp.body_parts.items()}
        record = {"stats": stats, "damage": damage}
        self.records[player_comp.owner.id] = record
        publish(
            "medical_scanned",
            scanner_id=self.owner.id if self.owner else None,
            patient_id=player_comp.owner.id,
        )
        return record

    def to_dict(self) -> Dict[str, Any]:
        return {"records": self.records}
