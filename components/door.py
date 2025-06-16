"""
Door component for MUDpy SS13.
Represents a door or airlock that can be opened, closed, and locked.
"""

from typing import Dict, Any, Optional
import logging
from events import publish
from world import get_world

logger = logging.getLogger(__name__)


class DoorComponent:
    """
    Component that represents a door or airlock.
    """

    def __init__(
        self,
        is_open: bool = False,
        is_locked: bool = False,
        destination: Optional[str] = None,
        requires_power: bool = True,
        access_level: int = 0,
    ):
        """
        Initialize the door component.

        Args:
            is_open (bool): Whether the door is currently open.
            is_locked (bool): Whether the door is currently locked.
            destination (str, optional): The room ID this door leads to.
            requires_power (bool): Whether this door requires power to operate.
            access_level (int): The access level required to use this door (0 = public).
        """
        self.owner = None
        self.is_open = is_open
        self.is_locked = is_locked
        self.destination = destination
        self.requires_power = requires_power
        self.access_level = access_level

    def open(self, player_id: str, access_code: Optional[int] = None) -> str:
        """
        Attempt to open the door.

        Args:
            player_id (str): The ID of the player trying to open the door.
            access_code (int, optional): Access code provided by the player.

        Returns:
            str: Response message.
        """
        # Check if door is already open
        if self.is_open:
            return "The door is already open."

        world = get_world()
        level = 0
        player_obj = world.get_object(player_id)
        if player_obj:
            pcomp = player_obj.get_component("player")
            if pcomp:
                level = pcomp.access_level
                for item_id in pcomp.inventory:
                    item = world.get_object(item_id)
                    if item:
                        card = item.get_component("id_card")
                        if card and card.access_level > level:
                            level = card.access_level

        if access_code is not None:
            level = access_code

        # Handle locked doors
        if self.is_locked:
            if level >= self.access_level:
                self.is_locked = False
                logger.debug(
                    f"Door {self.owner.id} unlocked with access level {level}"
                )
            else:
                return "The door is locked. You need proper authorization to unlock it."

        # Open the door
        self.is_open = True
        logger.debug(f"Door {self.owner.id} opened by {player_id}")
        publish("door_opened", door_id=self.owner.id, player_id=player_id)

        return f"You open the {self.owner.name}."

    def close(self, player_id: str) -> str:
        """
        Attempt to close the door.

        Args:
            player_id (str): The ID of the player trying to close the door.

        Returns:
            str: Response message.
        """
        # Check if door is already closed
        if not self.is_open:
            return "The door is already closed."

        # Close the door
        self.is_open = False
        logger.debug(f"Door {self.owner.id} closed by {player_id}")
        publish("door_closed", door_id=self.owner.id, player_id=player_id)

        return f"You close the {self.owner.name}."

    def lock(self, player_id: str, access_code: int) -> str:
        """
        Attempt to lock the door.

        Args:
            player_id (str): The ID of the player trying to lock the door.
            access_code (int): Access code provided by the player.

        Returns:
            str: Response message.
        """
        # Check if door is already locked
        if self.is_locked:
            return "The door is already locked."

        # Check if player has permission to lock the door
        if access_code < self.access_level:
            return "You don't have authorization to lock this door."

        # Lock the door
        self.is_locked = True
        logger.debug(f"Door {self.owner.id} locked by {player_id}")
        publish("door_locked", door_id=self.owner.id, player_id=player_id)

        return f"You lock the {self.owner.name}."

    def unlock(self, player_id: str, access_code: int) -> str:
        """
        Attempt to unlock the door.

        Args:
            player_id (str): The ID of the player trying to unlock the door.
            access_code (int): Access code provided by the player.

        Returns:
            str: Response message.
        """
        # Check if door is already unlocked
        if not self.is_locked:
            return "The door is already unlocked."

        # Check if player has permission to unlock the door
        if access_code < self.access_level:
            return "You don't have authorization to unlock this door."

        # Unlock the door
        self.is_locked = False
        logger.debug(f"Door {self.owner.id} unlocked by {player_id}")
        publish("door_unlocked", door_id=self.owner.id, player_id=player_id)

        return f"You unlock the {self.owner.name}."

    def hack(self, player_id: str, skill: int = 0) -> str:
        """Attempt to hack the door open."""
        if not self.is_locked:
            return "The door is already unlocked."
        if skill < self.access_level:
            return "You fail to hack the door."

        self.is_locked = False
        publish("door_hacked", door_id=self.owner.id, player_id=player_id)
        return f"You hack the {self.owner.name} and unlock it."

    def on_power_loss(self) -> None:
        """
        Handle power loss event.
        Doors that require power will lock automatically on power loss.
        """
        if self.requires_power:
            self.is_locked = True
            self.is_open = False
            logger.debug(f"Door {self.owner.id} locked due to power loss")
            publish("door_emergency_lockdown", door_id=self.owner.id)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert this component to a dictionary for serialization.

        Returns:
            Dict[str, Any]: Dictionary representation of this component.
        """
        return {
            "is_open": self.is_open,
            "is_locked": self.is_locked,
            "destination": self.destination,
            "requires_power": self.requires_power,
            "access_level": self.access_level,
        }
