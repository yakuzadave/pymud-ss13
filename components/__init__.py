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
from .fluid import FluidContainerComponent
from .access import AccessControlComponent
from .id_card import IDCardComponent

from .power_consumer import PowerConsumerComponent
from .structure import StructureComponent
from .ai import AIComponent, CyborgComponent
from .camera import CameraComponent
from .motion_sensor import MotionSensorComponent
from .maintenance import MaintainableComponent
from .circuit import CircuitComponent
from .replica_pod import ReplicaPodComponent
from .medical import MedicalScannerComponent

__all__ = [
    "RoomComponent",
    "DoorComponent",
    "ItemComponent",
    "PlayerComponent",
    "NPCComponent",
    "ContainerComponent",
    "ChemicalContainerComponent",
    "FluidContainerComponent",
    "AccessControlComponent",
    "IDCardComponent",
    "PowerConsumerComponent",
    "StructureComponent",
    "AIComponent",
    "CyborgComponent",
    "CameraComponent",
    "MotionSensorComponent",
    "MaintainableComponent",
    "CircuitComponent",
    "ReplicaPodComponent",
    "MedicalScannerComponent",
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
    "fluid_container": FluidContainerComponent,
    "access": AccessControlComponent,
    "power_consumer": PowerConsumerComponent,
    "structure": StructureComponent,
    "ai": AIComponent,
    "cyborg": CyborgComponent,
    "camera": CameraComponent,
    "motion_sensor": MotionSensorComponent,
    "maintenance": MaintainableComponent,
    "circuit": CircuitComponent,
    "replica_pod": ReplicaPodComponent,
    "medical_scanner": MedicalScannerComponent,
    "id_card": IDCardComponent,
}
