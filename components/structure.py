"""Structure component representing walls and floors."""

from typing import Dict, Any
from events import publish
import logging
from systems.physics import MATERIALS, Material

logger = logging.getLogger(__name__)


class StructureComponent:
    """Component for station structures like walls and floors."""

    def __init__(
        self,
        kind: str = "wall",
        integrity: int = 100,
        is_destructible: bool = True,
        is_constructible: bool = True,
        material: str = "steel",
    ):
        self.owner = None
        self.kind = kind
        self.integrity = max(0, min(100, integrity))
        self.is_destructible = is_destructible
        self.is_constructible = is_constructible
        self.material_name = material
        self.material: Material = MATERIALS.get(material, MATERIALS["steel"])

    def apply_environment(self, pressure: float, temperature: float) -> None:
        """Apply environmental factors and reduce integrity accordingly."""
        damage = 0
        if pressure > self.material.yield_strength:
            damage += int(pressure - self.material.yield_strength)
        if temperature > self.material.heat_resistance:
            damage += int((temperature - self.material.heat_resistance) / 10)
        if damage > 0:
            self.damage(damage)

    def damage(self, amount: int) -> bool:
        """Damage the structure, returning True if destroyed."""
        if not self.is_destructible or amount <= 0:
            return False
        old = self.integrity
        self.integrity = max(0, self.integrity - amount)
        logger.debug(
            f"Damaged {self.owner.id if self.owner else 'structure'} from {old} to {self.integrity}"
        )
        if self.integrity == 0:
            publish(
                "structure_destroyed",
                structure_id=self.owner.id if self.owner else None,
            )
            return True
        return False

    def repair(self, amount: int) -> None:
        """Repair the structure if constructible."""
        if not self.is_constructible or amount <= 0:
            return
        old = self.integrity
        self.integrity = min(100, self.integrity + amount)
        logger.debug(
            f"Repaired {self.owner.id if self.owner else 'structure'} from {old} to {self.integrity}"
        )
        if old == 0 and self.integrity > 0:
            publish(
                "structure_rebuilt", structure_id=self.owner.id if self.owner else None
            )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "kind": self.kind,
            "integrity": self.integrity,
            "is_destructible": self.is_destructible,
            "is_constructible": self.is_constructible,
            "material": self.material_name,
        }
