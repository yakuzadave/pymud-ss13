"""Random events system for MUDpy SS13."""

import asyncio
import logging
import random
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from pathlib import Path

import yaml
from events import publish

logger = logging.getLogger(__name__)


@dataclass
class RandomEvent:
    """Definition of a random event."""

    id: str
    name: str
    weight: int = 1
    params: Dict[str, Any] = field(default_factory=dict)
    description: Optional[str] = None


class RandomEventSystem:
    """System that periodically fires random events."""

    def __init__(
        self,
        events_file: str = "data/random_events.yaml",
        interval: float = 60.0,
    ) -> None:
        self.events_file = events_file
        self.interval = interval
        self.events: List[RandomEvent] = []
        self.weights: List[int] = []
        self.events_by_id: Dict[str, RandomEvent] = {}
        self.enabled = False
        self.task: Optional[asyncio.Task] = None

    def load_events(self) -> None:
        """Load random events from a YAML file."""
        if not Path(self.events_file).exists():
            logger.warning(f"Random events file {self.events_file} not found")
            self.events = []
            return

        try:
            with Path(self.events_file).open("r") as f:
                data = yaml.safe_load(f) or []

            self.events = [
                RandomEvent(
                    id=evt.get("id"),
                    name=evt.get("name", evt.get("id", "event")),
                    weight=evt.get("weight", 1),
                    params=evt.get("params", {}),
                    description=evt.get("description"),
                )
                for evt in data
            ]
            self.weights = [evt.weight for evt in self.events]
            self.events_by_id = {evt.id: evt for evt in self.events if evt.id}
            logger.info(f"Loaded {len(self.events)} random events")
        except Exception as e:
            logger.error(f"Failed to load random events: {e}")
            self.events = []
            self.weights = []
            self.events_by_id = {}

    def start(self) -> None:
        """Start the random event loop."""
        if self.enabled:
            return
        if not self.events:
            self.load_events()
        self.enabled = True
        self.task = asyncio.create_task(self._run())
        logger.info("Random event system started")

    def stop(self) -> None:
        """Stop the random event loop."""
        self.enabled = False
        if self.task and not self.task.done():
            self.task.cancel()
        self.task = None
        logger.info("Random event system stopped")

    async def _run(self) -> None:
        while self.enabled:
            try:
                await asyncio.sleep(self.interval)
                await self.update()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in random event loop: {e}")

    async def update(self) -> None:
        """Choose and fire a random event."""
        if not self.events:
            return

        if not self.weights:
            self.weights = [evt.weight for evt in self.events]

        event = random.choices(self.events, weights=self.weights, k=1)[0]
        logger.debug(f"Triggering random event {event.id}")
        publish(event.id, **event.params)
        publish("random_event", event_id=event.id, event=event)

    def list_events(self) -> List[str]:
        """Return available event IDs."""
        return [evt.id for evt in self.events]

    def trigger_event(self, event_id: str, **kwargs: Any) -> bool:
        """Manually trigger a specific event."""
        event = self.events_by_id.get(event_id)
        if not event:
            return False
        params = {**event.params, **kwargs}
        publish(event.id, **params)
        publish("random_event", event_id=event.id, event=event)
        return True


RANDOM_EVENT_SYSTEM = RandomEventSystem()


def get_random_event_system() -> RandomEventSystem:
    """Return the global random event system instance."""
    return RANDOM_EVENT_SYSTEM
