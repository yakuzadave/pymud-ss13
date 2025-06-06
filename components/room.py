"""
Room component for MUDpy SS13.
Represents a location in the game world.
"""

from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

class RoomComponent:
    """
    Component that represents a location in the game world.
    """
    
    def __init__(self, 
                 exits: Optional[Dict[str, str]] = None, 
                 atmosphere: Optional[Dict[str, float]] = None,
                 hazards: Optional[List[str]] = None,
                 is_airlock: bool = False):
        """
        Initialize the room component.
        
        Args:
            exits (Dict[str, str], optional): Mapping of direction -> room_id.
            atmosphere (Dict[str, float], optional): Atmospheric conditions.
            hazards (List[str], optional): List of hazards in the room.
            is_airlock (bool): Whether this room is an airlock.
        """
        self.owner = None
        self.exits = exits or {}
        self.atmosphere = atmosphere or {"oxygen": 21.0, "nitrogen": 78.0, "co2": 0.04, "pressure": 101.3}
        self.hazards = hazards or []
        self.is_airlock = is_airlock
        
    def get_exit(self, direction: str) -> Optional[str]:
        """
        Get the room ID for an exit in a given direction.
        
        Args:
            direction (str): The direction to check.
            
        Returns:
            Optional[str]: The room ID if an exit exists, None otherwise.
        """
        return self.exits.get(direction.lower())
    
    def add_exit(self, direction: str, room_id: str) -> None:
        """
        Add an exit to this room.
        
        Args:
            direction (str): The direction of the exit.
            room_id (str): The ID of the connecting room.
        """
        self.exits[direction.lower()] = room_id
        logger.debug(f"Added exit from {self.owner.id} to {room_id} in direction {direction}")
    
    def remove_exit(self, direction: str) -> bool:
        """
        Remove an exit from this room.
        
        Args:
            direction (str): The direction of the exit to remove.
            
        Returns:
            bool: True if the exit was removed, False if it didn't exist.
        """
        if direction.lower() in self.exits:
            del self.exits[direction.lower()]
            logger.debug(f"Removed exit from {self.owner.id} in direction {direction}")
            return True
        return False
    
    def update_atmosphere(self, changes: Dict[str, float]) -> None:
        """
        Update the atmospheric conditions in this room.
        
        Args:
            changes (Dict[str, float]): Changes to apply to the atmosphere.
        """
        for gas, value in changes.items():
            if gas in self.atmosphere:
                self.atmosphere[gas] += value
            else:
                self.atmosphere[gas] = value
                
        # Ensure values stay in reasonable ranges
        for gas in self.atmosphere:
            if gas != "pressure":
                self.atmosphere[gas] = max(0, min(100, self.atmosphere[gas]))
                
        logger.debug(f"Updated atmosphere in {self.owner.id}: {self.atmosphere}")
    
    def add_hazard(self, hazard: str) -> None:
        """
        Add a hazard to this room.
        
        Args:
            hazard (str): The hazard to add.
        """
        if hazard not in self.hazards:
            self.hazards.append(hazard)
            logger.debug(f"Added hazard {hazard} to {self.owner.id}")
    
    def remove_hazard(self, hazard: str) -> bool:
        """
        Remove a hazard from this room.
        
        Args:
            hazard (str): The hazard to remove.
            
        Returns:
            bool: True if the hazard was removed, False if it didn't exist.
        """
        if hazard in self.hazards:
            self.hazards.remove(hazard)
            logger.debug(f"Removed hazard {hazard} from {self.owner.id}")
            return True
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert this component to a dictionary for serialization.
        
        Returns:
            Dict[str, Any]: Dictionary representation of this component.
        """
        return {
            "exits": self.exits,
            "atmosphere": self.atmosphere,
            "hazards": self.hazards,
            "is_airlock": self.is_airlock
        }
