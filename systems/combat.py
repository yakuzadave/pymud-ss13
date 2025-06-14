"""Simple combat system with weapons and armor."""

from dataclasses import dataclass
from typing import Dict, Optional

from events import publish
from world import get_world


@dataclass
class Armor:
    protection: float  # percentage reduction 0-1
    durability: float = 100.0
    coverage: Optional[str] = None  # body part


@dataclass
class Weapon:
    damage: float
    weapon_type: str  # "melee" or "ballistic"
    range: int = 1
    penetration: float = 0.0  # ignore armor percentage
    ammo_capacity: int = 0
    ammo: int = 0


class CombatSystem:
    """Very simple combat system for applying damage."""

    def __init__(self) -> None:
        self.armors: Dict[str, Armor] = {}
        self.weapons: Dict[str, Weapon] = {}

    # ------------------------------------------------------------------
    def register_weapon(self, obj_id: str, weapon: Weapon) -> None:
        self.weapons[obj_id] = weapon

    # ------------------------------------------------------------------
    def register_armor(self, obj_id: str, armor: Armor) -> None:
        self.armors[obj_id] = armor

    # ------------------------------------------------------------------
    def attack(self, attacker_id: str, defender_id: str, weapon_id: str) -> None:
        world = get_world()
        attacker = world.get_object(attacker_id)
        defender = world.get_object(defender_id)
        if not attacker or not defender:
            return
        weapon = self.weapons.get(weapon_id)
        if not weapon:
            return
        dmg = weapon.damage
        armor = self.armors.get(defender_id)
        if armor and armor.coverage == "body":
            dmg *= max(0.0, 1.0 - armor.protection + weapon.penetration)
            armor.durability = max(0.0, armor.durability - dmg)
        dcomp = defender.get_component("player")
        if dcomp:
            dcomp.apply_damage("torso", "brute", dmg)
        publish("attack", attacker=attacker_id, defender=defender_id, damage=dmg)


COMBAT_SYSTEM = CombatSystem()


def get_combat_system() -> CombatSystem:
    return COMBAT_SYSTEM
