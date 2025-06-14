"""Structure component representing walls and floors."""

from typing import Dict, Any
from events import publish
import logging

logger = logging.getLogger(__name__)

class StructureComponent:
    """Component for station structures like walls and floors."""

    def __init__(self,
                 kind: str = "wall",
                 integrity: int = 100,
                 is_destructible: bool = True,
                 is_constructible: bool = True):
        self.owner = None
        self.kind = kind
        self.integrity = max(0, min(100, integrity))
        self.is_destructible = is_destructible
        self.is_constructible = is_constructible

    def damage(self, amount: int) -> bool:
        """Damage the structure, returning True if destroyed."""
        if not self.is_destructible or amount <= 0:
            return False
        old = self.integrity
        self.integrity = max(0, self.integrity - amount)
        logger.debug(f"Damaged {self.owner.id if self.owner else 'structure'} from {old} to {self.integrity}")
        if self.integrity == 0:
            publish("structure_destroyed", structure_id=self.owner.id if self.owner else None)
            return True
        return False

    def repair(self, amount: int) -> None:
        """Repair the structure if constructible."""
        if not self.is_constructible or amount <= 0:
            return
        old = self.integrity
        self.integrity = min(100, self.integrity + amount)
        logger.debug(f"Repaired {self.owner.id if self.owner else 'structure'} from {old} to {self.integrity}")
        if old == 0 and self.integrity > 0:
            publish("structure_rebuilt", structure_id=self.owner.id if self.owner else None)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "kind": self.kind,
            "integrity": self.integrity,
            "is_destructible": self.is_destructible,
            "is_constructible": self.is_constructible,
        }
