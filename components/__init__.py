"""Components package for MUDpy SS13.
Components are the building blocks of game objects in the component-based architecture.
"""

from .room import RoomComponent
from .door import DoorComponent
from .item import ItemComponent
from .player import PlayerComponent
from .npc import NPCComponent
from .container import ContainerComponent
from systems.chemical_reactions import ChemicalContainerComponent
from .access import AccessControlComponent

__all__ = [
    "RoomComponent",
    "DoorComponent",
    "ItemComponent",
    "PlayerComponent",
    "NPCComponent",
    "ContainerComponent",
    "ChemicalContainerComponent",
    "AccessControlComponent",
]

# Mapping of component names in YAML to classes
COMPONENT_REGISTRY = {
    "room": RoomComponent,
    "door": DoorComponent,
    "item": ItemComponent,
    "player": PlayerComponent,
    "npc": NPCComponent,
    "container": ContainerComponent,
    "chemical_container": ChemicalContainerComponent,
    "access": AccessControlComponent,
}
