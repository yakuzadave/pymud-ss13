import os
import yaml
import logging
from typing import Any, List

from components.room import RoomComponent
from components.door import DoorComponent
from components.item import ItemComponent
from components.npc import NPCComponent
from world import GameObject

logger = logging.getLogger(__name__)

def _read_yaml(path: str) -> List[Any]:
    try:
        with open(path, 'r') as f:
            data = yaml.safe_load(f) or []
        if not isinstance(data, list):
            logger.error(f"Expected list in {path}, got {type(data)}")
            return []
        return data
    except FileNotFoundError:
        logger.warning(f"File not found: {path}")
        return []
    except Exception as e:
        logger.error(f"Error reading {path}: {e}")
        return []

def load_rooms(path: str, world) -> int:
    """Load rooms from YAML file into the given world."""
    rooms_data = _read_yaml(path)
    count = 0
    for room_data in rooms_data:
        try:
            room_obj = GameObject(
                id=room_data['id'],
                name=room_data['name'],
                description=room_data.get('description', '')
            )
            if 'components' in room_data:
                comps = room_data['components']
                if 'room' in comps:
                    rc = comps['room']
                    room_comp = RoomComponent(
                        exits=rc.get('exits', {}),
                        atmosphere=rc.get('atmosphere', {}),
                        hazards=rc.get('hazards', []),
                        is_airlock=rc.get('is_airlock', False)
                    )
                    room_obj.add_component('room', room_comp)
                if 'door' in comps:
                    dc = comps['door']
                    door_comp = DoorComponent(
                        is_open=dc.get('is_open', False),
                        is_locked=dc.get('is_locked', False),
                        destination=dc.get('destination'),
                        requires_power=dc.get('requires_power', True),
                        access_level=dc.get('access_level', 0)
                    )
                    room_obj.add_component('door', door_comp)
            world.register(room_obj)
            count += 1
        except Exception as e:
            logger.error(f"Error loading room data {room_data}: {e}")
    logger.info(f"Loaded {count} rooms from {path}")
    return count

def load_items(path: str, world) -> int:
    items_data = _read_yaml(path)
    count = 0
    for item_data in items_data:
        try:
            item_obj = GameObject(
                id=item_data['id'],
                name=item_data['name'],
                description=item_data.get('description', ''),
                location=item_data.get('location')
            )
            if 'components' in item_data:
                comps = item_data['components']
                if 'item' in comps:
                    ic = comps['item']
                    item_comp = ItemComponent(
                        weight=ic.get('weight', 1.0),
                        is_takeable=ic.get('is_takeable', True),
                        is_usable=ic.get('is_usable', False),
                        use_effect=ic.get('use_effect'),
                        item_type=ic.get('item_type', 'miscellaneous'),
                        item_properties=ic.get('item_properties', {})
                    )
                    item_obj.add_component('item', item_comp)
            world.register(item_obj)
            count += 1
        except Exception as e:
            logger.error(f"Error loading item data {item_data}: {e}")
    logger.info(f"Loaded {count} items from {path}")
    return count

def load_npcs(path: str, world) -> int:
    npcs_data = _read_yaml(path)
    count = 0
    for npc_data in npcs_data:
        try:
            npc_obj = GameObject(
                id=npc_data['id'],
                name=npc_data['name'],
                description=npc_data.get('description', ''),
                location=npc_data.get('location')
            )
            if 'components' in npc_data and 'npc' in npc_data['components']:
                nc = npc_data['components']['npc']
                npc_comp = NPCComponent(
                    role=nc.get('role', 'crew'),
                    dialogue=nc.get('dialogue', [])
                )
                npc_obj.add_component('npc', npc_comp)
            world.register(npc_obj)
            count += 1
        except Exception as e:
            logger.error(f"Error loading NPC data {npc_data}: {e}")
    logger.info(f"Loaded {count} NPCs from {path}")
    return count
