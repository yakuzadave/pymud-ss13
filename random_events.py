import yaml
import logging
from typing import Dict, Any, List

from events import publish

logger = logging.getLogger(__name__)

RANDOM_EVENTS: Dict[str, Dict[str, Any]] = {}


def load_random_events(path: str = 'data/random_events.yaml') -> None:
    """Load random events from a YAML file."""
    global RANDOM_EVENTS
    try:
        with open(path, 'r') as f:
            data = yaml.safe_load(f) or []
        if isinstance(data, list):
            RANDOM_EVENTS = {evt['id']: evt for evt in data if 'id' in evt}
        elif isinstance(data, dict):
            RANDOM_EVENTS = data
        logger.info(f"Loaded {len(RANDOM_EVENTS)} random events from {path}")
    except FileNotFoundError:
        logger.warning(f"Random events file not found: {path}")
        RANDOM_EVENTS = {}
    except Exception as e:
        logger.error(f"Error loading random events from {path}: {e}")
        RANDOM_EVENTS = {}


def list_events() -> List[str]:
    """Return a list of available random event IDs."""
    return list(RANDOM_EVENTS.keys())


def trigger_event(event_id: str, **kwargs) -> bool:
    """Trigger a random event by publishing it."""
    event = RANDOM_EVENTS.get(event_id)
    if not event:
        return False


    # Merge event data with any additional parameters.
    # Warn if there are key conflicts that will be overwritten by kwargs.
    conflicting_keys = set(event.keys()) & set(kwargs.keys())
    if conflicting_keys:
        logger.warning(
            "Key conflicts detected in event '%s': %s. Values from kwargs will overwrite event values.",
            event_id,
            conflicting_keys,
        )

    merged_event = {**event, **kwargs}  # kwargs overwrite event values

    publish(event_id, **merged_event)
    publish("random_event", event_id=event_id, event=merged_event)
    #publish(event_id, **event, **kwargs)
    #publish('random_event', event_id=event_id, event=event, **kwargs)

    return True


# Load events on import
load_random_events()
