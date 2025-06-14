"""
Player component for MUDpy SS13.
Represents a player character with inventory, stats, and abilities.
"""

from typing import Dict, List, Any, Optional
import logging
import threading
import time
from events import publish

logger = logging.getLogger(__name__)


class PlayerComponent:
    """
    Component that represents a player character.
    """

    def __init__(
        self,
        inventory: Optional[List[str]] = None,
        stats: Optional[Dict[str, float]] = None,
        access_level: int = 0,
        current_location: Optional[str] = None,
        role: str = "crew",
        abilities: Optional[List[str]] = None,
        body_parts: Optional[Dict[str, Dict[str, float]]] = None,
        diseases: Optional[List[str]] = None,
        skills: Optional[Dict[str, int]] = None,
    ):
        """
        Initialize the player component.

        Args:
            inventory (List[str], optional): List of item IDs in inventory.
            stats (Dict[str, float], optional): Player statistics.
            access_level (int): The player's security access level.
            current_location (str, optional): The ID of the player's current location.
        """
        self.owner = None
        self.inventory = inventory or []
        self._lock = threading.Lock()
        self.stats = stats or {
            "health": 100.0,
            "energy": 100.0,
            "oxygen": 100.0,
            "radiation": 0.0,
        }
        self.access_level = access_level
        self.current_location = current_location
        self.max_inventory_size = 10
        self.role = role
        self.abilities = abilities or self._default_role_abilities(role)
        self.equipment_slots = ["head", "body", "hands"]
        self.equipment: Dict[str, str] = {}
        self.move_speed = 1.0
        self.last_move_time = 0.0

        default_parts = {
            "head": {"brute": 0.0, "burn": 0.0, "toxin": 0.0, "oxygen": 0.0},
            "torso": {"brute": 0.0, "burn": 0.0, "toxin": 0.0, "oxygen": 0.0},
            "left_arm": {"brute": 0.0, "burn": 0.0, "toxin": 0.0, "oxygen": 0.0},
            "right_arm": {"brute": 0.0, "burn": 0.0, "toxin": 0.0, "oxygen": 0.0},
            "left_leg": {"brute": 0.0, "burn": 0.0, "toxin": 0.0, "oxygen": 0.0},
            "right_leg": {"brute": 0.0, "burn": 0.0, "toxin": 0.0, "oxygen": 0.0},
        }
        self.body_parts = body_parts or default_parts
        self.diseases = diseases or []
        self.skills: Dict[str, int] = skills or {}
        self.alive = True

    def add_to_inventory(self, item_id: str) -> bool:
        """
        Add an item to the player's inventory.

        Args:
            item_id (str): The ID of the item to add.

        Returns:
            bool: True if the item was added, False if inventory is full.
        """
        with self._lock:
            if len(self.inventory) >= self.max_inventory_size:
                return False
            self.inventory.append(item_id)
        logger.debug(f"Added item {item_id} to {self.owner.id}'s inventory")
        publish(
            "inventory_changed", player_id=self.owner.id, item_id=item_id, action="add"
        )

        return True

    def remove_from_inventory(self, item_id: str) -> bool:
        """
        Remove an item from the player's inventory.

        Args:
            item_id (str): The ID of the item to remove.

        Returns:
            bool: True if the item was removed, False if not found.
        """

        with self._lock:
            if item_id in self.inventory:
                self.inventory.remove(item_id)
            else:
                return False
        logger.debug(f"Removed item {item_id} from {self.owner.id}'s inventory")
        publish("inventory_changed", player_id=self.owner.id, item_id=item_id, action="remove")
        return True



    def has_item(self, item_id: str) -> bool:
        """
        Check if the player has an item in their inventory.

        Args:
            item_id (str): The ID of the item to check.

        Returns:
            bool: True if the player has the item, False otherwise.
        """
        return item_id in self.inventory

    def get_inventory_ids(self) -> List[str]:
        """
        Get the list of item IDs in the player's inventory.

        Returns:
            List[str]: List of item IDs.
        """
        return self.inventory.copy()

    def equip_item(self, item_id: str, slot: str) -> bool:
        """Equip an item from inventory into a slot."""
        if slot not in self.equipment_slots:
            return False
        with self._lock:
            if item_id not in self.inventory or slot in self.equipment:
                return False
            self.inventory.remove(item_id)
            self.equipment[slot] = item_id
        publish("inventory_changed", player_id=self.owner.id, item_id=item_id, action="equip")
        return True

    def unequip_item(self, slot: str) -> Optional[str]:
        """Unequip an item from a slot back to inventory."""
        if slot not in self.equipment:
            return None
        with self._lock:
            item_id = self.equipment.pop(slot)
            self.inventory.append(item_id)
        publish("inventory_changed", player_id=self.owner.id, item_id=item_id, action="unequip")
        return item_id

    def move_to(self, location_id: str) -> None:
        """
        Move the player to a new location.

        Args:
            location_id (str): The ID of the new location.
        """
        if time.time() - self.last_move_time < self.move_speed:
            return
        self.last_move_time = time.time()
        old_location = self.current_location
        self.current_location = location_id
        logger.debug(
            f"Moved player {self.owner.id} from {old_location} to {location_id}"
        )
        publish(
            "player_moved",
            player_id=self.owner.id,
            from_location=old_location,
            to_location=location_id,
        )

    def update_stat(self, stat_name: str, value: float) -> None:
        """
        Update a player statistic.

        Args:
            stat_name (str): The name of the stat to update.
            value (float): The amount to change the stat by (can be negative).
        """
        if stat_name in self.stats:
            old_value = self.stats[stat_name]
            self.stats[stat_name] += value

            # Ensure stats stay within reasonable ranges
            if stat_name == "radiation":
                self.stats[stat_name] = max(0, self.stats[stat_name])
            else:
                self.stats[stat_name] = max(0, min(100, self.stats[stat_name]))

            logger.debug(
                f"Updated {self.owner.id}'s {stat_name} from {old_value} to {self.stats[stat_name]}"
            )
            publish(
                "stat_changed",
                player_id=self.owner.id,
                stat=stat_name,
                old_value=old_value,
                new_value=self.stats[stat_name],
            )

    def apply_damage(self, body_part: str, damage_type: str, amount: float) -> None:
        """Apply damage to a body part."""
        part = self.body_parts.get(body_part)
        if not part or damage_type not in part:
            return
        old = part[damage_type]
        part[damage_type] = max(0.0, min(100.0, part[damage_type] + amount))
        if damage_type == "oxygen":
            self.update_stat("oxygen", -amount)
        else:
            self.update_stat("health", -amount)
        publish(
            "damage_applied",
            player_id=self.owner.id,
            part=body_part,
            damage_type=damage_type,
            old_value=old,
            new_value=part[damage_type],
        )
        if self.stats.get("health", 0) <= 0 and self.alive:
            self.alive = False
            publish("player_dead", player_id=self.owner.id)

    def heal_damage(self, body_part: str, damage_type: str, amount: float) -> None:
        """Heal damage on a body part."""
        part = self.body_parts.get(body_part)
        if not part or damage_type not in part:
            return
        old = part[damage_type]
        part[damage_type] = max(0.0, part[damage_type] - amount)
        if damage_type == "oxygen":
            self.update_stat("oxygen", amount)
        else:
            self.update_stat("health", amount)
        publish(
            "damage_healed",
            player_id=self.owner.id,
            part=body_part,
            damage_type=damage_type,
            old_value=old,
            new_value=part[damage_type],
        )
        if self.stats.get("health", 0) > 0 and not self.alive:
            self.alive = True
            publish("player_revived", player_id=self.owner.id)

    def contract_disease(self, disease: str) -> None:
        if disease not in self.diseases:
            self.diseases.append(disease)
            publish("disease_contracted", player_id=self.owner.id, disease=disease)

    def cure_disease(self, disease: str) -> None:
        if disease in self.diseases:
            self.diseases.remove(disease)
            publish("disease_cured", player_id=self.owner.id, disease=disease)

    def apply_environmental_effects(
        self, room_atmosphere: Dict[str, float], hazards: List[str]
    ) -> List[str]:
            logger.debug(f"Updated {self.owner.id}'s {stat_name} from {old_value} to {self.stats[stat_name]}")
            publish("stat_changed", player_id=self.owner.id, stat=stat_name, old_value=old_value, new_value=self.stats[stat_name])

    def breathe(self, room_comp: "RoomComponent", amount: float = 0.1) -> None:
        """Simulate the player breathing in a room.

        Oxygen is removed from the room atmosphere and converted to CO2.
        The player's oxygen stat is adjusted based on the remaining oxygen
        percentage in the room.

        Args:
            room_comp: The room component representing the current location.
            amount: Amount of oxygen consumed each tick.
        """
        atmos = getattr(room_comp, "atmosphere", None)
        if atmos is None and hasattr(room_comp, "gas"):
            atmos = room_comp.gas.composition
        if atmos is None:
            return
        available = atmos.get("oxygen", 0.0)
        consumed = min(amount, available)
        atmos["oxygen"] = max(0.0, available - consumed)
        atmos["co2"] = atmos.get("co2", 0.0) + consumed

        if atmos.get("oxygen", 21.0) < 10.0:
            self.update_stat("oxygen", -1.0)
        else:
            if self.stats.get("oxygen", 0) < 100.0:
                self.update_stat("oxygen", 0.5)

    def apply_environmental_effects(self, room_atmosphere: Dict[str, float], hazards: List[str]) -> List[str]:

        """
        Apply environmental effects to the player based on room conditions.

        Args:
            room_atmosphere (Dict[str, float]): Atmospheric conditions in the room.
            hazards (List[str]): Hazards present in the room.

        Returns:
            List[str]: Messages describing the effects.
        """
        messages = []

        # Check oxygen level
        if room_atmosphere.get("oxygen", 21.0) < 10.0:
            self.update_stat("oxygen", -2.0)
            if self.stats["oxygen"] < 50:
                messages.append(
                    "You're having trouble breathing in the low-oxygen environment."
                )

        # Check radiation
        if "radiation" in hazards:
            radiation_increase = 1.0
            # Check if player has radiation protection
            if self.has_radiation_protection():
                radiation_increase = 0.2
                messages.append("Your radiation suit provides some protection.")

            self.update_stat("radiation", radiation_increase)
            if self.stats["radiation"] > 50:
                messages.append("Warning: High radiation levels detected.")
                # Radiation also affects health
                self.update_stat("health", -1.0)

        # Check extreme pressure
        if room_atmosphere.get("pressure", 101.3) > 150:
            self.update_stat("health", -1.0)
            messages.append("The high pressure is causing discomfort.")

        # Check extreme temperature
        if "extreme_heat" in hazards:
            self.update_stat("health", -1.5)
            messages.append("The extreme heat is damaging.")

        if "electrical" in hazards:
            self.update_stat("health", -5.0)
            messages.append("Sparks arc across your body, shocking you.")

        # Apply any other hazard effects
        if "toxic_gas" in hazards:
            self.update_stat("health", -2.0)
            messages.append("You cough as the toxic gas irritates your lungs.")

        return messages

    def _equipment_has_property(self, prop: str) -> bool:
        from world import get_world

        w = get_world()
        item_ids = list(self.equipment.values()) + self.inventory
        for item_id in item_ids:
            obj = w.get_object(item_id)
            if not obj:
                continue
            comp = obj.get_component("item")
            if comp and comp.item_properties.get(prop):
                return True
        return False

    def has_radiation_protection(self) -> bool:
        return self._equipment_has_property("radiation_protection")

    def has_vacuum_protection(self) -> bool:
        return self._equipment_has_property("vacuum_protection")

    def has_thermal_protection(self) -> bool:
        return self._equipment_has_property("thermal_protection")

    def get_access_card_level(self) -> int:
        """
        Get the highest access card level from the player's inventory.

        Returns:
            int: The highest access level found, or the player's base level.
        """
        # This is a placeholder implementation
        # In a real game, you'd check item properties of keycards in inventory
        return self.access_level

    def _default_role_abilities(self, role: str) -> List[str]:
        mapping = {
            "engineer": ["repair_power", "fix_leak"],
            "doctor": ["heal"],
            "security": ["restrain"],
            "chemist": ["mix"],
        }
        return mapping.get(role.lower(), [])

    def has_ability(self, ability: str) -> bool:
        return ability in self.abilities

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert this component to a dictionary for serialization.

        Returns:
            Dict[str, Any]: Dictionary representation of this component.
        """
        return {
            "inventory": self.inventory,
            "stats": self.stats,
            "access_level": self.access_level,
            "current_location": self.current_location,
            "max_inventory_size": self.max_inventory_size,
            "role": self.role,
            "abilities": self.abilities,
            "equipment": self.equipment,
            "body_parts": self.body_parts,
            "diseases": self.diseases,
            "skills": self.skills,
            "alive": self.alive,
        }
