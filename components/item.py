"""
Item component for MUDpy SS13.
Represents an item that can be picked up and used.
"""

from typing import Dict, List, Any, Optional, Callable
import logging
from events import publish

logger = logging.getLogger(__name__)


class ItemComponent:
    """
    Component that represents an item in the game world.
    """

    def __init__(
        self,
        weight: float = 1.0,
        is_takeable: bool = True,
        is_usable: bool = False,
        use_effect: Optional[str] = None,
        item_type: str = "miscellaneous",
        item_properties: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the item component.

        Args:
            weight (float): The weight of the item.
            is_takeable (bool): Whether the item can be picked up.
            is_usable (bool): Whether the item can be used.
            use_effect (str, optional): Custom use effect description.
            item_type (str): The type of item (e.g., "tool", "weapon", "keycard").
            item_properties (Dict[str, Any], optional): Additional properties.
        """
        self.owner = None
        self.weight = weight
        self.is_takeable = is_takeable
        self.is_usable = is_usable
        self.use_effect = use_effect
        self.item_type = item_type
        self.item_properties = item_properties or {}
        self.custom_use_handler = None

    def set_custom_use_handler(self, handler: Callable[[str], str]) -> None:
        """
        Set a custom handler function for item use.

        Args:
            handler (Callable[[str], str]): Function that takes player_id and returns a message.
        """
        self.custom_use_handler = handler

    def take(self, player_id: str) -> str:
        """
        Attempt to take the item.

        Args:
            player_id (str): The ID of the player trying to take the item.

        Returns:
            str: Response message.
        """
        if not self.is_takeable:
            return f"The {self.owner.name} cannot be taken."

        # The actual inventory management is handled by the player's inventory component
        publish("item_taken", item_id=self.owner.id, player_id=player_id)

        return f"You take the {self.owner.name}."

    def drop(self, player_id: str) -> str:
        """
        Attempt to drop the item.

        Args:
            player_id (str): The ID of the player trying to drop the item.

        Returns:
            str: Response message.
        """
        # The actual inventory management is handled by the player's inventory component
        publish("item_dropped", item_id=self.owner.id, player_id=player_id)

        return f"You drop the {self.owner.name}."

    def use(self, player_id: str) -> str:
        """
        Attempt to use the item.

        Args:
            player_id (str): The ID of the player trying to use the item.

        Returns:
            str: Response message.
        """
        if not self.is_usable:
            return f"The {self.owner.name} cannot be used."

        # If there's a custom use handler, delegate to it
        if self.custom_use_handler:
            return self.custom_use_handler(player_id)

        # Medical items automatically heal based on properties
        if self.item_type == "medical":
            from world import get_world

            world_instance = get_world()
            player = world_instance.get_object(player_id)
            if player:
                comp = player.get_component("player")
                if comp:
                    heal_type = self.item_properties.get("heal_type")
                    heal_amount = self.item_properties.get("heal_amount", 0)
                    body_part = self.item_properties.get("body_part", "torso")
                    if heal_type:
                        comp.heal_damage(body_part, heal_type, heal_amount)
                    disease = self.item_properties.get("cures")
                    if disease:
                        comp.cure_disease(disease)
            doses = self.item_properties.get("doses_remaining")
            if doses is not None:
                if doses <= 0:
                    return f"The {self.owner.name} is empty."
                self.item_properties["doses_remaining"] = doses - 1

        # Diagnostic scanners provide detailed health information
        elif self.item_type == "diagnostic":
            from world import get_world

            world_instance = get_world()
            player = world_instance.get_object(player_id)
            if player:
                comp = player.get_component("player")
                if comp:
                    status = []
                    for part, damage in comp.body_parts.items():
                        for dtype, val in damage.items():
                            if val > 0:
                                status.append(f"{part} {dtype}: {val}")
                    if comp.diseases:
                        status.append("Diseases: " + ", ".join(comp.diseases))
                    if status:
                        return "; ".join(status)
                    else:
                        return "No issues detected."

        # Food items restore player nutrition
        elif self.item_type == "food":
            from world import get_world

            world_instance = get_world()
            player = world_instance.get_object(player_id)
            if player:
                comp = player.get_component("player")
                if comp:
                    nutrition = self.item_properties.get("nutrition", 0)
                    comp.consume_food(float(nutrition))
            return f"You eat the {self.owner.name}."

        # Otherwise use the default behavior
        publish(
            "item_used",
            item_id=self.owner.id,
            player_id=player_id,
            item_type=self.item_type,
        )

        if self.use_effect:
            return self.use_effect
        else:
            return f"You use the {self.owner.name}."

    def examine(self, player_id: str) -> str:
        """
        Examine the item for more details.

        Args:
            player_id (str): The ID of the player examining the item.

        Returns:
            str: Detailed description of the item.
        """
        description = f"{self.owner.description}\n"

        # Add type-specific information
        if self.item_type == "tool":
            description += f"It appears to be a tool of some kind."
        elif self.item_type == "weapon":
            description += f"It looks like it could be used as a weapon."
        elif self.item_type == "keycard":
            access_level = self.item_properties.get("access_level", 0)
            description += f"Access level: {access_level}"
        elif self.item_type == "medical":
            description += f"It's a medical item. It might have healing properties."
        elif self.item_type == "diagnostic":
            description += "A medical scanner capable of detailed health analysis."
        elif self.item_type == "food":
            nutrition = self.item_properties.get("nutrition", 0)
            description += f"It looks edible and provides {nutrition} nutrition."

        # Add additional property information
        if "durability" in self.item_properties:
            description += f"\nDurability: {self.item_properties['durability']}/100"

        return description

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert this component to a dictionary for serialization.

        Returns:
            Dict[str, Any]: Dictionary representation of this component.
        """
        return {
            "weight": self.weight,
            "is_takeable": self.is_takeable,
            "is_usable": self.is_usable,
            "use_effect": self.use_effect,
            "item_type": self.item_type,
            "item_properties": self.item_properties,
            # Note: custom_use_handler is not serialized as it's a function
        }
