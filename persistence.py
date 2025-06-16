import os
import asyncio
import yaml
import logging
import time
from typing import Any, List, Dict

from components.room import RoomComponent
from components.door import DoorComponent
from components.item import ItemComponent
from components.npc import NPCComponent
from world import GameObject, World
import inspect

logger = logging.getLogger(__name__)


def _read_yaml(path: str) -> List[Any]:
    try:
        with open(path, "r") as f:
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
                id=room_data["id"],
                name=room_data["name"],
                description=room_data.get("description", ""),
            )
            if "components" in room_data:
                comps = room_data["components"]
                if "room" in comps:
                    rc = comps["room"]
                    room_comp = RoomComponent(
                        exits=rc.get("exits", {}),
                        atmosphere=rc.get("atmosphere", {}),
                        hazards=rc.get("hazards", []),
                        is_airlock=rc.get("is_airlock", False),
                    )
                    room_obj.add_component("room", room_comp)
                if "door" in comps:
                    dc = comps["door"]
                    door_comp = DoorComponent(
                        is_open=dc.get("is_open", False),
                        is_locked=dc.get("is_locked", False),
                        destination=dc.get("destination"),
                        requires_power=dc.get("requires_power", True),
                        access_level=dc.get("access_level", 0),
                    )
                    room_obj.add_component("door", door_comp)
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
                id=item_data["id"],
                name=item_data["name"],
                description=item_data.get("description", ""),
                location=item_data.get("location"),
            )
            if "components" in item_data:
                comps = item_data["components"]
                if "item" in comps:
                    ic = comps["item"]
                    item_comp = ItemComponent(
                        weight=ic.get("weight", 1.0),
                        is_takeable=ic.get("is_takeable", True),
                        is_usable=ic.get("is_usable", False),
                        use_effect=ic.get("use_effect"),
                        item_type=ic.get("item_type", "miscellaneous"),
                        item_properties=ic.get("item_properties", {}),
                    )
                    item_obj.add_component("item", item_comp)
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
                id=npc_data["id"],
                name=npc_data["name"],
                description=npc_data.get("description", ""),
                location=npc_data.get("location"),
            )
            if "components" in npc_data and "npc" in npc_data["components"]:
                nc = npc_data["components"]["npc"]
                npc_comp = NPCComponent(
                    role=nc.get("role", "crew"),
                    dialogue=nc.get("dialogue", []),
                    routine=nc.get("routine", []),
                    event_dialogue=nc.get("event_dialogue", {}),
                )
                npc_obj.add_component("npc", npc_comp)
            world.register(npc_obj)
            count += 1
        except Exception as e:
            logger.error(f"Error loading NPC data {npc_data}: {e}")
    logger.info(f"Loaded {count} NPCs from {path}")
    return count


def load_players(directory: str, world: World) -> int:
    """Load player objects from individual YAML files in ``directory``."""
    if not os.path.isdir(directory):
        logger.debug(f"Player directory not found: {directory}")
        return 0

    count = 0
    for filename in sorted(os.listdir(directory)):
        if not filename.endswith(".yaml"):
            continue
        path = os.path.join(directory, filename)
        try:
            with open(path, "r") as f:
                data = yaml.safe_load(f)
            if not isinstance(data, dict):
                logger.error(f"Expected dict in {path}, got {type(data)}")
                continue

            obj = GameObject(
                id=data.get("id"),
                name=data.get("name", ""),
                description=data.get("description", ""),
                location=data.get("location"),
            )

            if "components" in data:
                from components import COMPONENT_REGISTRY

                for comp_name, comp_data in data["components"].items():
                    comp_class = COMPONENT_REGISTRY.get(comp_name)
                    if comp_class and isinstance(comp_data, dict):
                        params = inspect.signature(comp_class.__init__).parameters
                        kwargs = {
                            k: v
                            for k, v in comp_data.items()
                            if k in params and k != "self"
                        }
                        try:
                            comp_instance = comp_class(**kwargs)
                        except Exception as e:
                            logger.warning(
                                f"Failed to instantiate component {comp_name} for {obj.id}: {e}"
                            )
                            continue
                        obj.add_component(comp_name, comp_instance)
                    else:
                        obj.components[comp_name] = comp_data

            world.register(obj)
            count += 1
        except FileNotFoundError:
            logger.debug(f"Player file not found: {path}")
        except Exception as e:
            logger.error(f"Error loading player file {path}: {e}")

    logger.info(f"Loaded {count} players from {directory}")
    return count


