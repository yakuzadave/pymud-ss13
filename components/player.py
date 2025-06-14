"""
Player component for MUDpy SS13.
Represents a player character with inventory, stats, and abilities.
"""

from typing import Dict, List, Any, Optional
import logging
from events import publish

logger = logging.getLogger(__name__)

class PlayerComponent:
    """
    Component that represents a player character.
    """

    def __init__(self,
                 inventory: Optional[List[str]] = None,
                 stats: Optional[Dict[str, float]] = None,
                 access_level: int = 0,
                 current_location: Optional[str] = None,
                 role: str = "crew",
                 abilities: Optional[List[str]] = None):
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
        self.stats = stats or {
            "health": 100.0,
            "energy": 100.0,
            "oxygen": 100.0,
            "radiation": 0.0
        }
        self.access_level = access_level
        self.current_location = current_location
        self.max_inventory_size = 10
        self.role = role
        self.abilities = abilities or self._default_role_abilities(role)

    def add_to_inventory(self, item_id: str) -> bool:
        """
        Add an item to the player's inventory.

        Args:
            item_id (str): The ID of the item to add.

        Returns:
            bool: True if the item was added, False if inventory is full.
        """
        if len(self.inventory) >= self.max_inventory_size:
            return False

        self.inventory.append(item_id)
        logger.debug(f"Added item {item_id} to {self.owner.id}'s inventory")
        publish("inventory_changed", player_id=self.owner.id, item_id=item_id, action="add")

        return True

    def remove_from_inventory(self, item_id: str) -> bool:
        """
        Remove an item from the player's inventory.

        Args:
            item_id (str): The ID of the item to remove.

        Returns:
            bool: True if the item was removed, False if not found.
        """
        if item_id in self.inventory:
            self.inventory.remove(item_id)
            logger.debug(f"Removed item {item_id} from {self.owner.id}'s inventory")
            publish("inventory_changed", player_id=self.owner.id, item_id=item_id, action="remove")
            return True
        return False

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

    def move_to(self, location_id: str) -> None:
        """
        Move the player to a new location.

        Args:
            location_id (str): The ID of the new location.
        """
        old_location = self.current_location
        self.current_location = location_id
        logger.debug(f"Moved player {self.owner.id} from {old_location} to {location_id}")
        publish("player_moved", player_id=self.owner.id, from_location=old_location, to_location=location_id)

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

            logger.debug(f"Updated {self.owner.id}'s {stat_name} from {old_value} to {self.stats[stat_name]}")
            publish("stat_changed", player_id=self.owner.id, stat=stat_name, old_value=old_value, new_value=self.stats[stat_name])

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
                messages.append("You're having trouble breathing in the low-oxygen environment.")

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

    def has_radiation_protection(self) -> bool:
        """
        Check if the player has radiation protection.
        This would check for hazmat suits or similar items in inventory.

        Returns:
            bool: True if protected, False otherwise.
        """
        # This is a placeholder implementation
        # In a real game, you'd check for specific items or equipment
        return "hazmat_suit" in self.inventory or "rad_suit" in self.inventory

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
            "abilities": self.abilities
        }
