"""Components package for MUDpy SS13.
Components are the building blocks of game objects in the component-based architecture.
"""

from .room import RoomComponent
from .door import DoorComponent
from .item import ItemComponent
from .player import PlayerComponent
from .npc import NPCComponent

__all__ = [
    "RoomComponent",
    "DoorComponent",
    "ItemComponent",
    "PlayerComponent",
    "NPCComponent",
]