def game_object_to_dict(obj: GameObject) -> Dict[str, Any]:
    """Convert a GameObject and its components into a serializable dict."""
    data = {
        "id": obj.id,
        "name": obj.name,
        "description": obj.description,
        "location": obj.location,
        "components": {},
    }
    for name, comp in obj.components.items():
        if hasattr(comp, "to_dict"):
            data["components"][name] = comp.to_dict()
    return data


def save_game_object(obj: GameObject, path: str) -> None:
    """Serialize a GameObject to YAML and write it to ``path``."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        yaml.dump(
            game_object_to_dict(obj), f, default_flow_style=False, sort_keys=False
        )
    logger.info(f"Saved object {obj.id} to {path}")


def world_to_list(world: World) -> List[Dict[str, Any]]:
    """Return a list of all objects in the world as dicts."""
    return [game_object_to_dict(o) for o in world.objects.values()]


def save_world(world: World, path: str) -> None:
    """Write the entire world state to a YAML file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        yaml.dump(world_to_list(world), f, default_flow_style=False, sort_keys=False)
    logger.info(f"Saved {len(world.objects)} objects to {path}")


async def autosave_loop(
    world: World,
    interval: int = 60,
    *,
    iterations: int | None = None,
    prefix: str = "autosave",
) -> None:
    """Periodically write world snapshots to ``data/world``."""
    count = 0
    while iterations is None or count < iterations:
        await asyncio.sleep(interval)
        timestamp = int(time.time())
        filename = os.path.join(world.data_dir, "world", f"{prefix}_{timestamp}.yaml")
        save_world(world, filename)
        save_scripts(os.path.join(world.data_dir, "scripts.yaml"))
        count += 1


def load_aliases(path: str) -> Dict[str, str]:
    """Load a dictionary of command aliases from ``path``."""
    try:
        with open(path, "r") as f:
            data = yaml.safe_load(f) or {}
        if not isinstance(data, dict):
            logger.error(f"Expected dict in {path}, got {type(data)}")
            return {}
        return {str(k): str(v) for k, v in data.items()}
    except FileNotFoundError:
        logger.debug(f"Alias file not found: {path}")
        return {}
    except Exception as e:
        logger.error(f"Error reading aliases from {path}: {e}")
        return {}


def save_aliases(aliases: Dict[str, str], path: str) -> None:
    """Write the ``aliases`` mapping to ``path`` as YAML."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        with open(path, "w") as f:
            yaml.safe_dump(dict(sorted(aliases.items())), f, default_flow_style=False)
    except Exception as e:
        logger.error(f"Failed to save aliases to {path}: {e}")


def load_scripts(path: str) -> int:
    """Load scripts from ``path`` into the global script engine."""
    from systems.script_engine import get_script_engine

    engine = get_script_engine()
    if not os.path.exists(path):
        logger.debug(f"Script file not found: {path}")
        return 0
    try:
        engine.load_from_file(path)
        return len(engine.scripts)
    except Exception as e:
        logger.error(f"Error loading scripts from {path}: {e}")
        return 0


def save_scripts(path: str) -> None:
    """Save all registered scripts to ``path``."""
    from systems.script_engine import get_script_engine

    engine = get_script_engine()
    try:
        engine.save_to_file(path)
    except Exception as e:
        logger.error(f"Failed to save scripts to {path}: {e}")
